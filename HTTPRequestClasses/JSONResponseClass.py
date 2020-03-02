import ResponsesFromFiles as FileResponder
import json
import logging
logFormat = '%(asctime)s: %(levelname)s: %(message)s @ %(filename)s : %(funcName)s: --> line %(lineno)d'
logging.basicConfig(filename='logs/log.txt', format=logFormat,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

class PatientJSONResponse:
    def __init__(self, response=None):
        if response is None:
            response={}
            logging.info("No response passed as argument.")
        else:
            try:
                self.response = response
                self.entries = self.getPatientEntriesFromResponse(response)
                self.patientDictionaries = self.getDictFromEntries()
                logging.info("Created PatientJSONResponse object")
                logging.debug('patientDictionaries: %s', self.patientDictionaries)
            except:
                logging.error("Could not initialize PatientJSONResponse!")

    def setResponse(self, resp):
        logging.debug("setResponse received parameter: %s", resp)
        self.response = resp

    def getResponse(self):
        logging.info("Inside getResponse()")
        return self.response

    def getPatientEntries(self):
        logging.debug("Patient entries: %s", self.entries)
        return self.entries

    def getNumberOfPatientEntries(self):
        logging.debug("Number of patient entries from GET Response: %d", len(self.entries))
        return len(self.entries)

    def getPatientDictionaries(self):
        logging.debug("patientDictionaries: %s", self.patientDictionaries)
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
        logging.debug("resource: %s", resource)
        try:
            nameList =  resource['name']
            d['given'] = nameList[1]['given'][0]
            d['family'] = nameList[0]['family']
            logging.debug("nameList parsed: %s",nameList)
        except:
            logging.error("Failed to parse names from resource")
            logging.error("nameList: %s", nameList)
        #get street address
        try:
            address = resource['address'][0]['line'][0]
            d['address'] = address
            logging.debug("address: %s", address)
        except:
            logging.error("Failed to parse address from resource")
            logging.error("address parsed: %s", address)
        #Get DOB, Gender
        try:
            dob = resource['birthDate']
            d['DOB'] = dob
            gender = resource['gender']
            d['gender'] = gender
            logging.debug("date of birth parsed: %s", dob)
            logging.debug("gender parsed: %s", gender)
        except:
            logging.error("Failed parsing birthDate, Gender")
            logging.error("birthDate: %s, gender %s",dob, gender)
        logging.debug("Parsed resource from response into dict %s", d)
        return d

    def printPatientDictionaries(self):
        print(self.patientDictionaries)
        for id, info in self.patientDictionaries.items():
            print("\nID: ", id)
            for field in info:
                print(field + ":", info[field])



def createPatientJSONResponse(response):
    logging.info("Creating patient JSON Response Instance")
    return PatientJSONResponse(response)

