import nltk
from nltk.stem import PorterStemmer, SnowballStemmer

# Khởi tạo Porter Stemmer
porter = PorterStemmer()

# Ví dụ các từ cần rút gọn
words = ["running", "mobile", "ran", "tensed", "service"]

print("--- Porter Stemmer ---")
for word in words:
    print(f"{word} -> {porter.stem(word)}")

# Khởi tạo Snowball Stemmer (hỗ trợ nhiều ngôn ngữ hơn, ví dụ 'english')
snowball = SnowballStemmer("english")

print("\n--- Snowball Stemmer ---")
for word in words:
    print(f"{word} -> {snowball.stem(word)}")