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