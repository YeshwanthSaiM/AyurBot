"""Generates responses based on intent 
Response format :: 
{
    "recipient": {
        "id": id_
    },
    "message": {
        "text": "Hi! This is chatbot made by Yeshwanth."
    }
}
"""
from fuzzywuzzy import fuzz
import json, numpy as np, pandas as pd
import threading, time
from datetime import datetime
import requests

# libraries
def extractResponse(obj):
    intent = extractIntent(obj)
    if intent == "getRemedy":
        response = getRemedyResponse(obj) 
    elif intent == 'getSimilarIngredient':
        response = getSimilarIngredientResponse(obj)
    elif intent == 'smalltalk':
        response = smalltalkResponse(obj)
    elif intent == 'startSubscription':
        response = startSubscriptionResponse(obj)
    elif intent == 'endSubscription':
        response = endSubscriptionResponse(obj)
    else:
        response = {
            "message": {
                "text": "Hi! I could not understand you. Can you ask another one please!"
            }
        }  
    # adding id to the response:
    id_ = extractId(obj)
    response["recipient"] = {
            "id": id_
        }
    return response

def extractIntent(obj):
    """Extracts the intent from the face book request.
    """
    text = obj["entry"][0]["messaging"][0]["message"]["text"]
    intent = obj["entry"][0]["messaging"][0]["message"]["nlp"]["entities"]["intent"][0]["value"]
    return intent

def extractDisease(obj):
    """Extracts the disease from the entities captured from facebook response
    """
    entitiesObj = obj["entry"][0]["messaging"][0]["message"]["nlp"]["entities"]
    entities = {}
    disease = ""
    for key, val in entitiesObj.items():
        if key == 'disease':
            entities[key] = val[0]["value"]
            disease = val[0]["value"]

    # extracting disease from entities 
    return disease

with open("../data/remedies/remedy_1.json", "r") as f:
    content = json.load(f)

conditions = []
treatments = []
for obj in content:
    conditions.append(obj["condition"])
    treatments.append(obj["treatments"])

def extractRemedy(disease):
    """Extracts the remedy from the data base from disease
    """
    global treatments
    global conditions
    condition = disease
    scores = [fuzz.ratio(str(condition),str(cond)) for cond in conditions]
    maxIndex = np.argmax(scores)
    remediesList = treatments[maxIndex]
    remedy = " ".join(remediesList)
    remedy = remedy
    return remedy


def getRemedyResponse(obj):
    """Gives response for getRemedy intent
    If disease is present remedy is given
    or else prompt is given for disease
    """
    disease = extractDisease(obj)
    if disease:
        remedy = extractRemedy(disease)
        response = {
            "message": {
                "text": remedy
            }
        }

    else:
        response = {
            "message": {
                "text": "Can you please say for which disease you need treatment?"
            }
        } 

    return response
path = "../data/smalltalk.xlsx"
smalltalk = pd.read_excel(path)
questions = smalltalk['User'].values
answers = smalltalk['BOT'].values

def smalltalkResponse(obj):
    global questions
    global answers
    question = obj["entry"][0]["messaging"][0]["message"]["text"]
    scores = [fuzz.ratio(str(question),str(q)) for q in questions]
    maxIndex = np.argmax(scores)
    answer = answers[maxIndex]
    response = {
            "message": {
                "text": answer
            }
        }
    return response

def extractIngredient(obj):
    entitiesObj = obj["entry"][0]["messaging"][0]["message"]["nlp"]["entities"]
    entities = {}
    ingredient = ""
    for key, val in entitiesObj.items():
        if key == 'ingredient':
            entities[key] = val[0]["value"]
            ingredient = val[0]["value"]

    # extracting disease from entities 
    return ingredient

def getSimilarIngredientResponse(obj):
    """extracts ingredients and gives substiture for it
    """
    ingredient = extractIngredient(obj)
    similarIngredient = ingredient
    response = {
            "message": {
                "text": "You can replace {} with {}.".format(ingredient, similarIngredient)
            }
        }
    return response

