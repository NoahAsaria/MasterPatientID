

from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import csv
import pandas as pd

class DemographicsData:
    def __init__(self, filepath=None):
        if filepath is None:
            print("Please pass in a local file path in the format filename.xml")
        
def getRoot(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root

def parseDemographicDataToCSV(file):  
    root = getRoot(file)
    DemographicsCSV = open('demographic.csv', 'w')
    csvwriter = csv.writer(DemographicsCSV)
    headers = ["First Name", "Last Name", "Street Address", "City", "State", "Zip", "DOB", "Gender", "Race"]
    csvwriter.writerow(headers)
    infoList = parseDemographicsListFromRoot(root)
    csvwriter.writerow(infoList)
    DemographicsCSV.close()
    return 'demographic.csv'

def parseDemographicsDictFromRoot(root):
    names = {}
    for name in root.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given'):
        names.setdefault('firstname', []).append(name.text)
    #Parse last name(s)
    for name in root.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family'):
        names.setdefault('lastname', []).append(name.text)
    #Parse addresses
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}streetAddressLine'):
        names.setdefault('address', []).append(name.text)
    #Parse city
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}city'):
        names.setdefault('address', []).append(name.text)
    #Parse state
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}state'):
        names.setdefault('state', []).append(name.text)
    #Parse postal code
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}postalCode'):
        names.setdefault('postalcode', []).append(name.text)
    #Parse birthTime
    birth = root.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}birthTime')
    names['birthtime'] = birth.attrib["value"]
    #Parse gender
    gender = root.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}administrativeGenderCode')
    names['gender'] = gender.attrib["code"]
    #Parse race
    race = root.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}raceCode')
    names['race'] = race.attrib["displayName"]
    return names

def parseDemographicsListFromRoot(root):
    names = []
    #Parse first name(s)
    for name in root.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given'):
        names.append(name.text)
    #Parse last name(s)
    for name in root.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family'):
        names.append(name.text)
    #Parse addresses
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}streetAddressLine'):
        names.append(name.text)
    #Parse city
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}city'):
        names.append(name.text)
    #Parse state
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}state'):
        names.append(name.text)
    #Parse postal code
    for name in root.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}postalCode'):
        names.append(name.text)
    #Parse birthTime
    birth = root.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}birthTime')
    names.append(birth.attrib["value"])
    #Parse gender
    gender = root.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}administrativeGenderCode')
    names.append(gender.attrib["code"])
    #Parse race
    race = root.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}raceCode')
    names.append(race.attrib["displayName"])
    return names

def printCSV(csv):
    df = pd.read_csv(csv)
    print(df.head(1))

printCSV(parseDemographicDataToCSV('IsabellaJones-ReferralSummary.xml'))
dict1 = parseDemographicsDictFromRoot(getRoot('IsabellaJones-ReferralSummary.xml'))
print(dict1)


def getFirstName(d):
    try:
        return d['firstname'][0]
    except:
        print("Can't find first name field in dictionary")

def getLastName(d):
    try:
        return d['lastname'][0]
    except:
        print("Can't find last name field in dictionary")

dict1 = parseDemographicsDictFromRoot(getRoot('IsabellaJones-ReferralSummary.xml'))
print(getFirstName(dict1))

import requests
import json
import urllib
import logging

class HTTPRequest:
    def __init__(self,  requestType=None, apiEndpoint=None, resource=None, headersDict=None, identifiersDict=None):
        if requestType is None:
            self.requestType = ''
        else:
            self.requestType = requestType
        if apiEndpoint is None:
            self.apiEndpoint = ''
        else:
            self.apiEndpoint = apiEndpoint
        if resource is None:
            self.resource = ''
        else:
            self.resource = resource
        if headersDict is None:
            self.headersDict = {}
        else:
            self.headersDict = headersDict
        if identifiersDict is None:
            self.identifiersDict = {}
        else:
            self.identifiersDict = identifiersDict
        self.apiKey = None
    def setApiEndpoint(self, endpt):
        self.apiEndpoint = endpt
    def setApiKey(self, key):
        self.apiKey = key
    def setRequestType(self, request):
        self.requestType = request
    def setResource(self, res):
        self.resource = res
    def setHeadersDict(self, hd):
        self.headersDict = hd
    def setIdentifiersDict(self, id):
        self.identifiersDict = id
    def setPayload(self, p):
        self.payload = p;
        
    def getApiEndpoint(self):
        return self.apiEndpoint
    def getRequestType(self):
        return self.requestType
    def getResource(self):
        return self.resource
    def getHeadersDict(self):
        return self.headersDict
    def getIdentifiersDict(self):
        return self.identifiersDict
    def getPayload(self):
        return self.payload
    def toString(self):
        return "apiEndpoint=" + self.apiEndpoint + ", requestType=" + self.requestType + ", resource=" + self.resource +         ", headersDict=" + str(self.headersDict) + ", identifiersDict=" + str(self.identifiersDict)

    def constructRequestUrl(self):
        url = self.apiEndpoint + "/" + self.resource + "/?"
        req = self.requestType.lower()
        if (req == 'get'):
            try:
                for key,value in self.identifiersDict.items():
                    url += (key + "=" + value +"&")
            except:
                print("Invalid query parameters. Key =",key, ", Value =",value)
        return url
    
    def executeRequest(self, url1):
        req = self.requestType.lower()
        h = self.headersDict
        if (self.apiKey is not None):
            a = {'apikey': self.apiKey}
            h.update(a)
        if (req == 'get'):
            response = requests.get(url = url1, headers = h)
            return response
        elif (req == 'post'):
            response = requests.post(url = url1, headers = h, json = self.payload)
            return response
        else:
            return "Invalid request type"

    def executeRequest(self):
        url1 = self.constructRequestUrl()
        req = self.requestType.lower()
        h = self.headersDict
        if (self.apiKey is not None):
            a = {'apikey': self.apiKey}
            h.update(a)
        if (req == 'get'):
            response = requests.get(url = url1, headers = h)
            return response
        elif (req == 'post'):
            response = requests.post(url = url1, headers = h, json = self.payload)
            return response
        else:
            return "Invalid request type"
        
def createDefaultPatientGETRequest():
    GETTest = HTTPRequest('GET')
    GETTest.setApiEndpoint("http://hackathon.siim.org/fhir")
    GETTest.setResource("Patient")
    GETTest.setHeadersDict({'content-type': 'application/json'})
    GETTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
    return GETTest

def createDefaultPatientPOSTRequest():
    POSTTest = HTTPRequest('POST')
    POSTTest.setApiEndpoint("http://hackathon.siim.org/fhir")
    POSTTest.setResource("Patient")
    POSTTest.setHeadersDict({'content-type': 'application/json'})
    POSTTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
    return POSTTest

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
isabellaPost = createDefaultPatientPOSTRequest()
isabellaPost.setPayload(payload)
response = isabellaPost.executeRequest()
print(response.text, "response", response.status_code)


isabellaRequest = createDefaultPatientGETRequest()
isabellaDemoDict = parseDemographicsDictFromRoot(getRoot('IsabellaJones-ReferralSummary.xml'))
isabellaLookupIds = {'given' : getFirstName(isabellaDemoDict)}
isabellaRequest.setIdentifiersDict(isabellaLookupIds)
response = isabellaRequest.executeRequest().text
print(response)


