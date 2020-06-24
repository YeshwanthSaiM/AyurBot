"""
This file trains and extracts the named entities from the query
@author: yeshu
"""
import spacy
import random
import pickle

# TRAIN_DATA = [('what is the price of polo?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of ball?', {'entities': [(21, 25, 'PrdName')]}), ('what is the price of jegging?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of t-shirt?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of jeans?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bat?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of shirt?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of bag?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of cup?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of jug?', {'entities': [(21, 24, 'PrdName')]}), ('what is the price of plate?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of glass?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of moniter?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of desktop?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of bottle?', {'entities': [(21, 27, 'PrdName')]}), ('what is the price of mouse?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of keyboad?', {'entities': [(21, 28, 'PrdName')]}), ('what is the price of chair?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of table?', {'entities': [(21, 26, 'PrdName')]}), ('what is the price of watch?', {'entities': [(21, 26, 'PrdName')]})]
# making data for ner train
templates = [
        "what is the treatment for {}?",
        "Give me remedy for {}",
        "{}",
        "Tell me treatment for {}",
        "How to reduce {}",
        "How to treat {}",
        "how to reduce {}",
        "{}?",
        "how to treat {}?",
        "help me reduce {}",
        "{} how to treat it",
        "hey! tell me about {}",
        "hello. I have {}",
        "I have {}",
        "I am suffering with {}",
        "I am feeling {}",
        "what to do when I have {}",
        "I want get well from {}",
        "how to get cured {}",
        "{} how to treat it.",
        "How to treat {}, can you say it",
        "How to improve health from {}",
        "how to improve {}"
        ]
conditions = [
        "Indigestion",
        "indigestion",
        'Ear Pain',
        'par pain',
        'Hoarseness of voice',
        'hoarseness of voice',
        'Aches and pain',
        'aches and pain',
        'Cold / cough',
        'Cold',
        'cough',
        'head ache',
        'Head ache',
        'Abdominal pain',
        'abdominal pain',
        'Piles',
        'piles',
        'Painful Menses',
        'painful Menses',
        'Urticaria (Skin allergy)',
        'Urticaria',
        'Skin allergy',
        'Skin problems',
        'Abdominal pain',
        'abdominal pain',
        'immunity',
        'synus'
        ]

temp = []
for template in templates:
    for condition in conditions[:2]:
        s = template.format(condition)
        temp.append(s)
def makingData():
    temp = []
    for template in templates:
        for condition in conditions:
            s = template.format(condition)
            word = condition
            leftIndex = s.index(word)
            rightIndex = leftIndex + len(word)
            entities = {'entities':[(leftIndex,rightIndex,"condition")]}
            temp.append((s,entities))
    return temp

# temp = makingData()

TRAIN_DATA = makingData()

"""
TRAIN_DATA_PATH = "../Data/NERData/TRAIN_DATA"
with open (TRAIN_DATA_PATH, 'rb') as fp:
    TRAIN_DATA = pickle.load(fp)
"""

#######
def train_spacy(data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp




prdnlp = train_spacy(TRAIN_DATA, 25)

# Save our trained Model
modelfilepath = "../models/NER"
prdnlp.to_disk(modelfilepath)


test_text = "How to treat for head ache"
doc = prdnlp(test_text)

for ent in doc.ents:
    print(ent.text," : ", ent.label_)
    
        
loaded_nlp = spacy.load(modelfilepath) 
test_text = "I want to book an appointment for Dr. Raju"
doc = loaded_nlp(test_text)

for ent in doc.ents:
    print(ent.text," : ", ent.label_)


