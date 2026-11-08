import io
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "SMSSpamCollection")

# 1. Giả lập dữ liệu thô giống như cấu trúc bạn cung cấp
data_raw = """spam	Rock yr chik. Get 100's of filthy films &XXX pics on yr phone now. rply FILTH to 69669. Saristar Ltd, E14 9YT 08701752560. 450p per 5 days. Stop2 cancel
ham	Single line with a big meaning::::: "Miss anything 4 ur "Best Life" but, don't miss ur best life for anything... Gud nyt...
ham	I got like $ <#> , I can get some more later though. Get whatever you feel like
ham	Dad wanted to talk about the apartment so I got a late start, omw now
ham	I love you both too :-)
ham	Lol u still feeling sick?
ham	Din i tell u jus now 420
ham	am up to my eyes in philosophy
spam	From next month get upto 50% More Calls 4 Ur standard network charge 2 activate Call 9061100010 C Wire3.net 1st4Terms PoBox84 M26 3UZ Cost £1.50 min MobcudB more
ham	Ok lor. I'm in town now lei.
ham	I had it already..sabarish asked me to go..
ham	No da. . Vijay going to talk in jaya tv
spam	URGENT! We are trying to contact U Todays draw shows that you have won a £800 prize GUARANTEED. Call 09050000460 from land line. Claim J89. po box245c2150pm
ham	Lol I know! Hey someone did a great inpersonation of flea on the forums. I love it!
spam	Text BANNEDUK to 89555 to see! cost 150p textoperator g696ga 18+ XXX"""

# Nếu bạn đọc từ file thật ngoài đời, hãy dùng lệnh dưới đây:
# df = pd.read_csv("ten_file.txt", sep="\t", names=["label", "text"])
df = pd.read_csv(DATA_PATH, sep="\t", header=None,
                       names=["label", "text"], quoting=3, encoding="utf-8")

# 2. Tiền xử lý nhãn (Chuyển đổi ham -> 0, spam -> 1)
df["label_num"] = df["label"].map({"ham": 0, "spam": 1})

# 3. Biến đổi văn bản thành ma trận đếm số lần xuất hiện của Từ (Bag of Words)
# Thêm stop_words='english' để loại bỏ các từ vô nghĩa chung như 'the', 'is', 'at'...
vectorizer = CountVectorizer(stop_words="english", lowercase=True)
X_counts = vectorizer.fit_transform(df["text"])
y = df["label_num"]

# Lấy danh sách toàn bộ các từ (các đặc trưng từ vựng)
feature_names = vectorizer.get_feature_names_out()

# 4. Tính toán điểm Chi-Square cho từng từ
chi2_scores, p_values = chi2(X_counts, y)

# 5. Tạo bảng kết quả và sắp xếp điểm Chi2 từ cao xuống thấp
df_chi2 = pd.DataFrame(
    {"Từ vựng": feature_names, "Điểm Chi2": chi2_scores, "Chỉ số p-value": p_values}
)

# Loại bỏ các giá trị NaN nếu có và sắp xếp giảm dần theo điểm Chi2
df_chi2 = df_chi2.dropna().sort_values(by="Điểm Chi2", ascending=False)

# 6. In ra Top 10 từ có điểm Chi-Square cao nhất (mang tính đặc trưng cho Spam/Ham tốt nhất)
print("--- TOP 10 TỪ VỰNG ĐẶC TRƯNG NHẤT DỰA TRÊN CHI-SQUARE ---")
print(df_chi2.head(10).to_string(index=False))

# 7. Trích xuất ra danh sách (Ví dụ: Lấy 5 từ tốt nhất)
top_k = 5
selector = SelectKBest(score_func=chi2, k=top_k)
X_new = selector.fit_transform(X_counts, y)
selected_features = feature_names[selector.get_support()]

print(f"\n danh sách {top_k} từ được chọn tự động để đưa vào mô hình học máy:")
print(selected_features)