from thaibow.app import my_function, get_color_escape
from rich.console import Console
from rich.table import Table

import json
import requests

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

url = 'https://www.thai2english.com/_next/data/qqerWs1vgtpJGScVYNO0N/index.json'

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
        if "pasathai::processed" in note["tags"]:
            continue

        text = note['fields'][0]

        with open('./thaibow/data/' + text + '.json') as data_file:
            raw_data = json.load(data_file)

            thai_word_data = api_external_validator(raw_data, text)

            amt_meanings = len(thai_word_data.firestoreWord.meanings)

            note["tags"].append("pasathai::meta::usage::" + thai_word_data.commonessText.replace(" ", "_").lower())

            if amt_meanings > 1:
                note["tags"].append("pasathai::meta::multiple_meanings")

                for meaning in thai_word_data.firestoreWord.meanings:
                    if len(meaning.components) > 1:
                        note["tags"].append("pasathai::meta::component_word")
                    if meaning.etymology != "":
                        note["tags"].append("pasathai::meta::etymology::" + meaning.etymology.lower())
                    for pos in meaning.partOfSpeech:
                        note["tags"].append("pasathai::meta::part_of_speech::" + pos.lower())
            else:
                meaning = thai_word_data.firestoreWord.meanings[0]

                if len(meaning.components) > 1:
                        note["tags"].append("pasathai::meta::component_word")
                if meaning.etymology != "":
                        note["tags"].append("pasathai::meta::etymology::" + meaning.etymology.lower())

                for pos in meaning.partOfSpeech:
                    note["tags"].append("pasathai::meta::part_of_speech::" + pos.lower())

        note["tags"].append("pasathai::meta::processed")
        note["tags"] = unique(note["tags"])

    anki['children'][2]["notes"] = notes

    json_out = open('../deck.json', 'w')
    json_out.write(json.dumps(anki, indent=4, ensure_ascii=False))

    json_file.close()
    json_out.close()