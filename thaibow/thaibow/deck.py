from thaibow.app import my_function, get_color_escape
from rich.console import Console
from rich.table import Table

import json

# engines for tokenization that work locally
engines = [
    "newmm", # fastest tokenizer
    # "newmm-safe",
    # "longest", 
    # "attacut", 
    # "nercut", 
    # "tltk",
]

def get_notes_data():
    with open('../deck.json') as json_file:
        notes = json.load(json_file)['notes']

        for note in notes:
            if note['note_model_uuid'] == '2949c2a2-322f-11ed-bea3-57623aa003ca':
                text = note['fields'][0]

                table = Table(title=text)
                columns = ["Transliteration", "Output"]

                for column in columns:
                    table.add_column(column)

                for engine in engines:
                    (output, roman_text) = my_function(text, engine)
                    row = [roman_text, output]
                    table.add_row(*row, style='bright_green')

                console = Console()
                console.print(table)