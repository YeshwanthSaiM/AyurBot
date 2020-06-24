# -*- coding: utf-8 -*-

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

authenticator = IAMAuthenticator('XWwJwthuLd_W0g4GnR3oW4e81q0k7X-J4FSq78PpulFW')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator)

url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/97935957-c16b-4933-8b15-07759651846e"
natural_language_understanding.set_service_url(url)

response = natural_language_understanding.analyze(
    text='I am suffering with headache and body pains I need treatment ',
    features=Features(
        entities=EntitiesOptions( limit=5),
        keywords=KeywordsOptions(limit=5))).get_result()

res = eval(json.dumps(response, indent=2))
print(res)