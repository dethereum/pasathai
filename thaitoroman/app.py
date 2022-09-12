from pythainlp import word_tokenize
from pythainlp.transliterate import transliterate

test_data="โรงหนัง"

data = ["มา", "ไก่", "ได้", "นับ", "ฉัน"]

def my_function():
    print(word_tokenize(test_data))

    print(transliterate(test_data, engine="iso_11940"))

    for d in data:
        print(transliterate(d, engine="icu"))

