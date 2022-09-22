# pasathai
 A JSON representation of my personal thai flashcards

The python script is used to turn natural thai, identify thai syllabes in said input, and transliterate the syllables such that they can colored by tone in ANKI


# to install thaibow (from fresh)
- ❯ python3 -m venv env
- ❯ source env/bin/activate 
- ❯ python3 -m pip install -r requirements.txt
- ❯ python3 -m pip uninstall gensim
- ❯ python3 -m pip install gensim --no-binary gensim
- ❯ python setup.py develop

# to run model generator
- ❯  datamodel-codegen  --input ./thaibow/schema.json --input-file-type jsonschema --output ./thaibow/model.py

# Anki add'ons reccomended
### Free
- [CrowdAnki: JSON export&import](https://github.com/Stvad/CrowdAnki)
- [Pass/Fail 2](https://ankiweb.net/shared/info/876946123)
### Paid (Anking)
- [Audiovisual Feedback](https://ankiweb.net/shared/info/231569866)
- [Calculate New Cards To](https://ankiweb.net/shared/info/2014569756)