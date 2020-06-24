# -*- coding: utf-8 -*-
"""
For testing the trained domain classifier
@author: yeshu
"""

query = "I want to login"

from DomainClassifierMakeClassification import DomainClassifier
dc = DomainClassifier(query)
domain = dc.makeClassification()
domain
