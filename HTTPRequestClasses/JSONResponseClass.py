import ResponsesFromFiles as FileResponder
import json
import logging
logging.basicConfig(filename='logs.txt', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

class PatientJSONResponse:
    def __init__(self, response=None):
        if response is None:
            response={}
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
        self.response = resp

    def getResponse(self):
        return self.response

    def getPatientEntries(self):
        return self.entries

    def getNumberOfPatientEntries(self):
        return len(self.entries)
    def getPatientDictionaries(self):
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
        try:
            nameList =  resource['name']
            d['given'] = nameList[1]['given'][0]
            d['family'] = nameList[0]['family']
        except:
            logging.error("Failed to parse names from resource")
            logging.error("nameList: %s", nameList)
        #get street address
        try:
            address = resource['address'][0]['line'][0]
            d['address'] = address
        except:
            logging.error("Failed to parse address from resource")
            logging.error("address: %s", address)
        #Get DOB, Gender
        try:
            dob = resource['birthDate']
            d['DOB'] = dob
            gender = resource['gender']
            d['gender'] = gender
        except:
            logging.error("Failed parsing birthDate, Gender")
            logging.error("birthDate: %s, gender %s",dob, gender)
        logging.info("Parsed resource from response into dict %s", d)
        return d

    def printPatientDictionaries(self):
        print(self.patientDictionaries)
        for id, info in self.patientDictionaries.items():
            print("\nID: ", id)

            for field in info:
                print(field + ":", info[field])



def createPatientJSONResponse(response):
    return PatientJSONResponse(response)

fileName = 'IsabellaJones-ReferralSummary.xml'
lookupIds = ['given', 'family']
IsabellaResponse = FileResponder.getPatientGETResponseFromDemographicsFile(fileName, lookupIds)
JSON = createPatientJSONResponse(IsabellaResponse)
#JSON.printPatientDictionaries()