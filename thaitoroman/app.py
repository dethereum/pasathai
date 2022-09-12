from pythainlp import word_tokenize
from pythainlp.transliterate import transliterate

test_data="โรงหนัง"

data = ["มา", "ไก่", "ได้", "นับ", "ฉัน"]
engines = [
#    "icu",
    "ipa",
    "thaig2p",
    "tltk_ipa",
    "tltk_g2p",
    "iso_11940"
]


def my_function():
    for engine in engines:
        print("Using {}".format(engine))

        for d in data:
            print(transliterate(d, engine=engine))

