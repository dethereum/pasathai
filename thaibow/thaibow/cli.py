import os
import json

from thaibow.deck import get_notes_data
from thaibow.validator import api_external_validator

def main():
    # get_notes_data()
    # this finds our json files
    path_to_json = './thaibow/data/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            if json_text["type"] == "thai-word":
                api_external_validator(json_text, js)
            else:
                print(js, json_text["type"])

if __name__ == "__main__":
    main()