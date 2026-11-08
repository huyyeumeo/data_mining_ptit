"""
BTL Khai phá dữ liệu - Đề 8: SMS Spam Detection
================================================
Mỗi bước được đánh dấu [Slide ...] để đối chiếu với bài giảng:
  - Data.pptx           : Chapter 2. Data, Measurements, and Data Preprocessing
  - Classification.pptx : Chapter 6. Classification: Basic Concepts
Phần ngoài slide (bắt buộc theo đề bài) được đánh dấu [Đề bài].

Chạy:  python spam_detection.py      -> kết quả lưu trong ./outputs
"""

import io
import os
import re
import zipfile
import urllib.request

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.stem import PorterStemmer
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve)
from sklearn.model_selection import (StratifiedKFold, cross_validate,
                                     train_test_split)
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "SMSSpamCollection")
OUT_DIR = os.path.join(BASE_DIR, "outputs")
SEED = 42
DATA_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"

META_COLS = ["num_chars", "num_words", "num_upper", "num_digits",
             "num_special", "has_url", "has_money"]


def section(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# =============================================================================
# 0. NẠP DỮ LIỆU
# =============================================================================
def load_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        print(f"[*] Tải dữ liệu từ {DATA_URL}")
        raw = urllib.request.urlopen(DATA_URL, timeout=30).read()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            open(DATA_PATH, "wb").write(z.read("SMSSpamCollection"))
    return pd.read_csv(DATA_PATH, sep="\t", header=None,
                       names=["label", "message"], quoting=3, encoding="utf-8")


# =============================================================================
# 1. LÀM SẠCH DỮ LIỆU  [Data.pptx - Slide 61-66: Data Cleaning]
# =============================================================================
def clean_data(df):
    section("1. LÀM SẠCH DỮ LIỆU (Data Cleaning)")
    # Slide 64-65: Missing data -> bỏ bản ghi thiếu nhãn/nội dung
    n_missing = df.isna().any(axis=1).sum()
    # Slide 66: Duplicate records là một dạng dữ liệu nhiễu
    n_dup = df.duplicated().sum()
    df = df.dropna().drop_duplicates().reset_index(drop=True)
    print(f"Bản ghi thiếu giá trị: {n_missing} | Bản ghi trùng lặp: {n_dup} -> đã loại bỏ")
    print(f"Còn lại: {len(df)} tin nhắn")

    # Slide 9: thuộc tính nhị phân bất đối xứng -> gán 1 cho lớp quan trọng (spam)
    df["target"] = (df["label"] == "spam").astype(int)
    return df


# =============================================================================
# 2. XÂY DỰNG THUỘC TÍNH METADATA
#    [Data.pptx - Slide 73: Attribute/feature construction]  [Đề bài: length, special chars]
# =============================================================================
def build_meta_features(df):
    m = df["message"]
    df["num_chars"] = m.str.len()
    df["num_words"] = m.str.split().str.len()
    df["num_upper"] = m.str.count(r"[A-Z]")
    df["num_digits"] = m.str.count(r"\d")
    df["num_special"] = m.str.count(r"[^A-Za-z0-9\s]")
    df["has_url"] = m.str.contains(r"http|www\.", case=False).astype(int)
    df["has_money"] = m.str.contains(r"[£$€]").astype(int)
    return df


# =============================================================================
# 3. THỐNG KÊ MÔ TẢ  [Data.pptx - Slide 12-38: Statics of Data]
# =============================================================================
def describe_data(df):
    section("2. THỐNG KÊ MÔ TẢ (Statistical Descriptions)")
    counts = df["label"].value_counts()
    for lbl, n in counts.items():
        print(f"  {lbl:<5}: {n:>5} ({n / len(df):.1%})")
    print("-> Dữ liệu mất cân bằng lớp (Classification.pptx - Slide 76)")

    # Slide 14-19: Mean, Median, Mode, Variance/Std
    print("\nĐộ dài tin nhắn (ký tự) theo lớp:")
    g = df.groupby("label")["num_chars"]
    stats = pd.DataFrame({
        "mean": g.mean(), "median": g.median(),
        "mode": g.agg(lambda s: s.mode().iloc[0]), "std": g.std(),
        # Slide 33: Five-number summary
        "min": g.min(), "Q1": g.quantile(.25), "Q3": g.quantile(.75), "max": g.max(),
    }).round(1)
    print(stats.to_string())

    # Slide 33: Outlier = giá trị vượt Q3 + 1.5 x IQR
    q1, q3 = df["num_chars"].quantile([.25, .75])
    upper = q3 + 1.5 * (q3 - q1)
    print(f"\nOutlier theo 1.5xIQR (num_chars > {upper:.0f}): "
          f"{(df['num_chars'] > upper).sum()} tin")

    # Slide 29: Hệ số tương quan giữa thuộc tính metadata và nhãn
    corr = df[META_COLS + ["target"]].corr()["target"].drop("target")
    print("\nHệ số tương quan (Pearson) giữa metadata và nhãn spam:")
    print(corr.sort_values(ascending=False).round(3).to_string())

    # Biểu đồ: Bar chart (nhãn), Histogram, Boxplot  [Slide 32-35]
    pal = {"ham": "#4C72B0", "spam": "#DD5555"}
    fig, ax = plt.subplots(1, 3, figsize=(16, 4))
    sns.countplot(x="label", hue="label", data=df, palette=pal, legend=False, ax=ax[0])
    ax[0].set_title("Bar chart: phân bố nhãn")
    sns.histplot(data=df, x="num_chars", hue="label", bins=60, palette=pal,
                 element="step", ax=ax[1])
    ax[1].set_xlim(0, 400)
    ax[1].set_title("Histogram: độ dài tin nhắn")
    sns.boxplot(data=df, x="label", y="num_chars", hue="label", palette=pal,
                legend=False, ax=ax[2])
    ax[2].set_ylim(0, 400)
    ax[2].set_title("Boxplot: độ dài tin nhắn")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "1_statistics.png"), dpi=120)
    plt.close()


