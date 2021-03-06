import xml.etree.ElementTree as ET
import bs4 as bs
import csv
import lxml
import pandas as pd
import logging
import pathlib
import re
logFormat = '%(asctime)s: %(levelname)s: %(message)s @ %(filename)s : %(funcName)s: --> line %(lineno)d'
logging.basicConfig(filename='logs/log.txt', format=logFormat,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


class Demographics:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = ''
            logging.warning("Demographics: No filepath was entered!")
            print("Please pass in a local file path in the format filename.xml")
        else:
            self.filepath=filepath
            self.root = self.getRoot()
            self.demographicDict = self.getDemographicDict()
            self.allergiesDict = self.getAllergiesDict()
            logging.debug("Demographics dictionary parsed: %s", self.demographicDict)

    def setFilePath(self, path):
        logging.debug("File path passed in: %s", path)
        self.filepath = path
        logging.info("Set filepath")

    def getFilePath(self):
        return str(self.filepath)

    def getRoot(self):
        try:
            fileType = pathlib.Path(self.getFilePath()).suffix.lower()
            #logging.debug("filetype: ", fileType)
            if (fileType == '.xml' or fileType == '.ccd'):
                tree = ET.parse(self.getFilePath())
                root = tree.getroot()
                logging.debug("Root parsed: %s", root)
                return root
            else:
                logging.error("File-type must be .XML or .CCD! Given: ", fileType)
        except:
            logging.ERROR("Unable to parse root! -- filepath given: ", self.getFilePath())
        return 0

    def getSoupFromFile(self):
        try:
            infile = open(self.filepath,"r")
            contents = infile.read()
            logging.info("Before Soup!")
            soup = bs.BeautifulSoup(contents,'xml')
            #logging.info("Soup: ", soup)
            logging.info("After soup!")
            infile.close()
        except:
            logging.ERROR("Couldn't get soup from file!")

        return soup

    def writeToCSV(self):
        root = self.getRoot()
        DemographicsCSV = open('demographic.csv', 'w')
        csvwriter = csv.writer(DemographicsCSV)
        headers = ["First Name", "Last Name", "Street Address", "City", "State", "Zip", "DOB", "Gender", "Race"]
        csvwriter.writerow(headers)
        infoList = self.getListFromRoot()
        logging.debug("Wrote to CSV: %s", infoList)
        csvwriter.writerow(infoList)
        DemographicsCSV.close()
        return 'demographic.csv'

    def getDemographicDict(self):
        #print(self.getRoot())
        try:
            names = {}
            root1 = self.root
            for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given'):
                names.setdefault('given', []).append(name.text)
            #Parse last name(s)
            for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family'):
                names.setdefault('family', []).append(name.text)
            #Parse addresses
            for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}streetAddressLine'):
                names.setdefault('address', []).append(name.text)
            #Parse city
            for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}city'):
                names.setdefault('city', []).append(name.text)
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
            names['gender'] = gender.attrib["displayName"]
            #Parse race
            #race = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}raceCode')
            #names['race'] = race.attrib["displayName"]
            return names
        except:
            logging.WARNING("Could not parse demographics dict!")
        return 0

    def getAllergiesDict(self):
        names = {}
        try:
            root1 = self.root
            soup = self.getSoupFromFile()
            names['allergies'] = parseOtherElements(soup,"allergy")
            names['immunizations'] = parseOtherElements(soup, "immun")
            names['procedures'] = parseOtherElements(soup, "proc")
            #names.setdefault('immunizations', []).append(parseOtherElements(soup,"immun")) # Parse Immunizations
            #names.setdefault('procedures', []).append(parseOtherElements(soup, "proc"))  # Parse allergies
            logging.info(names)
            return names
        except:
            logging.warning("Could not parse allergies!" + str(names))

    def getListFromRoot(self):
        names = []
        root1 = self.root
        #Parse first name(s)
        try:
            for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}given'):
                names.append(name.text)
        except:
            logging.warning("Failed to parse first name entry: %s", name.text)
        #Parse last name(s)
        try:
            for name in root1.findall('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}name/{urn:hl7-org:v3}family'):
                names.append(name.text)
        except:
            logging.warning("Failed to parse last name entry: %s", name.text)
        #Parse addresses
        try:
            for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}streetAddressLine'):
                names.append(name.text)
        except:
            logging.warning("Failed to parse address entry: %s", name.text)
        #Parse city
        try:
            for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}city'):
                names.append(name.text)
        except:
            logging.warning("Failed to parse city entry: %s", name.text)
        #Parse state
        try:
            for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}state'):
                names.append(name.text)
        except:
            logging.warning("Failed to parse state entry: %s", name.text)
        #Parse postal code
        try:
            for name in root1.findall('.//{urn:hl7-org:v3}patientRole/{urn:hl7-org:v3}addr/{urn:hl7-org:v3}postalCode'):
                names.append(name.text)
        except:
            logging.warning("Failed to parse postal code entry: %s", name.text)
        #Parse birthTime
        try:
            birth = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}birthTime')
            names.append(birth.attrib["value"])
        except:
            logging.warning("Failed to parse birthtime: %s", birth.attrib["value"])
        #Parse gender
        try:
            gender = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}administrativeGenderCode')
            #print("GENDER DISPLAY", gender.attrib["displayName"])
            names.append(gender.attrib["displayName"])
        except:
            logging.warning("Failed to parse gender: %s", gender.attrib["code"])
        #Parse race -- Note, we're ignoring this for now because the SIIM Server doesn't match!
        try:
            race = root1.find('.//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}raceCode')
            #names.append(race.attrib["displayName"])
        except:
            logging.warning("couldn't find race!")
            #logging.warning("Failed to parse race: %s", race.attrib["displayName"])
        logging.debug("dictionary parsed from file %s: %s", self.filepath, names)
        return names

    def printCSV(csv):
        df = pd.read_csv(csv)
        print(df.head(1))
        logging.info("CSV Printed")

    def getFieldFromDemographicDict(self, field):
        d = self.demographicDict
        try:
            if isinstance(d[field], list):
                logging.info("Field %s is in list format, returning %s", field, d[field][0])
                return d[field][0]
            else:
                logging.info("Field %s is not a list, returning %s", field, d[field])
                return d[field]
        except:
            logging.error("Can't find field in dict!")

def createNewDemographicsInstance(filepath):
    return Demographics(filepath)


#Helper:
def parseOtherElements(soup,element):
    list1 = []
    tabled = soup.find_all('tr', {'ID':re.compile(element)})
    for each in tabled:
        temp = str(each.get_text()).split('\n')
        list1.append(temp[1])
    return list1

