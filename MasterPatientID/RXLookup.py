import json
import xml
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import pathlib
import requests

global commonCodes
commonCodes={}
commonCodes['bicillin l-a'] = '215674'
commonCodes['aspirin'] = '1191'
commonCodes['codeine phosphate'] = '2672'
commonCodes['ALLERGENIC EXTRACT, PENICILLIN'] = '314422'
commonCodes['']=""

def lookup(DisplayName):
    try:
        return commonCodes[DisplayName.lower()]
    except:
        print("Wasn't in dictionary!")
    lookupUrl = "http://rxnav.nlm.nih.gov/REST/rxcui?name="+DisplayName
    response = requests.get(lookupUrl)
    soup = BeautifulSoup(response.content, features='lxml')
    code = soup.rxnormid.string
    print(code)
    commonCodes[DisplayName] = code
    return code

def getAllergyNameFromCode(code):
    try:
        return list(commonCodes.keys())[list(commonCodes.values()).index(code)]
    except:
        return code
