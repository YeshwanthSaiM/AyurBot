"""
testing Intent classification
"""
# libraries:
from IntentClassifierMakeClassification import IntentClassifier

domain = "Social"
query = "Can you register"

ic = IntentClassifier(query, domain)

ic.intent