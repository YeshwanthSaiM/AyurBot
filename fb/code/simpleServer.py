"""AyurBot fb webhook

1. /
    echo: Echos the request.

"""


# libraries:
from flask import Flask
from flask import render_template,jsonify,request
from flask_cors import CORS
import json
import os
import requests

# Making the initializations for the flask
app = Flask(__name__)
CORS(app)

verify_token = "abcd1234"
# default empty path:
@app.route('/',methods = ['POST','GET'])
def echo():
    try: 
        return request.args['hub.challenge']
    except:
        body = eval(request.get_data().decode("utf-8"))
        print(body)

    return body 


app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)