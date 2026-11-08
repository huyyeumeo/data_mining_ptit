# HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
### KHOA CÔNG NGHỆ THÔNG TIN
---

# BÁO CÁO BÀI TẬP LỚN
## MÔN: KHAI PHÁ DỮ LIỆU (DATA MINING)

### ĐỀ TÀI SỐ 8: PHÁT HIỆN TIN NHẮN RÁC (SMS SPAM DETECTION) DỰA TRÊN CÁC KỸ THUẬT PHÂN LỚP DỮ LIỆU

* **Giảng viên hướng dẫn:** [Điền tên Thầy/Cô bộ môn]
* **Nhóm sinh viên thực hiện:** [Điền tên các thành viên trong nhóm]
* **Lớp:** [Điền tên lớp sinh hoạt]
* **Học kỳ / Năm học:** [Ví dụ: Học kỳ 1 - Năm học 2026]

---

## MỤC LỤC
1. [LỜI MỞ ĐẦU](#lời-mở-đầu)
2. [CHƯƠNG 1: TỔNG QUAN TẬP DỮ LIỆU VÀ THỐNG KÊ MÔ TẢ (EDA)](#chương-1-tổng-quan-tập-dữ-liệu-và-thống-kê-mô-tả-eda)
   - 1.1. Giới thiệu tập dữ liệu SMS Spam Collection
   - 1.2. Làm sạch dữ liệu (Data Cleaning)
   - 1.3. Xây dựng các thuộc tính Metadata (Feature Construction)
   - 1.4. Thống kê mô tả 5 số và nhận diện Outliers
   - 1.5. Phân tích tương quan thuộc tính (Correlation Analysis)
3. [CHƯƠNG 2: TIỀN XỬ LÝ VĂN BẢN VÀ LỰA CHỌN THUỘC TÍNH](#chương-2-tiền-xử-lý-văn-bản-và-lựa-chọn-thuộc-tính)
   - 2.1. Quy trình tiền xử lý văn bản (NLP Preprocessing)
   - 2.2. Biểu diễn dữ liệu dạng Bag-of-Words và vấn đề Sparsity
   - 2.3. Lựa chọn thuộc tính bằng kiểm định Chi-Square ($\chi^2$)
   - 2.4. Chuẩn hóa thang đo (Min-Max Normalization)
4. [CHƯƠNG 3: CƠ SỞ PHƯƠNG PHÁP VÀ MÔ HÌNH PHÂN LỚP](#chương-3-cơ-sở-phương-pháp-và-mô-hình-phân-lớp)
   - 3.1. Thuật toán Naïve Bayes và Kỹ thuật làm mịn Laplace
   - 3.2. Thuật toán Linear Support Vector Machine (Linear SVM)
   - 3.3. Thuật toán Cây quyết định (Decision Tree Induction)
   - 3.4. Phương pháp phân chia dữ liệu thẩm định (Holdout & 10-Fold CV)
5. [CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH SO SÁNH](#chương-4-kết-quả-thực-nghiệm-và-phân-tích-so-sánh)
   - 4.1. Hệ thống chỉ số đánh giá (Evaluation Metrics)
   - 4.2. Kết quả phân loại trên tập kiểm thử (Holdout 2/3 - 1/3)
   - 4.3. Kết quả thẩm định chéo Stratified 10-Fold Cross-Validation
   - 4.4. Thí nghiệm thực chứng 1: Vai trò của làm mịn Laplace
   - 4.5. Thí nghiệm thực chứng 2: Hiện tượng quá khớp (Overfitting) trên Cây quyết định
   - 4.6. Thử nghiệm Demo dự đoán tin nhắn thực tế
6. [KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN](#kết-luận-và-hướng-phát-triển)
7. [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)

---

## LỜI MỞ ĐẦU

Trong kỷ nguyên truyền thông số, tin nhắn SMS vẫn là một trong những kênh thông tin trực tiếp, phổ biến và có tỷ lệ mở đọc cao nhất. Tuy nhiên, sự bùng nổ của tin nhắn rác (SMS Spam), tin nhắn quảng cáo không mong muốn và đặc biệt là các tin nhắn lừa đảo viễn thông (SMS Phishing) đang gây ra nhiều phiền toái, đe dọa an toàn thông tin và tài sản của người dùng di động.

Bài toán lọc tin nhắn rác thực chất là một bài toán **Phân lớp văn bản (Text Classification)** kinh điển trong lĩnh vực Khai phá dữ liệu (Data Mining). Mục tiêu của đề tài số 8 là áp dụng quy trình chuẩn trích xuất tri thức (KDD) để xây dựng hệ thống tự động nhận diện tin nhắn rác: từ các bước thu thập, làm sạch dữ liệu, xây dựng và chọn lọc đặc trưng quan trọng, đến việc huấn luyện, đánh giá và so sánh 3 thuật toán phân loại cốt lõi trong chương trình đào tạo của Học viện: **Naïve Bayes, Support Vector Machine (Linear SVM)** và **Cây quyết định (Decision Tree)**.

Báo cáo này trình bày toàn bộ cơ sở lý thuyết, quy trình thực nghiệm và các phân tích chuyên sâu nhằm tìm ra mô hình tối ưu nhất cho bài toán thực tế.

---

## CHƯƠNG 1: TỔNG QUAN TẬP DỮ LIỆU VÀ THỐNG KÊ MÔ TẢ (EDA)
*(Tham chiếu bài giảng: `Data.pptx` - Slide 12–38 & 61–66)*

### 1.1. Giới thiệu tập dữ liệu SMS Spam Collection
Nghiên cứu sử dụng bộ dữ liệu chuẩn **SMS Spam Collection** từ kho lưu trữ của Đại học California (UCI Machine Learning Repository).
* Tổng số bản ghi thô: **5.574 tin nhắn**.
* Dữ liệu ban đầu gồm 2 trường thuộc tính:
  * `label`: Nhãn của tin nhắn (`ham` – tin nhắn bình thường; `spam` – tin nhắn rác).
  * `message`: Chuỗi văn bản nội dung tin nhắn tiếng Anh.

### 1.2. Làm sạch dữ liệu (Data Cleaning)
Dữ liệu trong thế giới thực thường xuyên bị nhiễu và trùng lặp (*Dirty Data* - Slide 63). Nhóm áp dụng quy trình làm sạch chuẩn:
1. **Kiểm tra giá trị thiếu (Missing Data - Slide 64):** Bộ dữ liệu đầy đủ 100%, không có trường rỗng.
2. **Xử lý bản ghi trùng lặp (Duplicate Records - Slide 66):** Phát hiện **403 bản ghi bị trùng lặp hoàn toàn**. Việc giữ lại các bản ghi trùng lặp sẽ gây rò rỉ dữ liệu giữa tập huấn luyện và tập kiểm thử (Data Leakage), làm điểm đánh giá thiếu khách quan. Nhóm đã loại bỏ 403 bản ghi này.
3. **Mã hóa nhãn (Binary Encoding - Slide 9):** Nhãn bài toán thuộc dạng thuộc tính nhị phân bất đối xứng (*Asymmetric Binary*). Theo quy ước, giá trị 1 được gán cho lớp hiếm và quan trọng cần phát hiện:
   $$\text{target} = \begin{cases} 1 & \text{nếu } label = \text{'spam'} \\ 0 & \text{nếu } label = \text{'ham'} \end{cases}$$

Sau khi làm sạch, tập dữ liệu còn lại **5.171 tin nhắn duy nhất**:
* **Ham (Tin nhắn thường):** 4.518 tin (chiếm **87.4%**).
* **Spam (Tin nhắn rác):** 653 tin (chiếm **12.6%**).

> [!NOTE]
> **Nhận xét quan trọng về dữ liệu (Slide 76):** Tỷ lệ phân bố nhãn 87.4% / 12.6% cho thấy đây là một bài toán **Mất cân bằng lớp (Class-Imbalanced Data)** điển hình. Điều này quyết định việc lựa chọn tiêu chí đánh giá ở Chương 4.

---

### 1.3. Xây dựng các thuộc tính Metadata (Feature Construction)
Theo yêu cầu đề bài và nguyên lý trích xuất thuộc tính (*Attribute Construction* - Slide 73), nhóm không chỉ sử dụng từ vựng mà còn thiết kế thêm 7 thuộc tính định lượng mô tả cấu trúc tin nhắn (Metadata):
1. `num_chars`: Tổng số lượng ký tự trong tin nhắn.
2. `num_words`: Tổng số lượng từ trong tin nhắn.
3. `num_upper`: Số lượng ký tự viết hoa (tin nhắn spam thường viết hoa để gây chú ý như *URGENT, FREE, WINNER*).
4. `num_digits`: Số lượng chữ số xuất hiện (tin nhắn rác thường kèm số điện thoại liên hệ, mã trúng thưởng, số tiền).
5. `num_special`: Số lượng ký tự đặc biệt, dấu câu (`!`, `?`, `@`, `#`).
6. `has_url`: Cờ nhị phân (0 hoặc 1) phát hiện sự xuất hiện của đường dẫn website (`http`, `www.`).
7. `has_money`: Cờ nhị phân (0 hoặc 1) phát hiện ký hiệu tiền tệ (`$`, `£`, `€`).

---

### 1.4. Thống kê mô tả 5 số và nhận diện Outliers
*(Tham chiếu bài giảng: `Data.pptx` - Slide 13–19, 33)*

Áp dụng phương pháp tóm tắt 5 số (*Five-number summary*: Min, Q1, Median, Q3, Max) và độ phân tán của thuộc tính độ dài ký tự (`num_chars`):

**Bảng 1.1: Thống kê mô tả độ dài tin nhắn (ký tự) theo từng nhãn lớp**
| Nhãn lớp | Mean | Median | Mode | Std | Min | Q1 (25%) | Q3 (75%) | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ham** (Bình thường) | 70.9 | 53.0 | 32.0 | 56.6 | 2 | 34.0 | 91.0 | 910 |
| **Spam** (Rác) | 137.7 | 148.0 | 156.0 | 29.8 | 13 | 132.0 | 157.0 | 223 |

**Nhận diện điểm dị biệt (Outlier Detection - Slide 33):**
* Khoảng tứ phân vị trên toàn bộ dữ liệu: $\text{IQR} = Q_3 - Q_1 = 120.0 - 37.0 = 83.0$.
* Ngưỡng biên trên phát hiện Outlier:
  $$\text{Upper Threshold} = Q_3 + 1.5 \times \text{IQR} = 120.0 + 1.5 \times 83.0 = 244.5 \text{ ký tự}$$
* Kết quả: Xác định được **63 tin nhắn** có độ dài vượt ngưỡng 244 ký tự được xem là các điểm dị biệt (phần lớn là các tin nhắn bình thường mang tính chất tâm sự, thư từ dài dòng).

![Thống kê mô tả và phân bố dữ liệu](file:///c:/Users/Administrator/Documents/Workplace/sms_spam_detection/outputs/1_statistics.png)
*Hình 1.1: Trực quan hóa dữ liệu gồm Bar chart phân bố nhãn, Histogram độ dài và Boxplot nhận diện dị biệt*

---

### 1.5. Phân tích tương quan thuộc tính (Correlation Analysis)
*(Tham chiếu bài giảng: `Data.pptx` - Slide 29: Correlation between Two Numerical Variables)*

Nhóm tính toán hệ số tương quan tuyến tính Pearson ($r$) giữa 7 thuộc tính metadata với biến mục tiêu `target` (Spam):

**Bảng 1.2: Hệ số tương quan Pearson giữa Metadata và Nhãn Spam**
| Thuộc tính Metadata | Hệ số tương quan Pearson ($r$) | Mức độ tương quan |
| :--- | :---: | :--- |
| `num_digits` (Số lượng chữ số) | **+0.837** | Rất mạnh |
| `has_money` (Ký hiệu tiền tệ) | **+0.522** | Khá mạnh |
| `num_chars` (Tổng số ký tự) | **+0.381** | Trung bình |
| `has_url` (Chứa link web) | **+0.350** | Trung bình |
| `num_upper` (Số chữ viết hoa) | **+0.320** | Trung bình |
| `num_words` (Tổng số từ) | **+0.284** | Yếu - Trung bình |
| `num_special` (Số ký tự đặc biệt) | **+0.160** | Yếu |

> [!TIP]
> **Kết luận EDA:** Tin nhắn spam có cấu trúc rất khác biệt: dài hơn đáng kể (trung vị 148 ký tự so với 53 ký tự của tin nhắn thường) và đặc biệt chứa mật độ chữ số (`num_digits`, $r=0.837$) và biểu tượng tiền tệ (`has_money`, $r=0.522$) cực kỳ dày đặc.

---

## CHƯƠNG 2: TIỀN XỬ LÝ VĂN BẢN VÀ LỰA CHỌN THUỘC TÍNH
*(Tham chiếu bài giảng: `Data.pptx` - Slide 2, 6, 20, 74, 95–101)*

### 2.1. Quy trình tiền xử lý văn bản (NLP Preprocessing)
Thực hiện nghiêm ngặt theo yêu cầu đề bài gồm 3 bước tuần tự:
1. **Chuẩn hóa chữ thường (Case Folding) & Làm sạch ký tự:** Đưa toàn bộ về chữ thường; dùng biểu thức chính quy `re.sub(r'[^a-z\s]', ' ', text)` để loại bỏ toàn bộ dấu câu và chữ số (do thông tin này đã được trích xuất sang thuộc tính Metadata ở Chương 1).
2. **Tách từ (Tokenization) & Bỏ từ dừng (Stop-word Removal):** Tách câu thành danh sách từ đơn; loại bỏ các từ thông dụng tiếng Anh từ danh mục `ENGLISH_STOP_WORDS` (*a, an, the, is, at, which...*) và các từ có độ dài $\le 1$ ký tự.
3. **Đưa từ về dạng gốc (Stemming):** Sử dụng thuật toán **Porter Stemmer (Martin Porter, 1980)** để cắt bỏ các hậu tố hình thái học (*-ing, -ed, -s, -ly*).
   * *Ví dụ:* Các biến thể `win`, `winner`, `winning`, `wins` đều được quy về một gốc chung là `win`.
   * *Ý nghĩa Khai phá dữ liệu:* Đây là kỹ thuật giảm số lượng chiều thuộc tính ngữ nghĩa, trực tiếp giải quyết vấn đề **"Lời nguyền số chiều" (Curse of Dimensionality - Slide 96)**.

---

### 2.2. Biểu diễn dữ liệu dạng Bag-of-Words và vấn đề Sparsity
Sau bước tiền xử lý, mỗi tin nhắn được biểu diễn dưới dạng một **Véctơ tần suất từ (Term-frequency vector)** trong không gian đa chiều (*Document Data* - Slide 2, 54):
* Tổng số từ vựng duy nhất xuất hiện ít nhất 2 lần: **2.216 từ**.
* **Đặc tính dữ liệu thưa (Sparsity - Slide 6):** Mỗi tin nhắn chỉ dài trung bình 15–25 từ, do đó trong một véctơ có 2.216 phần tử, có tới hơn 99% giá trị là số 0.

---

### 2.3. Lựa chọn thuộc tính bằng kiểm định Chi-Square ($\chi^2$)
*(Tham chiếu bài giảng: `Data.pptx` - Slide 20, 100–101: Attribute Subset Selection)*

Không gian 2.216 từ chứa nhiều từ ngữ xuất hiện ngẫu nhiên không mang thông tin phân biệt. Để tối ưu hóa tốc độ và độ chính xác, nhóm sử dụng phương pháp **Kiểm định Chi-bình-phương ($\chi^2$)**:
$$\chi^2 = \sum_{i=1}^r \sum_{j=1}^c \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$
* $O_{ij}$: Tần số quan sát thực tế của từ ngữ trong từng lớp nhãn.
* $E_{ij}$: Tần số kỳ vọng lý thuyết nếu giả định từ ngữ và nhãn lớp độc lập với nhau.

Giá trị $\chi^2$ càng lớn thể hiện sự xuất hiện của từ ngữ phụ thuộc mạnh mẽ vào nhãn Spam/Ham. Nhóm thiết lập chọn lọc ra **$K = 1.000$ từ có điểm $\chi^2$ cao nhất**.

**Bảng 2.1: Top 15 từ khóa có giá trị $\chi^2$ cao nhất (Dấu hiệu đặc trưng của Spam)**
| Thứ hạng | Từ khóa sau Stemming | Điểm $\chi^2$ | Ý nghĩa thực tế |
| :---: | :---: | :---: | :--- |
| 1 | `free` | 730 | Miễn phí (mồi câu lừa đảo) |
| 2 | `txt` | 639 | Nhắn tin SMS |
| 3 | `mobil` | 523 | Thiết bị di động |
| 4 | `claim` | 429 | Nhận thưởng / Yêu cầu nhận giải |
| 5 | `prize` | 415 | Giải thưởng |
| 6 | `www` | 407 | Tên miền liên kết lừa đảo |
| 7 | `tone` | 353 | Nhạc chuông dịch vụ |
| 8 | `repli` | 335 | Phản hồi tin nhắn |
| 9 | `text` | 305 | Soạn tin nhắn |
| 10 | `stop` | 305 | Cú pháp dừng dịch vụ tính phí |
| 11 | `uk` | 296 | Mã vùng quốc gia Anh |
| 12 | `servic` | 288 | Dịch vụ giá trị gia tăng |
| 13 | `cash` | 265 | Tiền mặt trúng thưởng |
| 14 | `nokia` | 263 | Thương hiệu điện thoại khuyến mãi |
| 15 | `award` | 220 | Trao tặng giải thưởng |

---

### 2.4. Chuẩn hóa thang đo (Min-Max Normalization)
*(Tham chiếu bài giảng: `Data.pptx` - Slide 74)*

Các thuộc tính Metadata có đơn vị đo rất khác nhau (độ dài lên tới vài trăm ký tự, trong khi các thuộc tính cờ chỉ có giá trị 0 hoặc 1). Để tránh việc các thuộc tính có thang đo lớn lấn át các thuộc tính khác, nhóm áp dụng **Chuẩn hóa Min-Max** để co dãn về đoạn $[0, 1]$:
$$v' = \frac{v - \min_A}{\max_A - \min_A} \times (new\_max_A - new\_min_A) + new\_min_A$$

Sau đó, ma trận từ vựng ($1.000$ chiều) và ma trận Metadata đã chuẩn hóa ($7$ chiều) được ghép lại thành không gian đặc trưng thống nhất gồm **1.007 chiều**.

---

## CHƯƠNG 3: CƠ SỞ PHƯƠNG PHÁP VÀ MÔ HÌNH PHÂN LỚP
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 8–50)*

Nhóm thực nghiệm 3 thuật toán phân lớp tiêu biểu đại diện cho 3 trường phái học máy khác nhau:

### 3.1. Thuật toán Naïve Bayes và Kỹ thuật làm mịn Laplace
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 20–31)*

* **Nguyên lý toán học:** Áp dụng định lý xác suất Bayes với giả định "ngây thơ" (*Naïve assumption*) rằng các thuộc tính $x_1, x_2, \dots, x_n$ độc lập có điều kiện khi biết trước nhãn lớp $C$:
  $$P(C \mid X) = \frac{P(X \mid C) P(C)}{P(X)} \propto P(C) \prod_{i=1}^n P(x_i \mid C)$$
  Quyết định phân lớp bằng cách tìm nhãn có xác suất hậu nghiệm cực đại:
  $$C^* = \arg\max_{C \in \{\text{ham, spam}\}} \left[ \log P(C) + \sum_{i=1}^n \log P(x_i \mid C) \right]$$
* **Khắc phục vấn đề xác suất 0 bằng Kỹ thuật làm mịn Laplace (Laplacian Correction - Slide 29):**
  Nếu một từ $x_i$ chưa từng xuất hiện trong tập huấn luyện của lớp $C$, xác suất $P(x_i \mid C) = 0$ sẽ làm triệt tiêu toàn bộ tích xác suất. Giải pháp là cộng thêm tham số làm mịn $\alpha = 1.0$:
  $$\hat{P}(x_i \mid C) = \frac{\text{count}(x_i, C) + 1}{\sum_{w} \text{count}(w, C) + |V|}$$
  Trong đó $|V|$ là kích thước không gian từ vựng ($|V| = 1.000$).

---

### 3.2. Thuật toán Linear Support Vector Machine (Linear SVM)
*(Tham chiếu bài giảng: Giáo trình Jiawei Han - Chương 9, Mục 9.3)*

* **Nguyên lý hình học:** Biểu diễn mỗi tin nhắn thành một điểm trong không gian $d = 1.007$ chiều. SVM tìm một siêu phẳng phân tách tối ưu:
  $$\mathbf{w}^T \mathbf{x} + b = 0$$
  sao cho khoảng cách lề (*Margin*) giữa siêu phẳng tới các điểm dữ liệu gần nhất của hai phe (gọi là các **Véctơ hỗ trợ - Support Vectors**) đạt cực đại:
  $$\max_{\mathbf{w}, b} \frac{2}{\|\mathbf{w}\|} \iff \min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^N \xi_i$$
  với ràng buộc: $y_i(\mathbf{w}^T \mathbf{x}_i + b) \ge 1 - \xi_i$ ($\xi_i \ge 0$ là biến bù trừ sai số).
* **Ưu điểm trên văn bản:** Dữ liệu văn bản có số chiều lớn và thưa, phần lớn các lớp đã phân tách tuyến tính tốt trong không gian đa chiều, do đó nhân tuyến tính (*Linear Kernel*) chạy rất nhanh và kiểm soát quá khớp cực tốt.

---

### 3.3. Thuật toán Cây quyết định (Decision Tree Induction)
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 8–18)*

* **Giải thuật:** Xây dựng cây phân nhánh theo giải thuật tham lam đệ quy từ trên xuống (*Top-down, divide-and-conquer*).
* **Tiêu chuẩn chọn thuộc tính phân nhánh: Entropy & Độ lợi thông tin (Information Gain - Slide 14–15):**
  * Độ hỗn loạn thông tin ban đầu của tập dữ liệu $D$:
    $$\text{Info}(D) = - \sum_{i=1}^m p_i \log_2(p_i)$$
  * Lượng thông tin kỳ vọng cần thiết sau khi phân tách theo thuộc tính $A$:
    $$\text{Info}_A(D) = \sum_{j=1}^v \frac{|D_j|}{|D|} \times \text{Info}(D_j)$$
  * Độ lợi thông tin thu được: $\text{Gain}(A) = \text{Info}(D) - \text{Info}_A(D)$.
  Thuộc tính nào có $\text{Gain}(A)$ lớn nhất sẽ được chọn làm nút phân nhánh tại mỗi bước.
* **Kiểm soát quá khớp:** Cây quyết định rất dễ bị quá khớp trên dữ liệu văn bản thưa. Nhóm khống chế độ sâu tối đa `max_depth = 15`.

---

### 3.4. Phương pháp phân chia dữ liệu thẩm định
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 60–61)*

Để đảm bảo tính khách quan khoa học, nhóm sử dụng 2 phương pháp thẩm định:
1. **Phương pháp Holdout phân tầng (Stratified Holdout):** Chia tập dữ liệu 5.171 dòng theo tỷ lệ chuẩn bài giảng: **2/3 tập huấn luyện (3.447 mẫu)** và **1/3 tập kiểm thử độc lập (1.724 mẫu)**. Kết hợp lấy mẫu phân tầng (*Stratified Sampling* - `Data.pptx` Slide 87) để đảm bảo cả hai tập đều giữ nguyên tỷ lệ 87.4% Ham / 12.6% Spam.
2. **Phương pháp kiểm định chéo phân tầng (Stratified 10-Fold Cross-Validation):** Chia dữ liệu làm 10 phần bằng nhau có cùng tỷ lệ nhãn, luân phiên dùng 9 phần để học và 1 phần để kiểm tra. Kết quả báo cáo dưới dạng $\text{Mean} \pm \text{Std}$.

---

## CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH SO SÁNH
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 52–62)*

### 4.1. Hệ thống chỉ số đánh giá (Evaluation Metrics)
Dựa trên ma trận nhầm lẫn (Confusion Matrix - Slide 53):

**Bảng 4.1: Cấu trúc Ma trận nhầm lẫn cho bài toán Lọc tin nhắn rác**
| Thực tế \ Dự đoán | Dự đoán là Ham (Âm tính) | Dự đoán là Spam (Dương tính) |
| :--- | :---: | :---: |
| **Thực tế là Ham** | $TN$ (True Negative - Đoán đúng tin thường) | $FP$ (False Positive - **Chặn nhầm tin thường thành rác**) |
| **Thực tế là Spam** | $FN$ (False Negative - **Lọt tin rác vào hộp thư đến**) | $TP$ (True Positive - Bắt đúng tin rác) |

Các công thức chỉ số chuẩn xác:
* **Accuracy:** $\frac{TP + TN}{All}$ *(Tỷ lệ dự đoán đúng tổng thể)*.
* **Error Rate:** $\frac{FP + FN}{All} = 1 - \text{Accuracy}$ *(Tỷ lệ dự đoán sai)*.
* **Sensitivity (Recall của Spam):** $\frac{TP}{TP + FN}$ *(Khả năng bắt trọn vẹn tin rác)*.
* **Specificity (Độ đặc hiệu của Ham):** $\frac{TN}{TN + FP}$ *(Khả năng bảo toàn tin thường)*.
* **Precision của Spam:** $\frac{TP}{TP + FP}$ *(Mức độ tin cậy khi gắn cờ Spam)*.
* **F1-Score:** $\frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ *(Trung bình điều hòa giữa Precision và Recall)*.
* **AUC (Area Under Curve):** Diện tích dưới đường cong ROC đo lường năng lực phân loại tổng quát.

> [!IMPORTANT]
> **Biện luận chuyên sâu về bài toán thực tế:**
> Trong bài toán lọc Spam, **sai lầm loại I (False Positive - $FP$) tai hại hơn rất nhiều so với sai lầm loại II (False Negative - $FN$)**. Nếu một tin nhắn chứa mã OTP ngân hàng hoặc thư mời phỏng vấn bị dán nhãn nhầm là Spam và chuyển vào sọt rác, người dùng có thể chịu thiệt hại nghiêm trọng. Do đó, tiêu chí tối thượng để chọn mô hình là **Precision của lớp Spam phải đạt mức tối đa (càng gần 100% càng tốt)**, chấp nhận đánh đổi một lượng nhỏ $FN$ (để lọt một vài tin rác).

---

### 4.2. Kết quả phân loại trên tập kiểm thử (Holdout 2/3 - 1/3)
Kiểm thử trên 1.724 mẫu độc lập (gồm 1.506 tin Ham và 218 tin Spam):

**Bảng 4.2: Bảng tổng hợp kết quả thẩm định Holdout (Test 1/3 dữ liệu)**
| Mô hình | Accuracy | Error Rate | Sensitivity (Recall) | Specificity | Precision (Spam) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Naive Bayes** | 0.9849 | 0.0151 | **0.9450** | 0.9907 | 0.9364 | 0.9406 | 0.9911 |
| **Linear SVM** | **0.9855** | **0.0145** | 0.9174 | **0.9954** | **0.9662** | **0.9412** | **0.9929** |
| **Decision Tree** | 0.9768 | 0.0232 | 0.9220 | 0.9847 | 0.8973 | 0.9095 | 0.9512 |

![Ma trận nhầm lẫn](file:///c:/Users/Administrator/Documents/Workplace/sms_spam_detection/outputs/3_confusion_matrices.png)
*Hình 4.1: Ma trận nhầm lẫn của 3 mô hình trên tập kiểm thử 1.724 mẫu*

![Đường cong ROC](file:///c:/Users/Administrator/Documents/Workplace/sms_spam_detection/outputs/4_roc_curves.png)
*Hình 4.2: So sánh đường cong ROC và diện tích AUC của 3 mô hình*

**Phân tích kết quả chi tiết:**
* **Linear SVM là mô hình xuất sắc nhất:** Đạt Precision lên tới **0.9662** (chỉ có 7 tin nhắn thường bị chặn nhầm trên tổng số 1.506 tin Ham). Điểm AUC đạt **0.9929**, đường cong ROC tiệm cận góc trên bên trái hoàn hảo.
* **Naive Bayes đạt Recall cao nhất (0.9450):** Bắt được 206/218 tin rác, tuy nhiên số lượng tin thường bị chặn nhầm cao hơn SVM ($FP = 14$ so với $FP = 7$).
* **Decision Tree có hiệu năng thấp nhất:** Precision dưới 90% ($0.8973$, có tới 23 tin thường bị dán nhãn nhầm) và AUC chỉ đạt $0.9512$ do bản chất phân chia ngưỡng bậc thang của cây quyết định.

---

### 4.3. Kết quả thẩm định chéo Stratified 10-Fold Cross-Validation
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 61)*

Để chứng minh kết quả không phải do ngẫu nhiên khi chia dữ liệu, nhóm chạy kiểm định chéo 10 lần trên toàn bộ tập dữ liệu:

**Bảng 4.3: Kết quả thẩm định chéo 10-Fold Cross-Validation (Mean ± Std)**
| Mô hình | Accuracy | Precision (Spam) | Recall (Spam) | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **Naive Bayes** | $0.9818 \pm 0.0054$ | $0.9259 \pm 0.0250$ | $\mathbf{0.9312 \pm 0.0313}$ | $0.9282 \pm 0.0216$ |
| **Linear SVM** | $\mathbf{0.9867 \pm 0.0036}$ | $\mathbf{0.9776 \pm 0.0175}$ | $0.9159 \pm 0.0264$ | $\mathbf{0.9454 \pm 0.0148}$ |
| **Decision Tree** | $0.9764 \pm 0.0065$ | $0.9185 \pm 0.0421$ | $0.8944 \pm 0.0227$ | $0.9058 \pm 0.0248$ |

Bảng số liệu kiểm định chéo khẳng định tính ổn định cao của **Linear SVM** với độ lệch chuẩn cực kỳ nhỏ ($\pm 0.0036$) và Precision trung bình lên tới **97.76%**.

---

### 4.4. Thí nghiệm thực chứng 1: Vai trò của làm mịn Laplace
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 29: Avoiding the Zero-Probability Problem)*

Nhóm tiến hành thực nghiệm đối đầu trên mô hình Naïve Bayes:
* **Trường hợp 1 ($\alpha = 10^{-10} \approx 0$ - Không làm mịn):** Các từ mới xuất hiện trong tập kiểm thử làm triệt tiêu xác suất thành phần. Kết quả: $\text{Precision} = 0.9174$, $\text{Recall} = 0.9174$, $\text{F1} = 0.9174$.
* **Trường hợp 2 ($\alpha = 1.0$ - Có làm mịn Laplace):** Điểm số tăng vọt toàn diện: $\text{Precision} = \mathbf{0.9364}$, $\text{Recall} = \mathbf{0.9450}$, $\text{F1} = \mathbf{0.9406}$.
* **Kết luận thực nghiệm:** Thực nghiệm đã chứng minh trực quan lý thuyết tại Slide 29: Làm mịn Laplace đóng vai trò sống còn giúp Naïve Bayes thích nghi với các từ vựng mới chưa từng gặp trong tập huấn luyện.

---

### 4.5. Thí nghiệm thực chứng 2: Hiện tượng quá khớp (Overfitting) trên Cây quyết định
*(Tham chiếu bài giảng: `Classification.pptx` - Slide 13 & Slide 59: Training Error vs. Testing Error)*

Nhóm khảo sát tỷ lệ lỗi trên tập huấn luyện (*Training Error*) và tập kiểm thử (*Testing Error*) khi thay đổi độ sâu cây `max_depth` từ $1$ đến $\infty$:

**Bảng 4.4: Sự biến thiên của Training Error và Testing Error theo độ sâu cây**
| Độ sâu `max_depth` | Tỷ lệ lỗi tập Train (Training Error) | Tỷ lệ lỗi tập Test (Testing Error) | Hiện tượng |
| :---: | :---: | :---: | :--- |
| 1 | 0.0249 (2.49%) | 0.0284 (2.84%) | Dưới khớp (Underfitting) |
| 2 | 0.0249 (2.49%) | 0.0284 (2.84%) | Dưới khớp (Underfitting) |
| 3 | 0.0215 (2.15%) | 0.0232 (2.32%) | Bắt đầu học tốt |
| **5** | **0.0099 (0.99%)** | **0.0174 (1.74%)** | **Điểm tối ưu (Best Generalization)** |
| 8 | 0.0041 (0.41%) | 0.0232 (2.32%) | Chớm quá khớp |
| 12 | 0.0015 (0.15%) | 0.0238 (2.38%) | Quá khớp tăng |
| 15 | 0.0009 (0.09%) | 0.0232 (2.32%) | Quá khớp |
| **$\ge 20 \rightarrow \infty$** | **0.0000 (0.00%)** | **0.0284 (2.84%)** | **Quá khớp cực đoan (Overfitting)** |

![Hiện tượng quá khớp](file:///c:/Users/Administrator/Documents/Workplace/sms_spam_detection/outputs/5_tree_overfitting.png)
*Hình 4.3: Đồ thị hình chữ U minh họa trực quan hiện tượng Quá khớp (Overfitting) khớp hoàn toàn với Slide 59*

> [!NOTE]
> **Giải thích đồ thị Slide 59:**
> Khi $\text{max\_depth} \ge 20$, cây quyết định tạo ra hàng trăm nhánh lá nhỏ li ti để phân loại đúng 100% mẫu trong tập huấn luyện ($\text{Training Error} = 0.0000$). Tuy nhiên, cây đã "học vẹt" cả các đặc trưng nhiễu ngẫu nhiên, khiến sai số khi gặp dữ liệu mới trong tập kiểm thử bị dội ngược lên $2.84\%$. Điều này chứng minh sự cần thiết của việc cắt tỉa cây hoặc khống chế độ sâu tối đa.

---

### 4.6. Thử nghiệm Demo dự đoán tin nhắn thực tế
Mô hình hoàn chỉnh (sử dụng Linear SVM làm lõi phân loại) được chạy thử nghiệm trên các tình huống giả lập thực tế:

1. **Tin nhắn 1:** *"Hey, are we still meeting for lunch today?"*
   * *Dự đoán:* **[ HAM ]** (Chính xác - Tin nhắn cá nhân thông thường).
2. **Tin nhắn 2:** *"CONGRATULATIONS! You won a $1000 Walmart gift card. Call 09061701461 now to claim your prize!"*
   * *Dự đoán:* **[ SPAM ]** (Chính xác - Phát hiện từ khóa *congratulation, won, gift card, call, claim, prize* và ký hiệu tiền tệ `$`).
3. **Tin nhắn 3:** *"Can you send me the slides from yesterday lecture?"*
   * *Dự đoán:* **[ HAM ]** (Chính xác - Tin nhắn học tập).
4. **Tin nhắn 4:** *"URGENT! Your mobile account has been suspended. Please text YES to 88088 to verify."*
   * *Dự đoán:* **[ SPAM ]** (Chính xác - Phát hiện cú pháp khẩn cấp giả mạo viễn thông).

---

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 1. Kết luận đạt được
1. Đã triển khai hoàn chỉnh quy trình Khai phá dữ liệu (KDD) theo đúng chuẩn học phần của Học viện: từ làm sạch dữ liệu, xây dựng và chọn lọc thuộc tính ($\chi^2$), đến tiền xử lý ngôn ngữ tự nhiên (NLP) với thuật toán Porter Stemmer.
2. Đã cài đặt, đánh giá và so sánh thực nghiệm 3 thuật toán phân lớp kinh điển (*Naïve Bayes, Linear SVM, Decision Tree*) thông qua hai phương pháp thẩm định chặt chẽ: Holdout (2/3 - 1/3) và 10-Fold Cross-Validation.
3. **Chọn lựa giải pháp:** **Linear Support Vector Machine (Linear SVM)** được lựa chọn là mô hình tối ưu nhất để triển khai trong thực tế nhờ đạt độ chuẩn xác (Precision) vượt trội **96.62%** (Holdout) và **97.76%** (10-Fold CV), giúp triệt tiêu gần như hoàn toàn nguy cơ chặn nhầm tin nhắn quan trọng của người dùng.
4. Đã thực hiện 2 thí nghiệm chuyên sâu minh chứng bằng số liệu thực nghiệm cho 2 nội dung lý thuyết cốt lõi trong slide: **Kỹ thuật làm mịn Laplace** và **Hiện tượng quá khớp (Overfitting) trên Cây quyết định**.

### 2. Hạn chế và Hướng phát triển
* **Hạn chế:** Tập dữ liệu nghiên cứu sử dụng ngôn ngữ tiếng Anh; chưa tích hợp cơ chế phân tích ngữ cảnh sâu giữa các cụm từ (N-gram bậc cao hoặc Transformer).
* **Hướng phát triển:**
  1. Mở rộng hệ thống để nhận diện tin nhắn rác tiếng Việt (sử dụng bộ tách từ `pyvi` hoặc `VnCoreNLP`).
  2. Triển khai mô hình thành một API dịch vụ nhẹ bằng FastAPI/Flask để tích hợp trực tiếp vào ứng dụng viễn thông thời gian thực.
  3. Thử nghiệm kết hợp các phương pháp học tăng cường nhóm (Ensemble Methods như Random Forest, XGBoost - Slide 64–75) trên các tập dữ liệu rác đa biến thể phức tạp hơn.

---

## TÀI LIỆU THAM KHẢO

1. **Jiawei Han, Micheline Kamber, Jian Pei (2011).** *Data Mining: Concepts and Techniques (3rd Edition)*, Morgan Kaufmann Publishers.
   * Chương 2: Getting to Know Your Data (Trang 39–82).
   * Chương 3: Data Preprocessing (Trang 83–124).
   * Chương 8: Classification: Basic Concepts (Trang 327–392).
   * Chương 9: Classification: Advanced Methods (Trang 393–442).
2. **Bộ môn Khoa học Máy tính / Hệ thống Thông tin - PTIT.** *Bài giảng điện tử môn Khai phá dữ liệu*:
   * `Data.pptx`: Chapter 2 - Data, Measurements, and Data Preprocessing.
   * `Classification.pptx`: Chapter 6 - Classification: Basic Concepts.
3. **UCI Machine Learning Repository.** *SMS Spam Collection Data Set (Almeida, T.A., Hidalgo, J.M.G., Yamakami, A., 2012)*.
4. **Porter, M. F. (1980).** *An algorithm for suffix stripping*, Program, 14(3), 130–137.
5. **Scikit-learn Documentation.** *Machine Learning in Python*, [https://scikit-learn.org/](https://scikit-learn.org/).
