"""
This file makes the chat: (implements the dialogue flow)
    1. It takes the query
    2. DM (Dialogue manager)
    3. Gives the response
@author: yeshu
"""
import sys
import json
from fuzzywuzzy import fuzz
import numpy as np
from NER import NER
from ibmNERClinicalData import ibmNER

state = "start"
# intentsUtterances
intentsUtterances = {}
utterancesIntents = {}
utterancesIntentsTuples = []
utterancesList = []
intentsList = []
# loading the NER model
nerModel = ""

with open("../data/intents/intentsUtterances.json", 'r') as fp:
    content = json.load(fp)
    intentsUtterances = content
    
for key,values in intentsUtterances.items():
    for val in values:
        utterancesIntents[val] = key
        
for key , val in utterancesIntents.items():
    utterancesIntentsTuples.append([key,val])
    utterancesList.append(key)
    intentsList.append(val)

def intentClassification(query):
    # returns intent i.e one of ['getInfo', 'addData', 'smalltalk','faq']
    global intentsList
    global utterancesList
    
    scores = [fuzz.ratio(str(query),str(utt)) for utt in utterancesList]
    # print(scores)
    maxIndex = np.argmax(scores)
    # print(maxIndex)
    intent = intentsList[maxIndex]
    return intent

def extractEntities(query):
    # loading the model
    global ibmNER
    en = ibmNER(query)
    entities = en.entities
    return entities

    
with open("../data/treatments/treatments_1.json", "r") as fp:
    content = json.load(fp)

conditions = []
treatments = []
for obj in content:
    conditions.append(obj["condition"])
    treatments.append(obj["treatments"])
    
def getTreatment(condition):
    # based on the condition => it gives treatment.
    global treatments
    global conditions
    scores = [fuzz.ratio(str(condition),str(cond)) for cond in conditions]
    maxIndex = np.argmax(scores)
    treatment = treatments[maxIndex]
    # treatment = "to cure {}, Please take care mama".format(condition)
    return treatment, scores[maxIndex]

with open("../fb/data/remedies/remedy_1.json", "r") as fp:
    content = json.load(fp)

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
    return remediesList, np.max(scores)


def addTreatment(treatmentObj):
    with open("../data/treatments/treatments_1.json", "r") as fp:
        content = json.load(fp)
    content.append(treatmentObj)
    with open("../data/treatments/treatments_1.json", "w") as fp:
        json.dump(content,fp)
    return None

def refreshTreatments():
    global conditions
    global treatments
    with open("../data/treatments/treatments_1.json", "r") as fp:
        content = json.load(fp)
    conditions = []
    treatments = []
    for obj in content:
        conditions.append(obj["disease"])
        treatments.append(obj["treatments"])
    return None

def checkSmallTalk(query):
    hi = ['hai','hello','Hi','Hello',"how are you?","hi","Hello"]
    bye = ['bye','good bye','take care','see you later']
    if query in hi:
        response = "Hi. I am AyurBot. Your companion for ayurvedic treatments"
        return True , response
    elif query in bye:
        response = "bye for now. Come back again"
        return True , response
    return False, ''

def Chat(query):
    global state
    # support for Smalltalk:
    check, res = checkSmallTalk(query)
    if check:
        return res
    
    # simplified implementation for version 1.
    intent = intentClassification(query)
    print("Intent ::",intent)
    # extracting entities
    entities_ = extractEntities(query)
    entities = {}
    for key, val in entities_.items():
        entities[val] = key 
    print("entities")
    print(entities.keys())
    if state == "start":
        # finding intent
        if intent == 'getRemedy':
            if "disease" in list(entities.keys()):
                # logic where to give treatments for condition
                treatmentList, score = extractRemedy(entities['disease'])
                if score > 75:
                    response = " .".join(treatmentList)
                    # re setting the state
                    state = "start"
                    return response
                else:
                    response = "Bot not trained for condition : {}. Please say add data and proceed"
                    state = 'start'
                    return response
            else:
                if 'item' in entities:
                    # logic where we give benefits 
                    # logic where we give substitue
                    response = "To know benefits of {}. Please eat it and you will get".format(entities['item'])
                    state = "start"
                    return response

        elif intent == "addData":
            # case where we give template
            # template 
            template = {
                "condition": "",
                "treatments": [
                    "",
                    ""
                ]
            }
            response = "plase fill the following and return => " + str(template)
            state = 'inter'
            return response

            # return response
            # no update of state to start
    else:
        if intent == "addData":
            # validate query 
            treatmentObj = eval(query)
            # add to the data
            addTreatment(treatmentObj)
            response = "Thanks for adding data to the bot."
            
            state = 'start'
            return response
        else:
            # here also same response as of now:: 
            # todo:: update later
            treatmentObj = eval(query)
            # add to the data
            addTreatment(treatmentObj)
            response = "Thanks for adding data to the bot."
            state = 'start'
            return response
        
    response = "Bot is not trained up to that point. Kindly add data."
    return response

"""
# to do: remove
query = 'I need treatment for headache'
intentClassification(query)
extractEntities(query)
Chat(query)

query = "add data for piles"
extractEntities(query)
Chat(query)

query = "{'disease': 'Piles', 'treatments': ['1 gm. powder and 1 gm of Spragne / Yavani /Vamu. black-salt with butter-milk twice daily.']}"
Chat(query)

  
"""