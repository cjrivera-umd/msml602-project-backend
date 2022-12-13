from flask import Flask, request
import pickle
import csv

app = Flask(__name__)

@app.post('/prediction')
def get_prediction():
    request_data = request.get_json()
    print(request_data)
    return {'prediction': 100}

def get_win_percentage(team):
    games = 0
    wins = 0

    # with open('preprocessed_results.csv') as csvfile:

