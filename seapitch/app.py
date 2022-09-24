import json
from flask import Flask, request, jsonify
import parselmouth
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)


def get_pitch_track_from_field(field):
    name = field.split(':')[1].replace("]", "")

    sound = parselmouth.Sound(
        '~/Library/Application Support/Anki2/User 1/collection.media/' + name)

    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']

    return {'y': list(pitch_values), 'x': list(pitch.xs())}


@app.route('/pitch_track', methods=['POST'])
def pitch_track():
    import parselmouth

    files = json.loads(request.data)['files']

    pitch_tracks = [get_pitch_track_from_field(file) for file in files]

    return jsonify(pitch_tracks)
