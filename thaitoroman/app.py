import re

from pythainlp.tokenize import word_tokenize, syllable_tokenize, tcc
from pythainlp.transliterate import transliterate

test_data="กรุงเทพเป็นเมืองหลวงของประเทศไทย"

tone_dict = {
    '1': (125, 125, 125),
    '2': (230, 138, 0),
    '3': (0, 128, 43),
    '4': (0, 92, 230),
    '5': (230, 0, 0)
}

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def get_last_index(word):
    return len(word) - 1 

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

    for tones, brk, word in info_store:
        print(get_color_escape(255, 255, 255, background=True))
        for tone in tones:
            print(get_color_escape(0, 0, 0, background=True) + get_color_escape(255, 255, 255, background=False))

            (r, g, b) = tone_dict[tone]
            colored_word = get_color_escape(r, g, b, background=False) + word
            print(tones, brk, word, str(get_last_index(word)), "\t", colored_word)