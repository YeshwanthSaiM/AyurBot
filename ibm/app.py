"""
Makes an flask server with UI
@author: yeshu
"""

# libraries:
from flask import Flask
from flask import render_template,jsonify,request
from flask_cors import CORS

# importing the chat
from chat import Chat
# from chat import Refresh

# # speech recognition:
# import speech_recognition as sr 

# # text to speech
# import pyttsx3
# import pythoncom

import json
import pandas as pd
import os
import numpy as np

# pickle for entities data
import pickle

# Making the initializations for the flask
app = Flask(__name__)
CORS(app)

# default path: rendering UI from home.html in templates folder
@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/chat', methods=["POST","GET"])
def chat():
    try:
        query = request.form["text"]

        response = Chat(query)
        
        # reads out the response:
        # text2speech(response)
        
        return jsonify({"status":"success","response":response})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})

app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5500)
    #app.run(port= 5000)
