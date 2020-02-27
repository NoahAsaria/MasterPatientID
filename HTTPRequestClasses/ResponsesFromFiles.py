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

#GETSIIMResponseFromDemographicsFile(String filepath, List identifierList): Parses file, GET call to Patient resource
#with identifier parameters
    #identifierList: ex) {given, family, address} --> GET http://hackathon.../Patient/?given= &family= &address=
def getPatientGETResponseFromDemographicsFile(filepath, identifierList):
    idList = {}
    tempRequest = http.createDefaultPatientGETRequest()
    tempDemographics = parser.Demographics(filepath)
    try:
        for id in identifierList:
            idList.update({id : tempDemographics.getFieldFromDict(id)})
            print(id, tempDemographics.getFieldFromDict(id))
    except:
        print("Parser lookup failed!")
    tempRequest.setIdentifiersDict(idList)
    response = tempRequest.executeRequest()
    return response

def getPOSTPayloadToSIIMPatient(payload):
    tempRequest = http.createDefaultPatientPOSTRequest()
    tempRequest.setPayload(payload)
    response = tempRequest.executeRequest()
    return response

def getPatientEntriesFromResponse(response):
    json_data = json.loads(response.text)
    entries = json_data['entry']
    return entries

def printEntries(patients):
    for entry in patients:
        print("\n\n", entry)

fileName = 'IsabellaJones-ReferralSummary.xml'
lookupIds = ['given', 'family']
IsabellaResponse = getPatientGETResponseFromDemographicsFile(fileName, lookupIds)
patients = getPatientEntriesFromResponse(IsabellaResponse)