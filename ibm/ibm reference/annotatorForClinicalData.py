# Analyze unstructured text via dynamic annotator flow defined in the request
from ibm_whcs_sdk import annotator_for_clinical_data as acd
from ibm_cloud_sdk_core.authenticators.iam_authenticator import IAMAuthenticator
key = "3u7qYytw9Mzc0i-ABMZvjBzcYJFY4YRCn-UrnjVjNLCq"
service = acd.AnnotatorForClinicalDataV1(
   authenticator=IAMAuthenticator(apikey=key),
   version="2020-06-22"
)
url = "https://us-east.wh-acd.cloud.ibm.com/wh-acd/api"
service.set_service_url(url)

text = "Patient has lung cancer, but did not smoke. She may consider chemotherapy as part of a treatment plan."

text = "I need treatment for Headache and body pains"

anno_cd = acd.Annotator(name="symptom_disease")
anno_neg = acd.Annotator(name="negation")

anno_ner = acd.Annotator(name="symptom_disease")
flow_arr = [
  acd.FlowEntry(annotator=anno_ner)
]

flow = acd.Flow(elements=flow_arr, async_=False)
resp = service.analyze(text, flow)

res = resp.to_dict()
for key,val in res.items():
    print(key)
    for obj in val:
        print(obj['coveredText'])



# named_entities  ,  
# list annotators
try:
       
   resp = service.get_annotators()
   rslt = resp.result
   for annotator in rslt:
       print(annotator)

except acd.ACDException as ex:
   print ("Error Code:", ex.code, " Message:", ex.message, " Correlation Id:", ex.correlation_id)