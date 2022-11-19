import flask
import joblib
import numpy as np
import pandas as pd
import requests
from flask import render_template, request
from flask_cors import CORS
from xgboost import XGBRegressor

app = flask.Flask(__name__, static_url_path='')
CORS(app)

API_KEY = "HbsERqktGhGoDzwEicls3kLdXyrcM-Z071KIpvjmAKT3"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token',data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/', methods=['GET'])
def sendhomepage():
    return render_template('Index Page.html')


@app.route('/predict', methods=['POST'])
def predictenergy():
    print("working..")
    ws = float(request.form['ws'])
    wd = float(request.form['wd'])
    X = [[ws, wd]]
    xgr=XGBRegressor()
    df=pd.DataFrame(X, columns=['WindSpeed(m/s)', 'WindDirection'])
    payload_scoring = {"input_data": [{"fields": [['ws','wd']], "values":[3,4]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/198415bf-21da-4777-9224-d0a04107abeb/predictions?version=2022-11-17', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("response_scoring")
    predictions = response_scoring.json()
    print(predictions)
    predict = predictions['predictions'][0]['values'][0][0] 
    print("Final prediction :",predict)
    return render_template('Predict Page.html',predict=predict)



if __name__ == '__main__':
    app.run()

