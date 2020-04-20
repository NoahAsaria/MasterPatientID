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
                logging.debug("response passed: ", response)
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
        entries=''
        try:
            json_data = json.loads(response.text)
            entries = json_data['entry']
            logging.DEBUG("Entry: ", entries)
        except:
            logging.error("Could not parse entries from JSON response")
        return entries

    def printEntries(self):
        for entry in self.entries:
            print("\n\n", entry)

    def getDictFromEntries(self):
        dict = {}
        patients = self.getPatientEntries()
        logging.debug("Patients: ", patients)
        try:
            for patient in patients:
                resource = patient['resource']
                id = resource['id']
                dict[id] = self.parseResource(resource)
        except:
            logging.error("Failed parsing patient dictionary from entries")
            print("ERROR: getDictFromEntries failed")
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
            logging.warning("Failed to parse names from resource")
            logging.warning("nameList: %s", nameList)
        #get street address
        try:
            address = resource['address'][0]['line'][0]
            d['address'] = address
            logging.debug("address: %s", address)
        except:
            logging.warning("Failed to parse address from resource")
            logging.warning("address parsed: %s", address)
        #Get DOB, Gender
        try:
            dob = resource['birthDate']
            d['birthtime'] = dob
            gender = resource['gender']
            d['gender'] = gender
            logging.debug("date of birth parsed: %s", dob)
            logging.debug("gender parsed: %s", gender)
        except:
            logging.warning("Failed parsing birthDate, Gender")
            logging.warning("birthDate: %s, gender %s",dob, gender)
        #Get city, state, postalCode
        try:
            state = resource['address'][0]['state']
            d['state'] = state
            city = resource['address'][0]['city']
            d['city'] = city
            zip = resource['address'][0]['postalCode']
            d['postalcode'] = zip
        except:
            logging.warning("Failed parsing state, city, zip", state, city)
        logging.debug("Parsed resource from response into dict %s", d)
        #print("parseResource:" ,d)
        return d

    def printPatientDictionaries(self):
        try:
            for id, info in self.patientDictionaries.items():
                print("\nID: ", id)
                for field in info:
                    print(field + ":", info[field])
        except:
            logging.error("FAILED TO PRINT Patient Entries")

def createPatientJSONResponse(response):
    logging.info("Creating patient JSON Response Instance")
    return PatientJSONResponse(response)

