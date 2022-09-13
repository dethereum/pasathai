import re
import functools

from pythainlp.tokenize import word_tokenize, syllable_tokenize, tcc
from pythainlp.transliterate import transliterate

test_data="กรุงเทพเป็นเมืองหลวงของประเทศไทย"

# https://convertingcolors.com/list/avery.html
tone_dict = {
    '1': (125, 132, 132), # Gray
    '2': (233, 149, 0), # Chrome Yellow
    '3': (0, 130, 75), # Green
    '4': (0, 100, 172), # Scuba Blue
    '5': (195, 14, 5) # Spicy Red
}

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def get_indexes_of_sub(str, sub):
    if str.find(sub) != -1:
        start_index = str.find(sub)
        last_index = start_index + len(sub)
        return (start_index, last_index)
    else:
        print(f"{sub} not found in the given string")

def get_last_index(word):
    return len(word) - 1

def get_tone_store(text):
    words = word_tokenize(text)

    info_store = []
    for word in words:
        syllables = syllable_tokenize(word)

        tones = []
        tone_indexes = []

        for syllable in syllables:
            syllable_indexs = get_indexes_of_sub(word, syllable)
            syllable_tone = re.sub("[^1-5]", "", transliterate(syllable, engine="tltk_ipa"))

            tone_indexes.append(syllable_indexs)
            tones.append(syllable_tone)

        info_store.append((tones, tone_indexes, word))
    return info_store

def my_function(text):
    info = get_tone_store(text)

    colored_words = []
    for tones, splits, word in info:
        colored_syllables = []
        for i in range(len(tones)):
            (lt, ri) = splits[i]
            (r, g, b) = tone_dict[tones[i]]

            color = get_color_escape(r, g, b, background=False) 
            colored_syllables.append(color + word[lt:ri])

        colored_words.append(functools.reduce(lambda a,b : a + '' + b, colored_syllables))
    final_colored = functools.reduce(lambda a,b : a + '' + b, colored_words)

    return final_colored


