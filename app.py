from flask import Flask, request
import pickle

app = Flask(__name__)

@app.post('/prediction')
def get_prediction():
    request_data = request.get_json()
    print(request_data)
    return {'prediction': 100}