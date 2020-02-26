from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import HTTPRequestClass as http
import ParserClass as parser
import requests
import json
import urllib
import logging
import time

payload = {
        "resourceType": "Patient",
        "id": "siimisabella",
        "identifier": [
          {
            "use": "usual",
            "system": "http://www.siim.org/",
            "value": "TCGA-17-Z058",
            "assigner": {
              "display": "TCIA"
            }
          }
        ],
        "active": "true",
        "name": [
          {
            "use": "official",
            "family": "Jones",
            "given": [
              "Isabella"
            ]
          },
          {
            "use": "usual",
            "given": [
              "Isabella"
            ]
          }
        ],
        "telecom": [
          {
            "use": "home"
          },
          {
            "system": "phone",
            "value": "(123) 123 1234",
            "use": "work"
          }
        ],
        "gender": "female",
        "birthDate": "1963-04-24",
        "deceasedBoolean": "false",
        "address": [
          {
            "use": "home",
            "line": [
              "1002 Healthcare Dr"
            ],
            "city": "Beaverton",
            "state": "OR",
            "postalCode": "97005"
          }
        ],
        "contact": [
          {
            "relationship": [
              {
                "coding": [
                  {
                    "system": "http://hl7.org/fhir/patient-contact-relationship",
                    "code": "partner"
                  }
                ]
              }
            ],
            "name": {
              "family": "du",
              "_family": {
                "extension": [
                  {
                    "url": "http://hl7.org/fhir/Profile/iso-21090#qualifier",
                    "valueCode": "VV"
                  }
                ]
              },
              "given": [
                "Bénédicte"
              ]
            },
            "telecom": [
              {
                "system": "phone",
                "value": "+33 (237) 998327"
              }
            ]
          }
        ],
        "managingOrganization": {
          "reference": "Organization/siim"
        }
    }

print("POSTING PAYLOAD ... ")
time.sleep(2)

isabellaPost = http.createDefaultPatientPOSTRequest()
isabellaPost.setPayload(payload)
response = isabellaPost.executeRequest()

print("ENDPOINT REQUESTED: ", isabellaPost.getFullURL())
print("RESPONSE RETURNED: ", response.status_code)
print("DATA POSTED: ")
time.sleep(1)
print(response.text)

time.sleep(3)
print("GETTING PAYLOAD: ")
time.sleep(1)

isabellaRequest = http.createDefaultPatientGETRequest()
isabellaDemographics = parser.Demographics('IsabellaJones-ReferralSummary.xml')
isabellaLookupIds = {'given' : isabellaDemographics.getFirstName()}
isabellaRequest.setIdentifiersDict(isabellaLookupIds)
response = isabellaRequest.executeRequest()

print("ENDPOINT REQUESTED: ", isabellaRequest.getFullURL())
print("GET RETURNED: ",response.status_code)
time.sleep(3)
print("DATA RECEIVED: ", response.text)