# =============================================================================
# 4. TIỀN XỬ LÝ VĂN BẢN  [Đề bài: tokenization, stop-word removal, stemming]
# =============================================================================
stemmer = PorterStemmer()


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)              # bỏ số, dấu câu (đã đếm ở metadata)
    tokens = text.split()                               # tokenization
    tokens = [w for w in tokens if w not in ENGLISH_STOP_WORDS and len(w) > 1]
    return " ".join(stemmer.stem(w) for w in tokens)    # stemming


# =============================================================================
# 5. BIỂU DIỄN DỮ LIỆU & CHỌN THUỘC TÍNH
#  - Bag-of-Words = Term-frequency vector          [Data.pptx - Slide 2, 54]
#  - Dữ liệu thưa, nhiều chiều (curse of dim.)     [Data.pptx - Slide 6, 96]
#  - Chọn thuộc tính bằng kiểm định Chi-square     [Data.pptx - Slide 20, 100-101]
#  - Chuẩn hóa Min-max cho metadata                [Data.pptx - Slide 74]
# =============================================================================
K_WORDS = 1000


def make_features():
    return ColumnTransformer([
        ("bow", Pipeline([
            ("count", CountVectorizer(min_df=2)),
            ("chi2", SelectKBest(chi2, k=K_WORDS)),
        ]), "clean"),
        ("meta", MinMaxScaler(), META_COLS),
    ])


def make_models():
    return {
        # [Classification.pptx - Slide 22, 29] Naive Bayes + Laplacian correction
        "Naive Bayes": MultinomialNB(alpha=1.0),
        # [Đề bài] SVM tuyến tính (giáo trình Han - Chương 9)
        "Linear SVM": LinearSVC(C=1.0, random_state=SEED),
        # [Classification.pptx - Slide 14-15] Decision Tree dùng Information Gain (entropy)
        "Decision Tree": DecisionTreeClassifier(criterion="entropy", max_depth=15,
                                                random_state=SEED),
    }


def pipe(clf):
    return Pipeline([("features", make_features()), ("clf", clf)])


def scores_of(model, X):
    return (model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba")
            else model.decision_function(X))


# =============================================================================
# 6. ĐÁNH GIÁ  [Classification.pptx - Slide 52-62]
# =============================================================================
def metrics(y, y_pred, s):
    tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
    return {
        "Accuracy": accuracy_score(y, y_pred),          # Slide 54
        "Error rate": (fp + fn) / len(y),               # Slide 54
        "Sensitivity/Recall": recall_score(y, y_pred),  # Slide 54-55
        "Specificity": tn / (tn + fp),                  # Slide 54
        "Precision": precision_score(y, y_pred),        # Slide 55
        "F1": f1_score(y, y_pred),                      # Slide 56
        "AUC": roc_auc_score(y, s),                     # Slide 62
    }


def holdout_evaluation(X_train, X_test, y_train, y_test):
    section("4. ĐÁNH GIÁ HOLDOUT (Classification.pptx - Slide 60)")
    rows, fitted = {}, {}
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    plt_roc = plt.figure(figsize=(6, 5)).gca()

    for i, (name, clf) in enumerate(make_models().items()):
        model = pipe(clf).fit(X_train, y_train)
        y_pred, s = model.predict(X_test), scores_of(model, X_test)
        rows[name], fitted[name] = metrics(y_test, y_pred, s), model

        # Slide 53: Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax[i],
                    xticklabels=["ham", "spam"], yticklabels=["ham", "spam"])
        ax[i].set(title=f"{name}\nFP={cm[0, 1]}  FN={cm[1, 0]}",
                  xlabel="Predicted class", ylabel="Actual class")

        # Slide 62: ROC curve
        fpr, tpr, _ = roc_curve(y_test, s)
        plt_roc.plot(fpr, tpr, label=f"{name} (AUC={rows[name]['AUC']:.3f})")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "3_confusion_matrices.png"), dpi=120)
    plt_roc.plot([0, 1], [0, 1], "k--", alpha=.5)
    plt_roc.set(xlabel="False positive rate (FP/N)", ylabel="True positive rate (TP/P)",
                title="ROC curves")
    plt_roc.legend()
    plt_roc.figure.tight_layout()
    plt_roc.figure.savefig(os.path.join(OUT_DIR, "4_roc_curves.png"), dpi=120)
    plt.close("all")

    result = pd.DataFrame(rows).T.round(4)
    print(result.to_string())
    result.to_csv(os.path.join(OUT_DIR, "results_holdout.csv"))
    return fitted


def cross_validation(X, y):
    section("5. STRATIFIED 10-FOLD CROSS-VALIDATION (Classification.pptx - Slide 61)")
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)
    rows = {}
    for name, clf in make_models().items():
        r = cross_validate(pipe(clf), X, y, cv=cv,
                           scoring=["accuracy", "precision", "recall", "f1"])
        rows[name] = {m: f"{r['test_' + m].mean():.4f} ± {r['test_' + m].std():.4f}"
                      for m in ["accuracy", "precision", "recall", "f1"]}
    result = pd.DataFrame(rows).T
    print(result.to_string())
    result.to_csv(os.path.join(OUT_DIR, "results_cv.csv"))


# =============================================================================
# 7. CÁC THÍ NGHIỆM MINH HỌA LÝ THUYẾT
# =============================================================================
def experiment_laplace(X_train, X_test, y_train, y_test):
    """[Classification.pptx - Slide 29] Zero-probability problem & Laplacian correction."""
    section("6a. THÍ NGHIỆM: LAPLACIAN CORRECTION (Slide 29)")
    for alpha, desc in [(1e-10, "không làm mịn (alpha≈0)"), (1.0, "Laplace (alpha=1)")]:
        m = pipe(MultinomialNB(alpha=alpha)).fit(X_train, y_train)
        y_pred = m.predict(X_test)
        print(f"  {desc:<26} Precision={precision_score(y_test, y_pred):.4f}  "
              f"Recall={recall_score(y_test, y_pred):.4f}  F1={f1_score(y_test, y_pred):.4f}")


