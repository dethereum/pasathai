from pythainlp import word_tokenize
from pythainlp.transliterate import transliterate

test_data="โรงหนัง"

data = ["มา", "ไก่", "ได้", "นับ", "ฉัน"]
engines = [
    "tltk_ipa",
    "tltk_g2p",
]


def my_function():
    for engine in engines:
        print("Using {}\n".format(engine))

        for d in data:
            print(transliterate(d, engine=engine))

        print("\n")