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

def get_last_index(word):
    return len(word) - 1 

def my_function():
    print(test_data)
    words = word_tokenize(test_data)

    info_store = []
    for word in words:
        syllables = syllable_tokenize(word)

        tones = []
        tone_indexes = []

        for syllable in syllables:
            tone_indexes.append(word.find(syllable))
            tones.append(re.sub("[^1-5]", "", transliterate(syllable, engine="tltk_ipa")))

        del tone_indexes[0]
        tone_indexes.append(get_last_index(word))

        info_store.append((tones, tone_indexes, word))

    
    colored_words = []
    for tones, brk, word in info_store:
        colored_syllable = []
        for i in range(len(tones)):
            tone = tones[i]
            ti = brk[i]

            (r, g, b) = tone_dict[tone]
            color = get_color_escape(r, g, b, background=False) 

            if len(tones) == 2:
                ib = brk[i]
                if i == 0:
                    colored_syllable.append(color + word[0:ib])
                else:
                    colored_syllable.append(color + word[brk[0]:ib+1])
            else:
                colored_syllable.append(color + word)
        colored_words.append(functools.reduce(lambda a,b : a + '' + b, colored_syllable))
    final_colored = functools.reduce(lambda a,b : a + '' + b, colored_words)

    print(final_colored)


        
