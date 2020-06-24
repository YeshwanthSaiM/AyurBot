"""AyurBot fb webhook

1. /verify
    This is used to verify the webhook for fb developer messenger

2. ./getResponse
    This is used to return response to the user

Note: 
When a user enters the question in the yeshuthecool message chat. 
The message gets hits to /getResponse. We generate the response
Then an api is hit to give the response to the user. 
"""


# libraries:
from flask import Flask
from flask import render_template,jsonify,request
from flask_cors import CORS
import json
import os
import requests
import generateResponse
import requests

# Making the initializations for the flask
app = Flask(__name__)
CORS(app)
verbose = True
verify_token = "abcd1234"

# default empty path:
@app.route('/verify',methods = ['POST','GET'])
def verify():
    try: 
        return request.args['hub.challenge']
    except:
        if verbose:
            print("The verify is failed because no hub.challenge key in request")
        pass
    response = {
        "status":"failed",
        "status_code": 400,
        "description": "No required key of hub.challenge in request"
    }

    # now the actuall response also here::
    if verbose:
        print("Here is the request in json")
        print(request.json) 
    body = request.json
    if verbose:
        print("Inside /getResponse =>")
        print("body of the request:: ",body) 

    resBody = generateResponse.extractResponse(body)
  
    if verbose:
        print("Respose body :: ",resBody)
    
    # Making a api call to give the response to user. 
    headers = {'Content-Type': 'application/json'}
    token = "EAAmlYOdwvrMBAOBQRLqaCNchVPXvFpZAVBaraZC9Y9u4gYZA34Guel81cFZAc5VVIpXIRLoKhuTVgZAPfKPZBoaBQjKXAvzyukZBgynwZCKeZCEmkScSNEiKPW6JB2cfOBoZC9bFRZBlr8ZAa2bsMQ3OSRbSHu2fcPjQuTTrLdvZBXHzVwwZDZD"
    url = "https://graph.facebook.com/v6.0/me/messages?access_token={}".format(token)
    r = requests.post(url=url, data=json.dumps(resBody),headers=headers)
    
    print("Reponse of the for post call to fb api to give reply to user")
    print(r.json())
    return response

# default empty path:
@app.route('/getResponse',methods = ['POST','GET'])
def getResponse():
    """Takes in the request from messenge. returns the response.
    """
    body = eval(request.get_data().decode("utf-8"))
    if verbose:
        print("Inside /getResponse =>")
        print("body of the request:: ",body) 

    # resBody = generateResponse.extractResponse(body)
    id_ = generateResponse.extractId(body)
    resBody = {
        # "messaging_type":"RESPONSE",
        "recipient": {
            "id": id_
        },
        "message": {
            "text": "Hi! This is chatbot made by Yeshwanth."
        }
    }
    if verbose:
        print("Respose body :: ",resBody)
    
    # Making a api call to give the response to user. 
    headers = {'Content-Type': 'application/json'}
    token = "EAAmlYOdwvrMBAOBQRLqaCNchVPXvFpZAVBaraZC9Y9u4gYZA34Guel81cFZAc5VVIpXIRLoKhuTVgZAPfKPZBoaBQjKXAvzyukZBgynwZCKeZCEmkScSNEiKPW6JB2cfOBoZC9bFRZBlr8ZAa2bsMQ3OSRbSHu2fcPjQuTTrLdvZBXHzVwwZDZD"
    url = "https://graph.facebook.com/v6.0/me/messages?access_token={}".format(token)
    r = requests.post(url=url, data=json.dumps(resBody),headers=headers)
    
    print("Reponse of the for post call to fb api to give reply to user")
    print(r.json())
    return {'status':200} 


app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)