from thaibow.app import my_function

import json

def get_notes_data():
    with open('../deck.json') as json_file:
        notes = json.load(json_file)['notes']

        for note in notes:
            if note['note_model_uuid'] == '2949c2a2-322f-11ed-bea3-57623aa003ca':
                text = note['fields'][0]
                print(text)
                print(my_function(text))