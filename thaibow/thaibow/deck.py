from thaibow.app import my_function, get_color_escape
from rich.console import Console
from rich.table import Table

import json
import requests
import shortuuid

from thaibow.validator import api_external_validator

# engines for tokenization that work locally
engines = [
    "newmm",  # fastest tokenizer
    # "newmm-safe",
    # "longest",
    # "attacut",
    # "nercut",
    # "tltk",
]

tag_prefix = "pasathai::meta::"

url = 'https://www.thai2english.com/_next/data/qqerWs1vgtpJGScVYNO0N/index.json'


def init_phrase_note(example, meaning):
    return {
        "__type__" : "Note",
        "fields" : [example.word, meaning.word, meaning.meaning, "", "", example.meaning],
        "guid" : shortuuid.uuid()[:10],
        "note_model_uuid" : "945aebac-33ec-11ed-8670-f7b6016c17e6",
        "tags" : []
    }

# EXAMPLE
#
# 3 and 4 are audio files to be inputed manually
#
# 0 ไม่มีปัญหา           phrase
# 1 ปัญหา              target
# 2 problem           target meaning
# 5 no have problem   phrase meaning
def make_phrase_notes(meaning):
    phrase_notes = []
    
    # make decision to use at most 2 examples of every meaning
    for example in meaning.examples[:2]:
        note = init_phrase_note(example, meaning)

        if example.etymology != "":
            note["tags"].append(tag_prefix + "etymology::" + example.etymology.lower())
        
        for pos in meaning.partOfSpeech:
            note["tags"].append(tag_prefix + "part_of_speech::" + pos.lower())

        if len(meaning.components) > 1:
            note["tags"].append(tag_prefix + "component_word")

        note["tags"].append(tag_prefix + "processed")

        note["tags"] = sorted(unique(note["tags"]), key=str.lower)
        phrase_notes.append(note)

    return phrase_notes


def unique(list1):
    unique_list = []

    for x in list1:
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


def handle_repeater(text):
    if "ๆ" in text:
        return text.replace("ๆ", text.replace("ๆ", ""))
    return text


def display_thaibow(notes):
    for note in notes:
        text = note['fields'][0]

        table = Table(title=text)
        columns = ["Transliteration", "Output"]

        for column in columns:
            table.add_column(column)

        for engine in engines:
            (output, roman_text) = my_function(handle_repeater(text), engine)
            row = [roman_text, output]
            table.add_row(*row, style='bright_green')

        console = Console()
        console.print(table)


def fetch_thai_word_data(notes):
    for note in notes:
        text = note['fields'][0]

        data = requests.get(url, params={'q': text})
        props = json.loads(data.content)['pageProps']['processed']

        with open('./thaibow/data/' + text + '.json', 'a') as out_file:
            json.dump(props, out_file, sort_keys=True,
                      indent=4, ensure_ascii=False)

# ensure no translation type or multiple meaning words become vocab cards


def get_notes_data():
    json_file = open('../deck.json')
    anki = json.load(json_file)

    # hard code vocab deck path
    notes = anki['children'][2]["notes"]

    for note in notes:
        if tag_prefix + "processed" in note["tags"]:
            print(note['fields'][0], "already processed")
            continue

        text = note['fields'][0]

        with open('./thaibow/data/' + text + '.json') as data_file:
            raw_data = json.load(data_file)

            thai_word_data = api_external_validator(raw_data, text)

            amt_meanings = len(thai_word_data.firestoreWord.meanings)

            note["tags"].append(tag_prefix + "usage::" +
                                thai_word_data.commonessText.replace(" ", "_").lower())

            if amt_meanings > 1:
                note["tags"].append(tag_prefix + "multiple_meanings")

                for meaning in thai_word_data.firestoreWord.meanings:
                    if len(meaning.examples) > 0: 
                        phrase_notes = make_phrase_notes(meaning)

                        for phrase_note in phrase_notes:
                            anki['children'][1]["notes"].append(phrase_note)
            else:
                meaning = thai_word_data.firestoreWord.meanings[0]

                if len(meaning.components) > 1:
                    note["tags"].append(tag_prefix + "component_word")
                if meaning.etymology != "":
                    note["tags"].append(
                        tag_prefix + "etymology::" + meaning.etymology.lower())

                for pos in meaning.partOfSpeech:
                    note["tags"].append(
                        tag_prefix + "part_of_speech::" + pos.lower())

        note["tags"].append(tag_prefix + "processed")
        note["tags"] = sorted(unique(note["tags"]), key=str.lower)

    anki['children'][2]["notes"] = notes

    json_out = open('../deck.json', 'w')
    json_out.write(json.dumps(anki, indent=4, ensure_ascii=False))

    json_file.close()
    json_out.close()
