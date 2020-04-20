import xml.etree.ElementTree as ET
import csv
import pandas as pd
import HTTPRequestClass as http
import ParserClass as parser
import PatientJSONResponseClass as jsonResponse
import logging
import operator
import pathlib

import fuzzywuzzy
from fuzzywuzzy import fuzz
logFormat = '%(asctime)s: %(levelname)s: %(message)s @ %(filename)s : %(funcName)s: --> line %(lineno)d'
logging.basicConfig(filename='logs/log.txt', format=logFormat,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


#CCDDict = CCD File data, SIIMDicts = parsed info from the server for each patient based on selected parameters
#Returns a dictionary with the match
def weightedPatientDictionaryMatch(CCDDict, SIIMDicts):
    global matchDict
    matchDict={}
    for key in SIIMDicts:
        sum = 0
        count = 0
        for field in SIIMDicts[key]:
            count+=1
            try:
                SIIMVal = str(SIIMDicts[key][field])
                CCDVal = str(CCDDict[field][0])
                ratio = fuzz.token_set_ratio(SIIMVal,CCDVal)
                if (field == "family" or field == "birthtime"): sum+=(1.2*ratio)
                else:
                    sum+=ratio
            except:
                print("Failed on SIIMVal:",SIIMVal,"CCDVal",CCDVal)
        matchDict[key] = sum/count
    return matchDict

#CCDDict = all allergies parsed from file, #SIIMDicts = parsed allergies from the server, assume that each entry represents its own patient
def unweightedAllergyDictionaryMatch(CCDDict, SIIMDicts):
    global matchDict
    matchDict = {}
    for entry in SIIMDicts:
        sum = 0
        count = 0
        for allergy in SIIMDicts[entry]['allergies']:
            print("allergy", allergy)


def formatMatchDict(matchDict):
    formatted = ""
    #print(matchDict)
    for key in matchDict:
        matchVal = round(matchDict[key],2)
        if (matchVal >= 80):
            formatted += (key + ": " + "<strong><font color=#8BEC21>" + str(matchVal) + "%" + "<br></strong></font>")
        else:
            formatted+= (key + ": " + "<strong>" + str(matchVal) + "%" + "<br></strong>")
    return formatted

#Helper functions
def formatJSONDicts(JSONDict):
    result = ""
    for key in JSONDict:
        result +=(key + ": " + str(JSONDict[key]) + "<br><br>")
    return result

def sortStringDict(d):
    for key in d:
        d[key] = float(d[key])
        #print(d[key])
    sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
    #print("sorted: ",sorted_d)
    return dict(sorted_d)