def experiment_overfitting(X_train, X_test, y_train, y_test):
    """[Classification.pptx - Slide 13, 59] Overfitting của Decision Tree: Training vs Testing error."""
    section("6b. THÍ NGHIỆM: OVERFITTING CỦA DECISION TREE (Slide 59)")
    depths = [1, 2, 3, 5, 8, 12, 15, 20, 30, 50, None]
    tr_err, te_err = [], []
    for d in depths:
        m = pipe(DecisionTreeClassifier(criterion="entropy", max_depth=d,
                                        random_state=SEED)).fit(X_train, y_train)
        tr_err.append(1 - m.score(X_train, y_train))
        te_err.append(1 - m.score(X_test, y_test))
    labels = [str(d) if d else "∞" for d in depths]
    for l, a, b in zip(labels, tr_err, te_err):
        print(f"  max_depth={l:>3}: training error={a:.4f}  testing error={b:.4f}")

    plt.figure(figsize=(7, 4))
    plt.plot(labels, tr_err, "o-", label="Training error")
    plt.plot(labels, te_err, "s-", label="Testing error")
    plt.xlabel("max_depth")
    plt.ylabel("Error rate")
    plt.title("Decision Tree: Training vs Testing error")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "5_tree_overfitting.png"), dpi=120)
    plt.close()


def top_chi2_words(model, k=15):
    """[Data.pptx - Slide 20] Những từ có giá trị Chi-square cao nhất (liên quan mạnh nhất với nhãn)."""
    bow = model.named_steps["features"].named_transformers_["bow"]
    vocab = bow.named_steps["count"].get_feature_names_out()
    sel = bow.named_steps["chi2"]
    order = np.argsort(np.nan_to_num(sel.scores_))[::-1][:k]
    section("3. CHỌN THUỘC TÍNH BẰNG CHI-SQUARE (Data.pptx - Slide 20, 101)")
    print(f"Từ vựng ban đầu: {len(vocab)} từ -> giữ lại {K_WORDS} từ có χ² cao nhất")
    print("Top từ: " + ", ".join(f"{vocab[i]}({sel.scores_[i]:.0f})" for i in order))


def demo(model):
    section("7. DEMO DỰ ĐOÁN (Linear SVM)")
    samples = [
        "Hey, are we still meeting for lunch today?",
        "CONGRATULATIONS! You won a $1000 Walmart gift card. Call 09061701461 now to claim!",
        "Can you send me the slides from yesterday's lecture?",
        "URGENT! Your account has been suspended. Verify at http://bit.ly/xyz",
    ]
    d = build_meta_features(pd.DataFrame({"message": samples}))
    d["clean"] = d["message"].apply(preprocess_text)
    for s, p in zip(samples, model.predict(d)):
        print(f"  [{'SPAM' if p else 'HAM '}] {s}")


# =============================================================================
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = clean_data(load_data())
    df = build_meta_features(df)
    describe_data(df)
    df["clean"] = df["message"].apply(preprocess_text)

    X, y = df[["clean"] + META_COLS], df["target"]
    # [Classification.pptx - Slide 60] Holdout: 2/3 train, 1/3 test
    # [Data.pptx - Slide 87] Stratified sampling để giữ tỷ lệ ham/spam
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1 / 3, stratify=y, random_state=SEED)

    fitted = holdout_evaluation(X_train, X_test, y_train, y_test)
    top_chi2_words(fitted["Naive Bayes"])
    cross_validation(X, y)
    experiment_laplace(X_train, X_test, y_train, y_test)
    experiment_overfitting(X_train, X_test, y_train, y_test)

    print(fitted)

    demo(fitted["Linear SVM"])

    demo(fitted["Decision Tree"])

    demo(fitted["Naive Bayes"])

    print(f"\n[+] Kết quả lưu tại: {OUT_DIR}")


if __name__ == "__main__":
    main()
