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

def lookup(DisplayName):
    try:
        return commonCodes[DisplayName.lower()]
    except:
        print("Wasn't in dictionary!")
    lookupUrl = "http://rxnav.nlm.nih.gov/REST/rxcui?name="+DisplayName
    print("lookupUrl: ", lookupUrl)
    response = requests.get(lookupUrl)
    soup = BeautifulSoup(response.content, features='lxml')
    print(soup.rxnormid.string)
    return soup.rxnormid.string
