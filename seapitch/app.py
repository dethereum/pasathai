import json
import os

from flask import Flask, request, jsonify
import parselmouth
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)


def get_recording_names(card_id):
    path = os.environ.get(
        'HOME') + '/Library/Application Support/Anki2/addons21/1508039970/user_files/recordings/' + card_id

    return [(rec, path + '/' + rec) for rec in os.listdir(path)]


def get_pitch_track_from_field(field):
    name = field.split(':')[1].replace("]", "")

    sound = parselmouth.Sound(
        '~/Library/Application Support/Anki2/User 1/collection.media/' + name)

    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']

    return {'y': list(pitch_values), 'x': list(pitch.xs())}


def get_pitch_track_from_rec(rec):
    print(rec)
    sound = parselmouth.Sound(rec)

    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']

    return {'y': list(pitch_values), 'x': list(pitch.xs())}


@app.route('/pitch_track_by_field', methods=['POST'])
def pitch_track_by_field():
    field = json.loads(request.data)['field']

    return jsonify(get_pitch_track_from_field(field))


@app.route('/pitch_tracks', methods=['POST'])
def pitch_tracks():
    card_id = json.loads(request.data)['card-id']

    p_tracks = []
    ids = []
    for rec_id, rec_path in get_recording_names(card_id):
        pitch_track = {rec_id: get_pitch_track_from_rec(rec_path)}

        p_tracks.append(pitch_track)
        ids.append(rec_id)

    return jsonify({'recordings': p_tracks, 'ids': ids})
