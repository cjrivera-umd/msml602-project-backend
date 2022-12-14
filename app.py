from flask import Flask, request
from flask_cors import CORS
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
import csv
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

SECONDS_FOR_8YEARS = 251596800

@app.post('/prediction')
def get_prediction():
    request_data = request.get_json()

    # Get win percentage for home team
    hteam = f'H-{request_data["home"]}'
    hteam_wp = get_win_percentage(hteam)

    # Get win percentage for away team
    ateam = f'A-{request_data["away"]}'
    ateam_wp = get_win_percentage(ateam)

    # Encode values
    is_neutral = 'F' if 'Qatar' in hteam or 'Qatar' in ateam else 'T'
    encoded_features = encode_values(hteam, ateam, 'FIFA World Cup', is_neutral)

    # Prepare for prediction
    numerical_features = np.array([hteam_wp, ateam_wp])
    all_features = np.concatenate((numerical_features, encoded_features), axis=None)

    # Predict
    prediction = predict(all_features)

    return {'predicted_winner': prediction}


def predict(features):
    with open('model_pickle', 'rb') as f:
        model = pickle.load(f)
        predictions = model.predict([features])

        return predictions[0]


def encode_values(hteam, ateam, tournament, neutral):
    with open('encoder_pickle', 'rb') as f:
        encoder = pickle.load(f)
        encoded = encoder.transform([[hteam, ateam, tournament, neutral]]).toarray()
        return encoded[0]


def get_win_percentage(team):
    games = 0
    wins = 0

    limit = datetime.now().timestamp() - SECONDS_FOR_8YEARS
    with open('preprocessed_results.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            match = dict(row)

            if float(match['epoch']) < limit or (team not in [match['home_team'], match['away_team']]):
                continue

            games += 1

            if (match['winner'] == 'Home' and team == match['home_team']) or (match['winner'] == 'Away' and team in match['away_team']):
                wins += 1

    print(games)
    return 0 if games == 0 else wins / games

            
            


    

