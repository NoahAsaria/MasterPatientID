#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
import urllib
import logging

url = "http://hackathon.siim.org/fhir/Patient"
API_ENDPOINT = "http://hackathon.siim.org/fhir/Patient"
API_KEY = "d6e052ee-18c9-4f3b-a150-302c998e804c"
HEADERS = {'content-type': 'application/json', 'apikey': API_KEY}


# In[ ]:


def createSession():
    s = requests.Session()
    s.auth = {''}
    
#getPatientResourceById(url, headers, field, value): sends a response to FHIR server querying patient's given field with value
#GET http://hackathon.siim.org/fhir/Patient/?_[field]=[value]
def getPatientResourceByField(url, headers, field, value):
    data = {'Accept': 'application/json'}
    url+=("/?_"+field+"="+value)
    print(url)
    response = requests.get(url=url, headers=headers)
    return response

def printResponseText(response):
    print(response.text)
    

createSession()
response = getPatientResourceByField(url,HEADERS,"id","82")
printResponseText(response)
print(response.status_code)


# In[ ]:


def postNewPatient(URL, headers, payload):
    response = requests.post(url=URL,headers=headers,json=payload) 
    return response

payload={
    "resourceType": "Patient",
    "id" : "siimnoah",
    "name": [{
            "family": "Asaria",
            "given": [ "Noah", "J."]
    }],
    "gender": "male",
    "birthDate": "1997-12-29",
    "telecom": [{
        "system": "phone",
        "value": "(111) 123 1234",
        "use": "home"
    }],
    "address": [{
        "use": "home",
        "line": [
            "123 Sunnyside Lane"
        ],
        "city": "PleasantVille",
        "state": "IL",
        "postalCode": "12345"
    }],
    "search": {
        "mode": "match"
    }
}

response = postNewPatient(url, HEADERS, payload)
print(response.text, ": ", response.status_code)


# In[ ]:


#Patient class attributes modeled off Patient resource available on SIIM server
class Patient:
    def set_id(self):
        self._id = id
        self._
    def set_


# In[ ]:




