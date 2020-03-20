import requests
import json
import urllib
import logging
logFormat = '%(asctime)s: %(levelname)s: %(message)s @ %(filename)s : %(funcName)s: --> line %(lineno)d'
logging.basicConfig(filename='logs/log.txt', format=logFormat,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING)

class HTTPRequest:
    def __init__(self, requestType=None, apiEndpoint=None, resource=None, headersDict=None, identifiersDict=None):
        if requestType is None:
            logging.warning("No requestType specified as argument")
            self.requestType = ''
        else:
            self.requestType = requestType
        if apiEndpoint is None:
            logging.warning("No api endpoint specified as argument")
            self.apiEndpoint = ''
        else:
            self.apiEndpoint = apiEndpoint
        if resource is None:
            logging.debug("No resource specified as argument")
            self.resource = ''
        else:
            self.resource = resource
        if headersDict is None:
            logging.debug("No headers dictionary specified as argument")
            self.headersDict = {}
        else:
            self.headersDict = headersDict
        if identifiersDict is None:
            logging.warning("No identifiers specified")
            self.identifiersDict = {}
        else:
            self.identifiersDict = identifiersDict
        self.apiKey = None
        self.fullUrl = (self.constructRequestUrl())
        logging.debug("full url after initialization: %s", self.fullUrl)
        logging.info("After initialization, toString(): %s", self.toString())

    def setApiEndpoint(self, endpt):
        logging.debug("In set API Endpoint: %s", endpt)
        self.apiEndpoint = endpt
        logging.debug("New endpoint: %s", self.apiEndpoint)
    def setApiKey(self, key):
        logging.info("Setting API Key")
        self.apiKey = key

    def setRequestType(self, request):
        self.requestType = request

    def setResource(self, res):
        self.resource = res

    def setHeadersDict(self, hd):
        self.headersDict = hd

    def setIdentifiersDict(self, id):
        logging.debug("Setting identifiers dictionary as %s: ", id)
        self.identifiersDict = id

    def setPayload(self, p):
        self.payload = p;

    def getApiEndpoint(self):
        return self.apiEndpoint

    def getRequestType(self):
        return self.requestType

    def getResource(self):
        return self.resource

    def getHeadersDict(self):
        return self.headersDict

    def getIdentifiersDict(self):
        return self.identifiersDict

    def getPayload(self):
        return self.payload
    def getFullURL(self):
        return self.constructRequestUrl()

    def toString(self):
        return "apiEndpoint=" + self.apiEndpoint + ", requestType=" + self.requestType + ", resource=" + self.resource + ", headersDict=" + str(
            self.headersDict) + ", identifiersDict=" + str(self.identifiersDict)

    def constructRequestUrl(self):
        if (self.identifiersDict == '{}'): logging.WARNING("No identifiers present upon URL creation!")
        logging.debug("api endpoint: %s , resource: %s", self.apiEndpoint, self.resource)
        url = self.apiEndpoint + "/" + self.resource + "/?"
        req = self.requestType.lower()
        logging.debug("Lowercase request type: %s", req)
        if (req == 'get'):
            try:
                logging.debug("identifiersDict.items(): %s", self.identifiersDict.items())
                for key, value in self.identifiersDict.items():
                    url += (key + "=" + value + "&")
                    logging.debug("url appended: %s", url)
            except:
                print("Invalid query parameters. Key =", key, ", Value =", value)
        if (url[-1] == '&'):
            url = url[:-1]  # remove trailing & and ?
            logging.info("Removed trailing & character: %s")
            logging.debug("New Url after removing trailing characters %s", url)
        if (url[-1] == '?'):
            url = url[:-1]
            logging.info("Removed trailing ? character")
            logging.debug("New Url after removing trailing characters %s", url)
        logging.debug("url returned %s", url)
        return url

    def executeRequest(self, url1):
        req = self.requestType.lower()
        logging.info("Lowercase request parameter: %s", req)
        h = self.headersDict
        if (self.apiKey is not None):
            a = {'apikey': self.apiKey}
            h.update(a)
            logging.info("Added apikey to header dictionary")
        if (req == 'get'):
            response = requests.get(url=url1, headers=h)
            logging.info("GET Request response generated")
            return response
        elif (req == 'post'):
            response = requests.post(url=url1, headers=h, json=self.payload)
            logging.info("POST Request response generated")
            return response
        else:
            logging.error("Invalid request type: %s", req)

    def executeRequest(self):
        url1 = self.constructRequestUrl()
        req = self.requestType.lower()
        logging.info("Lowercase request type parameter: %s", req)
        h = self.headersDict
        if (self.apiKey is not None):
            a = {'apikey': self.apiKey}
            h.update(a)
            logging.info("Added apikey to header dictionary")
        if (req == 'get'):
            response = requests.get(url=url1, headers=h)
            logging.info("GET Request response generated")
            return response
        elif (req == 'post'):
            response = requests.post(url=url1, headers=h, json=self.payload)
            logging.info("GET Request response generated")
            return response
        else:
            logging.error("Invalid request type: %s", req)


def createDefaultPatientGETRequest():
    GETTest = HTTPRequest('GET', 'http://hackathon.siim.org/fhir', 'Patient')
    GETTest.setHeadersDict({'content-type': 'application/json'})
    GETTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
    return GETTest


def createDefaultPatientPOSTRequest():
    POSTTest = HTTPRequest('POST', 'http://hackathon.siim.org/fhir', 'Patient')
    POSTTest.setHeadersDict({'content-type': 'application/json'})
    POSTTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
    return POSTTest