def extractId(obj):
    return obj["entry"][0]["messaging"][0]["sender"]["id"]

def startSubscriptionResponse(obj):
    """Intent starts the subscription
    """
    id_ = extractId(obj)
    with open("../data/subscriptions.json","r") as f:
        content = json.load(f)
        subscriptionsIds = content["subscriptions"]

    if id_ not in subscriptionsIds:
        print("id ::::::::::::::::::::::::::::::::::::::",id_)
        print(subscriptionsIds)
        subscriptionsIds.append(id_)
        with open("../data/subscriptions.json","w") as f:
            obj = {
                "subscriptions": subscriptionsIds
            }
            json.dump(obj,f)
        print("Subscription added successfully")
        response = {
                "message": {
                    "text": "Subscription added successfully"
                }
            }
    else:
        response = {
                "message": {
                    "text": "Subscription already present! Thank you"
                }
            }
    return response

def endSubscriptionResponse(obj):
    """Ends the subscription
    """
    id_ = extractId(obj)
    with open("../data/subscriptions.json","r") as f:
        content = json.load(f)
        subscriptionsIds = content["subscriptions"]
    
    if id_ in subscriptionsIds:
        subscriptionsIds.remove(id_)
        with open("../data/subscriptions.json","w") as f:
            obj = {
                "subscriptions": subscriptionsIds
            }
            json.dump(obj,f)
        print("Subscription removed successfully")
        response = {
            "message": {
                "text": "Subscription removed successfully"
            }
        }
    else:

        response = {
                "message": {
                    "text": "Subscription not found"
                }
            }
    return response

def checkTime(t1,t2,limit=10):
    # limit in minutes:
    hours1 = int(t1.split(":")[0])
    hours2 = int(t2.split(":")[0])
    if hours1 == hours2:
        mins1 = int(t1.split(":")[1])
        mins2 = int(t2.split(":")[1])
        if abs(mins1 - mins2) < limit:
            return True
    return False
def subscriptionSendMessages(ids, instruction):
    # sends messages to ides
    for id_ in ids:
        resBody= {
            "recipient":{
                "id": id_
            },
            "message": {
                "text": "Hi! I could not understand you. Can you ask another one please!"
            }
        }
        headers = {'Content-Type': 'application/json'}
        token = "EAAmlYOdwvrMBAOBQRLqaCNchVPXvFpZAVBaraZC9Y9u4gYZA34Guel81cFZAc5VVIpXIRLoKhuTVgZAPfKPZBoaBQjKXAvzyukZBgynwZCKeZCEmkScSNEiKPW6JB2cfOBoZC9bFRZBlr8ZAa2bsMQ3OSRbSHu2fcPjQuTTrLdvZBXHzVwwZDZD"
        url = "https://graph.facebook.com/v6.0/me/messages?access_token={}".format(token)
        r = requests.post(url=url, data=json.dumps(resBody),headers=headers)
        
        print("Reponse of the for post call for subscriptions")
        print(r.json())
    pass

def subscriptionMessages():
    """For each subscription ids, 
    messages are given for the diet plan.
    """
    print("Subscriptions Started")
    while True:
        subscriptionsIds = []
        with open("../data/subscriptions.json","r") as f:
            content = json.load(f)
            print(content)
            subscriptionsIds = content["subscriptions"]
        
        # diet plan
        dietPlan = {}
        with open("../data/dietPlan.json","r") as f:
            content = json.load(f)
            dietPlan = content['dietPlan']
        
        # time now ::
        now = datetime.now().strftime("%H:%M:%S")
        for planObj in dietPlan:
            tempTime = planObj['time']
            if checkTime(now,tempTime):
                # send messages
                instruction = planObj['instruction']
                subscriptionSendMessages(subscriptionsIds,instruction)
        
        time.sleep(600)
        print("Slept for 10 minutes!")
    

def my_inline_function(some_args):
    # do some stuff
    download_thread = threading.Thread(target=subscriptionMessages, args=some_args)
    download_thread.start()
    # continue doing stuff
my_inline_function({})
