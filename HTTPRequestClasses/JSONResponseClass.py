from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import HTTPRequestClass as http
import ParserClass as parser
import ResponsesFromFiles as responses
import requests
import json
import urllib
import logging
import time

class PatientJSONResponse:
    def __init__(self, response=None):
        if response is None:
            response={}
        else:
            try:
                self.response = response
                self.entries = self.getPatientEntriesFromResponse(response)
                self.patientDictionaries = self.getDictFromEntries()
            except:
                print("Failed to extract patient entries, dictionaries!")

    def setResponse(self, resp):
        self.response = resp

    def getResponse(self):
        return self.response

    def getPatientEntries(self):
        return self.entries

    def getNumberOfPatientEntries(self):
        return len(self.entries)
    def getPatientDictionaries(self):
        return self.patientDictionaries

    def getPatientEntriesFromResponse(self, response):
        json_data = json.loads(response.text)
        entries = json_data['entry']
        return entries

    def printEntries(self):
        for entry in self.entries:
            print("\n\n", entry)

    def getDictFromEntries(self):
        dict = {}
        patients = self.entries
        for patient in patients:
            resource = patient['resource']
            id = resource['id']
            dict[id] = self.parseResource(resource)
        return dict

    def parseResource(self, resource):
        d = {}
        #get first and last names
        try:
            nameList =  resource['name']
            d['given'] = nameList[1]['given'][0]
            d['family'] = nameList[0]['family']
        except:
            print("Failed parsing patient names from resource!", nameList)
            print("Resource: ", resource)
        #get street address
        try:
            address = resource['address'][0]['line'][0]
            d['address'] = address
        except:
            print("Failed parsing address from resource!", address)
            print("Resource", resource)
        #Get DOB, Gender
        try:
            dob = resource['birthDate']
            d['DOB'] = dob
            gender = resource['gender']
            d['gender'] = gender
        except:
            print("Failed parsing birthDate, Gender", dob, gender)
            print("Resource", resource)
        return d

    def printPatientDictionaries(self):
        print(self.patientDictionaries)
        for id, info in self.patientDictionaries.items():
            print("\nID: ", id)

            for field in info:
                print(field + ":", info[field])



def createPatientJSONResponse(response):
    return PatientJSONResponse(response)

#fileName = 'IsabellaJones-ReferralSummary.xml'
#lookupIds = ['given', 'family']
#IsabellaResponse = responses.getPatientGETResponseFromDemographicsFile(fileName, lookupIds)
#JSON = createPatientJSONResponse(IsabellaResponse)
#JSON.printPatientDictionaries()