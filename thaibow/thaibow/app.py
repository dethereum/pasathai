import re
import functools

from pythainlp.tokenize import word_tokenize, syllable_tokenize, tcc
from pythainlp.transliterate import transliterate

from pythainlp.util import normalize

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
        print(f"{sub} not found in the given string {str}")

def get_last_index(word):
    return len(word) - 1

def handle_silent_marker(syllable):
    if " " in syllable:
        return syllable.split(" ")[0]

    return syllable

def handle_linking_syllable(roman_syllable, syllable, tones, roman_syllables, final_word, tone_indexes, cur_syllable_indexs):
    (lt_in, rt_in) = cur_syllable_indexs

    first_pos = 0
    no_hit = True
    for pos in tcc.tcc_pos(syllable):
        if no_hit == True:
            first_pos = pos
            no_hit = False
    
    lt_th = syllable[:first_pos]
    rt_th = syllable[first_pos:]

    for hidden_syllable in roman_syllable.split("."):
        roman_syllables.append(hidden_syllable)
        syllable_tone = re.sub("[^1-5]", "", hidden_syllable)
        tones.append(syllable_tone)

    final_word.append(lt_th)
    final_word.append(rt_th)

    tone_indexes.append((lt_in, first_pos))
    tone_indexes.append((first_pos, rt_in))


def get_tone_store(text, engine):
    words = word_tokenize(text, engine=engine)

    info_store = []
    for word in words:

        syllables = syllable_tokenize(word)

        tones = []
        tone_indexes = []
        roman_syllables = []
        final_word_parts = []

        for syllable in syllables:
            syllable_indexs = get_indexes_of_sub(word, syllable)
            
            if "์" in syllable: 
                roman_syllable = handle_silent_marker(transliterate(syllable, engine="tltk_ipa"))
                syllable_tone = re.sub("[^1-5]", "", roman_syllable)
                tones.append(syllable_tone)
                roman_syllables.append(roman_syllable)
                final_word_parts.append(syllable)
                tone_indexes.append(syllable_indexs)
            else:
                roman_syllable = transliterate(syllable, engine="tltk_ipa")
                if "." in roman_syllable:
                    handle_linking_syllable(roman_syllable, syllable, tones, roman_syllables, final_word_parts, tone_indexes, syllable_indexs)
                else:
                    syllable_tone = re.sub("[^1-5]", "", roman_syllable)
                    tones.append(syllable_tone)
                    roman_syllables.append(roman_syllable)
                    final_word_parts.append(syllable)
                    tone_indexes.append(syllable_indexs)

        final_word = functools.reduce(lambda a,b : a + '' + b, final_word_parts)

        info_store.append((tones, tone_indexes, final_word, roman_syllables))
    return info_store

def my_function(text, engine):
    info = get_tone_store(text, engine)

    colored_words = []
    roman_words = []
    for tones, splits, word, roman_syllables in info:
        colored_syllables = []
        for i in range(len(tones)):
            (lt, ri) = splits[i]
            (r, g, b) = tone_dict[tones[i]]

            color = get_color_escape(r, g, b, background=False) 
            colored_syllables.append(color + word[lt:ri])

        colored_words.append(functools.reduce(lambda a,b : a + '' + b, colored_syllables))
        roman_words.append(functools.reduce(lambda a,b : a + '' + b, roman_syllables))
    final_colored = functools.reduce(lambda a,b : a + '' + b, colored_words)
    roman_text = functools.reduce(lambda a,b : a + '' + b, roman_words)

    return (final_colored, roman_text)


