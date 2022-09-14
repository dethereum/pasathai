from thaibow.app import my_function, get_color_escape
from rich.console import Console
from rich.table import Table

import json
import requests

# engines for tokenization that work locally
engines = [
    "newmm", # fastest tokenizer
    # "newmm-safe",
    # "longest", 
    # "attacut", 
    # "nercut", 
    # "tltk",
]

url = 'https://www.thai2english.com/_next/data/qqerWs1vgtpJGScVYNO0N/index.json'

def handle_repeater(text):
    if "ๆ" in text:
        return text.replace("ๆ", text.replace("ๆ", ""))
    return text

def get_notes_data():
    with open('../deck.json') as json_file:
        notes = json.load(json_file)['children'][2]["notes"]

        for note in notes:
            text = note['fields'][0]

            # data = requests.get(url, params={'q': text})
            # props = json.loads(data.content)['pageProps']['processed']
            
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

                
            







