from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import HTTPRequestClass as http
import requests
import json
import urllib
import logging

class Demographics:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = ''
            print("Please pass in a local file path in the format filename.xml")
        else:
            self.filepath=filepath
            self.root = self.getRoot()
            self.demographicDict = self.getDemographicDict()

    def setFilePath(self, path):
        self.filepath = path

    def getFilePath(self):
        return self.filepath

    def getRoot(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        return root

    def writeToCSV(self):
        root = self.getRoot(self.filepath)
        DemographicsCSV = open('demographic.csv', 'w')
        csvwriter = csv.writer(DemographicsCSV)
        headers = ["First Name", "Last Name", "Street Address", "City", "State", "Zip", "DOB", "Gender", "Race"]
        csvwriter.writerow(headers)
        infoList = self.getListFromRoot(root)
        csvwriter.writerow(infoList)
        DemographicsCSV.close()
        return 'demographic.csv'

    def getDemographicDict(self):
        names = {}
        root1 = self.root
        for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given'):
            names.setdefault('firstname', []).append(name.text)
        #Parse last name(s)
        for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family'):
            names.setdefault('lastname', []).append(name.text)
        #Parse addresses
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}streetAddressLine'):
            names.setdefault('address', []).append(name.text)
        #Parse city
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}city'):
            names.setdefault('address', []).append(name.text)
        #Parse state
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}state'):
            names.setdefault('state', []).append(name.text)
        #Parse postal code
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}postalCode'):
            names.setdefault('postalcode', []).append(name.text)
        #Parse birthTime
        birth = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}birthTime')
        names['birthtime'] = birth.attrib["value"]
        #Parse gender
        gender = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}administrativeGenderCode')
        names['gender'] = gender.attrib["code"]
        #Parse race
        race = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}raceCode')
        names['race'] = race.attrib["displayName"]
        return names

    def getListFromRoot(self):
        names = []
        root1 = self.root
        #Parse first name(s)
        for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given'):
            names.append(name.text)
        #Parse last name(s)
        for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family'):
            names.append(name.text)
        #Parse addresses
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}streetAddressLine'):
            names.append(name.text)
        #Parse city
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}city'):
            names.append(name.text)
        #Parse state
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}state'):
            names.append(name.text)
        #Parse postal code
        for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}postalCode'):
            names.append(name.text)
        #Parse birthTime
        birth = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}birthTime')
        names.append(birth.attrib["value"])
        #Parse gender
        gender = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}administrativeGenderCode')
        names.append(gender.attrib["code"])
        #Parse race
        race = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}raceCode')
        names.append(race.attrib["displayName"])
        return names

    def printCSV(csv):
        df = pd.read_csv(csv)
        print(df.head(1))

    def getFirstName(self):
        d = self.demographicDict
        try:
            return d['firstname'][0]
        except:
            print("Can't find first name field in dictionary")

    def getLastName(self):
        d = self.demographicDict
        try:
            return d['lastname'][0]
        except:
            print("Can't find last name field in dictionary")

    def getAddress(self):
        d = self.demographicDict
        try:
            return d['lastname'][0]
        except:
            print("Can't find any addresses in dictionary")
