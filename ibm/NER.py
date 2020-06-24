"""
This file trains and extracts the named entities from the query
Synd NLP
@author: yeshu
"""


import numpy as np
import re
import nltk
import spacy
from joblib import load
import json


class NER:
    def __init__(self, query):
        self.query = query
        modelfilepath = "../models/NER" 
        self.loaded_nlp = spacy.load(modelfilepath) 
        self.entities = self.extractNER()
        
    def extractNER(self):
        # Loading the text processing function:
        sent = self.query
        entities = {}
        
        doc = self.loaded_nlp(sent)

        for ent in doc.ents:
            entities[ent.text] = ent.label_
        
        return entities
    