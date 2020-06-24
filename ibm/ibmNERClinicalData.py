"""
This file trains and extracts the named entities from the query
Synd NLP
@author: yeshu
"""


import numpy as np
import json
from ibm_whcs_sdk import annotator_for_clinical_data as acd
from ibm_cloud_sdk_core.authenticators.iam_authenticator import IAMAuthenticator

key = "3u7qYytw9Mzc0i-ABMZvjBzcYJFY4YRCn-UrnjVjNLCq"
service = acd.AnnotatorForClinicalDataV1(
   authenticator=IAMAuthenticator(apikey=key),
   version="2020-06-22"
)
url = "https://us-east.wh-acd.cloud.ibm.com/wh-acd/api"
service.set_service_url(url)
anno_ner = acd.Annotator(name="symptom_disease")
flow_arr = [
  acd.FlowEntry(annotator=anno_ner)
]
flow = acd.Flow(elements=flow_arr, async_=False)


class ibmNER:
    def __init__(self, query):
        self.query = query
        self.entities = self.extractNER()
        
    def extractNER(self):
        # Loading the text processing function:
        sent = self.query
        entities = {}
        
        resp = service.analyze(sent, flow)
        res = resp.to_dict()
        for key,val in res.items():
            # print(key)
            for obj in val:
                # print(obj['coveredText'])
                entities[obj['coveredText']] = 'disease'
        return entities

# t =ibmNER("I need treatment for headache")