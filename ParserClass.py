#!/usr/bin/env python
# coding: utf-8

# In[26]:


from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import csv
import pandas as pd

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


# In[ ]:





# In[ ]:




