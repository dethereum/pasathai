import re

from pythainlp.tokenize import word_tokenize, syllable_tokenize, tcc
from pythainlp.transliterate import transliterate

test_data="กรุงเทพเป็นเมืองหลวงของประเทศไทย"

data = ["มา", "ไก่", "ได้", "นับ", "ฉัน"]
engines = [
    "tltk_ipa",
    "tltk_g2p",
]

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def get_last_index(word):
    return len(word) - 1 

def print_tones():
    for engine in engines:
        print("Using {}\n".format(engine))

        for d in data:
            print(transliterate(d, engine=engine))

    print("\n")


def my_function():
    words = word_tokenize(test_data)

    info_store = []
    for word in words:
        syllables = syllable_tokenize(word)

        tones = []
        tone_indexes = []

        for syllable in syllables:
            tone_indexes.append(word.find(syllable))
            tones.append(re.sub("[^1-5]", "", transliterate(syllable, engine="tltk_ipa")))
        
        info_store.append((tones, tone_indexes, word))

    print(words)
    print("\n")

    for index, data in enumerate(info_store):
        (tones, brk, word) = data
        print(tones)
        print(brk)
        print(word + " " + str(get_last_index(word)))
        print("\n")
            # print(get_color_escape(r, g, b, background=False) + tonei[0])