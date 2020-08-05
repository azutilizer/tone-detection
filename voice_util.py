import os
import numpy as np
import librosa
import json
import datetime
import base64
import uuid
import requests
import pickle
from train_model import loading_model
from utilities import get_one_data
from mimetypes import MimeTypes
from flask import make_response, request, jsonify
from flask_restful import Resource, reqparse, inputs

UPLOAD_DIR = 'uploads'


class CustomException(Exception):
    pass


class StillProcessing(Exception):
    pass


class Tone_Detect(Resource):
    def __init__(self):
        self.session = requests.Session()
        self.uuid = uuid.uuid4().hex
        self.mime = MimeTypes()
        current_time = int(datetime.datetime.utcnow().timestamp())
        self.response_filename = f'{current_time}.txt'

        self.model = None
        self.model_path = os.path.join('models', 'my_lstm_model.h5')
        self.data_path = os.path.join('.', 'dataset')
        self.tone_list = []

        self.get_tone_list()
        self.load_model()
    
    def get_tone_list(self):
        try:
            for tone in os.listdir(self.data_path):
                if os.path.isdir(os.path.join(self.data_path, tone)):
                    self.tone_list.append(tone)
        except:
            pass

    def load_model(self):
        if self.model_path == '':
            return
        try:
            self.model = loading_model(self.model_path)
        except:
            pass

    def recognize(self, model, voice_file_path):
        if model is None:
            result = {"tone": "", "score": 0.0}
            return result
        feat = get_one_data(voice_file_path)
        feat = np.array([feat])
        voice = model.predict(feat)
        score = model.predict_proba(feat)
        max_score = max(score[0])
        ind = list(score[0]).index(max_score)
        result = {
            "tone": self.tone_list[ind],
            "score": "{:.3f}".format(max_score)
        }
        return result
    
    def post(self):
        is_parse = request.is_json
        if not is_parse:
            response = json.dumps({
                'result': 'Failed to receive audio file.'
            })
            return make_response(response, 404)

        content = request.get_json()
        base64_audio = content['audio_data']
        base64_ext = content['ext_type']
        
        if base64_audio is None:
            print('Audio is None.')
            return 'Audio File Uploading Error!'

        encoded_data = base64_audio.split(',')[-1]
        audio_buf = base64.b64decode(encoded_data)

        tmp_audio_file = os.path.join(UPLOAD_DIR, 'upload_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.wav')

        print('writing audio file: {}'.format(tmp_audio_file))
        with open(os.path.join(UPLOAD_DIR, 'tmp.wav'), 'wb') as f:
            f.write(audio_buf)

        # convert audio
        try:
            convert_audio_to_16kHz(os.path.join(UPLOAD_DIR, 'tmp.wav'), tmp_audio_file)
        except:
            response = json.dumps({
                'result': 'Failed to converting audio.'
            })
            return make_response(response, 503)

        try:
            result = self.recognize(self.model, tmp_audio_file)
            print(result)
            response = json.dumps(result)
        except:
            response = json.dumps({
                'result': 'Failed to send.'
            })
            return make_response(response, 503)

        return make_response(response, 200)


def read_voice_file(voice_file):
    if not os.path.exists(voice_file):
        return []
    y, sr = librosa.load(voice_file, sr=16000)
    nFrames = len(y)
    audio_length = nFrames * (1 / sr)
    return audio_length, np.asarray(y, dtype=np.float)


def get_duration(wave_file):
    y, fs = librosa.load(wave_file, sr=16000)
    nFrames = len(y)
    audio_length = nFrames * (1 / fs)

    return audio_length


def convert_audio_to_16kHz(audio_file, dest_file):
    if os.path.exists(dest_file):
        os.remove(dest_file)
    cmd = "ffmpeg -i \"{}\" -ac 1 -acodec pcm_s16le -ar 16000 \"{}\" -y -loglevel panic".format(audio_file, dest_file)
    os.system(cmd)


def save_model_info(model_path, speaker_model):
    with open(model_path, "wb") as f:
        pickle.dump(speaker_model, f)


def load_model_info(model_path):
    if not os.path.exists(model_path):
        return []
    with open(model_path, "rb") as f:
        return pickle.load(f)




