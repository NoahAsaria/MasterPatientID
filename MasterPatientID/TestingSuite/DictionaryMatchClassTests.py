import DictionaryMatcher as match
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import HTTPRequest as http
import CCDParser as parser
import PatientJSONResponse as jsonResponse
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

print(match.formatMatchDict(match.weightedPatientDictionaryMatch(CCD, SIIM)))
match.sortStringDict({'siimjoe': 35.125, 'siimandy': 30.125, 'siimneela': 48.125, 'siimravi': 30.125, 'siimsally': 33.5})