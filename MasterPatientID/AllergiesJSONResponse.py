import json
import logging
logFormat = '%(asctime)s: %(levelname)s: %(message)s @ %(filename)s : %(funcName)s: --> line %(lineno)d'
logging.basicConfig(filename='logs/log.txt', format=logFormat,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

class AllergiesJSONResponse:
    def __init__(self, response=None):
        if response is None:
            response={}
            logging.info("No response passed as argument.")
        else:
            try:
                logging.debug("response passed: ", response)
                self.response = response
                self.entries = self.getAllergyEntriesFromResponse(response)
                self.allergyDictionaries = self.getDictFromEntries()
                self.printAllergyDictionaries()
                logging.info("Created PatientJSONResponse object")
                logging.debug('patientDictionaries: %s', self.allergyDictionaries)
            except:
                logging.error("Could not initialize PatientJSONResponse!")

    def setResponse(self, resp):
        logging.debug("setResponse received parameter: %s", resp)
        self.response = resp

    def getResponse(self):
        logging.info("Inside getResponse()")
        return self.response

    def getAllergiesEntries(self):
        logging.debug("Allergy entries: %s", self.entries)
        return self.entries

    def getNumberOfAllergyEntries(self):
        logging.debug("Number of Allergy entries from GET Response: %d", len(self.entries))
        return len(self.entries)

    def getAllergyDictionaries(self):
        logging.debug("allergyDictionaries: %s", self.allergyDictionaries)
        print("Allergy dicts: ", self.allergyDictionaries)
        return self.allergyDictionaries

    def getAllergyEntriesFromResponse(self, response):
        entries=''
        try:
            json_data = json.loads(response.text)
            entries = json_data['entry']
            #print("ENTRIES: ", entries)
            logging.DEBUG("Entry: ", entries)
        except:
            logging.error("Could not parse entries from JSON response")
        return entries

    def printEntries(self):
        for entry in self.entries:
            print("\n\n", entry)

    def getDictFromEntries(self):
        dict = {}
        allergies = self.getAllergiesEntries()
        print("Allergies: ", allergies)
        try:
            for allergy in allergies:
                resource = allergy['resource']
                #print(resource['patient']['reference'].partition('/'))
                reference = resource['patient']['reference']
                patientName = reference.partition('/')[2] #The patient endpoint ids by patient name, so we extract that, in the form ('Patient', '/', 'siimjoe')

                id = patientName
                dict[id] = self.parseResource(resource)
        except:
            logging.error("Failed parsing patient dictionary from entries")
            print("ERROR: getDictFromEntries failed")
        return dict

    def parseResource(self, resource):
        d = {}
        try:
            results = []
            reactions = resource['reaction']
            substances = reactions[0]['substance']['coding']
            for substance in substances:
                #print("substance!", substance['display'])
                results.append(substance['code'])
            d['allergies'] = results
        except:
            #print("Error parsing substances")
            logging.warning("Error parsing substances")
        return d

    def printAllergyDictionaries(self):
        try:
            for id, info in self.allergyDictionaries.items():
                print("\nID: ", id)
                for field in info:
                    print(field + ":", info[field])
        except:
            logging.error("FAILED TO PRINT Allergies Entries")

def createAllergyJSONResponse(response):
    logging.info("Creating Allergies JSON Response Instance")
    return AllergiesJSONResponse(response)

