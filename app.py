import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

def wider_model():
    # create model
    model = Sequential()
    model.add(Dense(30, input_dim=19, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam',metrics=['mae','mse'])
    return model

app = Flask(__name__)
model = pickle.load(open('finalized_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    int_features =  [float(request.form["2s"]),float(request.form["4s"]),float(request.form["6s"]),float(request.form["boundaries_first_6"]),float(request.form["boundaries_given"]),float(request.form["boundaries_last_5"]),float(request.form["economy_first_6"]),float(request.form["economy_last_5"]),float(request.form["economy_middle"]),float(request.form["extras_given"]),float(request.form["matches"]),float(request.form["not_outs"]),float(request.form["runs_first_6"]),float(request.form["runs_last_5"]),float(request.form["runs_middle"]),float(request.form["runs_scored"]),float(request.form["wickets_first_6"]),float(request.form["wickets_last_5"]),float(request.form["wickets_taken"])]
    prediction = model.predict(np.array([float(request.form["2s"]),float(request.form["4s"]),float(request.form["6s"]),float(request.form["boundaries_first_6"]),float(request.form["boundaries_given"]),float(request.form["boundaries_last_5"]),float(request.form["economy_first_6"]),float(request.form["economy_last_5"]),float(request.form["economy_middle"]),float(request.form["extras_given"]),float(request.form["matches"]),float(request.form["not_outs"]),float(request.form["runs_first_6"]),float(request.form["runs_last_5"]),float(request.form["runs_middle"]),float(request.form["runs_scored"]),float(request.form["wickets_first_6"]),float(request.form["wickets_last_5"]),float(request.form["wickets_taken"])]).reshape(1,-1))
    print(prediction)

    output = prediction[0]
    if output < 100 and output > 50:
        player = "less experienced in IPL"
    if output <= 50:
        player  = "Inexperienced"
    if output >= 100 and output <= 150:
        player = "Average Player"
    if output > 150 and output <=200:
        player = "Above Average"
    if output > 200:
        player = "Valuable Player"

    return render_template('index.html', prediction_text='The Player is {}'.format(player), spoints = 'Season Points : {} '.format(round(prediction[0][0],2)))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
