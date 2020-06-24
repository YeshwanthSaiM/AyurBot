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

# speech recognition:
import speech_recognition as sr 

# text to speech
import pyttsx3
import pythoncom

import json
import pandas as pd
import os
import numpy as np

# pickle for entities data
import pickle
"""
def makeNERentry(utt,slots):
    # This function makes a single entry to be given to the NER data
    utt = utt
    ents = {"entities":[]}
    for slot in slots:
        text = slot['text']
        label = slot['label']
        left_index = utt.index(text)
        right_index = left_index + len(text)
        ents['entities'].append((left_index,right_index,label))
    entry = (utt,ents)
    return entry

def addDataToPlatform(Listobjs):
    # for each obj in Listbojs
    # stores data in respecive fields
    global makeNERentry
    entries = []
    domain = Listobjs['domain']
    intent = Listobjs['intent']
    Listobjs = Listobjs['slots']

    for obj in Listobjs:
        # For intent and domain
        
        utt = obj['utterance']
        # Adding in the respective intent temp_0 folder
        # try else block
        try:
            # new domain
            mkdir("../Data/Domains/" + domain)
        except:
            # case when domain already exits
            pass
    
        try:
            # new intent
            mkdir("../Data/Domains/" + domain + "/Intents/"+ intent)
        except:
            # case when intent already exits
            pass

        # reading temp_0.txt file:
        with open("../Data/Domains/" + domain + "/Intents/"+ intent+"/temp_0.txt", "a+") as myfile:
            myfile.write("\n")
            myfile.write(utt)

        # For Ner:
        # we first make the data:
        print("object",obj)
        slots = obj['entities']
        slots.append(obj['task'])

        entry = makeNERentry(utt,slots)
        entries.append(entry)

    # For NER: 
    # pass
    # Loading the existing data
    if len(entries) > 0:
        TRAIN_DATA_PATH = "../Data/NERData/TRAIN_DATA"
        with open(TRAIN_DATA_PATH, 'rb') as fp:
            TRAIN_DATA = pickle.load(fp)

        TRAIN_DATA.extend(entries)
        with open("../Data/NERData/TRAIN_DATA", 'wb') as file:
            pickle.dump(TRAIN_DATA, file)
    return None


    

def text2speech(text):
    # Converts text to speech and reads out
    pythoncom.CoInitialize()
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    return None

# Making a function for speech to text:
def gettextFromSpeech():
    # prompt the user to speak
    # Starts the mic 
    # records the user voice
    # returns the text
    global text2speech
    prompt = "Speak now!"
    text2speech(prompt)

    device_id = 0
    r = sr.Recognizer() 
    text = ''
    with sr.Microphone(device_index = device_id,
                   sample_rate = 48000,
                   chunk_size = 2048) as source: 
        #wait for a second to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 

        r.adjust_for_ambient_noise(source) 
        print("Say Something")

        #listens for the user's input 
        audio = r.listen(source) 

        try: 
            text = r.recognize_google(audio) 

        #error occurs when google could not understand what was said 

        except sr.UnknownValueError: 
            text = "Google Speech Recognition could not understand audio"

        except sr.RequestError as e: 
            text = "Could not request results from Google Speech Recognition service; {0}".format(e)
            
    return text
# Loggin module
# For each dialoue we add to it
logs = []

# function to extract the vulnerable conversations
def extractVulnerableConversations(conversations):
    # functionality to extract the required conversations
    vulnerableConversations = []
    i = 0
    # simple logic: when the task in not of the intent
    for conv in conversations:
        domain = conv['domain']
        intent = conv['intent']
        task = conv['task']

        intent_tasks_path = "../Data/Domains/" + domain + "/Intents/" + intent
        intent_tasks_path = intent_tasks_path + "/support.json"
        
        with open(intent_tasks_path, 'r') as file:
            content = json.load(file)
            list_of_tasks = content['tasks']
        if task not in list_of_tasks:
            conv['id'] = i 
            i += 1
            vulnerableConversations.append(conv)
    return vulnerableConversations

def getAllData():
    # To extract all the required mapping data for vulnerable conversations
    domains = []
    intents_map = {}
    states = ['start', 'inter']
    tasks = {}
    slots = []

    # extracting the domains
    domains = os.listdir("../Data/Domains/")
    # extracting the intents for each domain
    for domain in domains:
        intents = os.listdir("../Data/Domains/" + domain + "/Intents/")
        intents_map[domain] = intents
        # extracting tasks in each intent
        for intent in intents:
            with open("../Data/Domains/" + domain + "/Intents/" + intent + "/support.json", "r") as myfile:
                content = json.load(myfile)
                tasks[intent] = content['tasks']
    
  
    # connecting to the knowledge base
    kb = pd.read_csv("../Data/KnowledgeBase/KnowledgeBase.csv")
    slots_raw = kb.slots.values
    for slot in slots_raw:
        slots.extend([s.strip() for s in slot[1:-1].split(",") if len(s) > 3])
    slots = list(np.unique(slots))

    obj = {
        'domains': domains,
        'intents': intents_map,
        'states': states,
        'tasks': tasks,
        'slots': slots
        }
    return obj
"""
# Making the initializations for the flask
app = Flask(__name__)
CORS(app)

# default path: rendering UI from home.html in templates folder
@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/refresh')
def refresh():
    global Refresh
    Refresh()
    return jsonify({"status":"success","response":"The chatbot has been refreshed."})

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

"""

@app.route('/speak', methods=["POST","GET"])
def speak():
    try:
        # speak
        speech_text = gettextFromSpeech()    
        response = speech_text
        #            
        return jsonify({"status":"success","response":response})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})

# To get list of all conversations
@app.route('/getConversations', methods=["POST","GET"])
def getConversations():
    try:
        # loading the json file
        with open("../Conversations/conversations.json", 'r') as convfile:
            conversations = json.load(convfile)
        

        return jsonify({"status":"success","conversations":conversations})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry there is an issue with openning file"})

@app.route('/getVulnerableConversations', methods=["POST","GET"])
def getVulnerableConversations():
    try:
        # loading the json file
        with open("../Conversations/conversations.json", 'r') as convfile:
            conversations = json.load(convfile)
        # functionality to extract the vulnerable conversations
        vulnerableConversations = extractVulnerableConversations(conversations)
        all_data = getAllData()

        return jsonify({"status":"success","vulnerableConversations":vulnerableConversations , 'data': all_data})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry there is an issue in extracting the vulnerable"})

@app.route('/getMappingData', methods = ['POST', 'GET'])
def getMappingData():
    # sends the mapping data
    data = getAllData()
    return jsonify({"status":"success","mapping":data})

@app.route("/addData", methods = ['POST','GET'])
def addData():
    # obj contains
    # domain , intent, task, utterance, entities
    ListObjs = request.get_json()
    # adding a utterance in respective folder
    # i.e domain, intent, then utterace
    # adding a entities for task

    addDataToPlatform(ListObjs)

    return jsonify({
        "status": "success",
        "response": "Added successfully"
    })

"""
app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000)
    #app.run(port= 5000)
