import DictionaryMatchClass as match
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import HTTPRequestClass as http
import ParserClass as parser
import JSONResponseClass as jsonResponse
import logging
import pathlib
import fuzzywuzzy
from fuzzywuzzy import fuzz

GETRequest = http.createDefaultPatientGETRequest()
LookupIds = {'family': 'siim'}
GETRequest.setIdentifiersDict(LookupIds)
response = GETRequest.executeRequest()
JSONResponse = jsonResponse.createPatientJSONResponse(response)
SIIM = JSONResponse.getPatientDictionaries()

file_path = 'TestingSuite/TestFiles/IsabellaJones-ReferralSummary.xml'
isabellaDemographics = parser.createNewDemographicsInstance(file_path)
CCD = isabellaDemographics.getDemographicDict()

print(match.formatMatchDict(match.unweightedDictionaryMatch(CCD, SIIM)))
sortStringDict({'siimjoe': 35.125, 'siimandy': 30.125, 'siimneela': 48.125, 'siimravi': 30.125, 'siimsally': 33.5})