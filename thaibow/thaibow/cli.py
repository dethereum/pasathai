import os
import json

from thaibow.deck import get_notes_data
from thaibow.validator import api_external_validator

path_to_json = './thaibow/data/'

def main():
    get_notes_data()
    # this finds our json files

    # json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    # for index, js in enumerate(json_files):
    #     with open(os.path.join(path_to_json, js)) as json_file:
    #         json_text = json.load(json_file)
    # 
    #         api_external_validator(json_text, js)


if __name__ == "__main__":
    main()