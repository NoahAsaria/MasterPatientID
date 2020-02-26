import requests
import json
import urllib
import logging


class HTTPRequest:
    def __init__(self, requestType=None, apiEndpoint=None, resource=None, headersDict=None, identifiersDict=None):
        if requestType is None:
            self.requestType = ''
        else:
            self.requestType = requestType
        if apiEndpoint is None:
            self.apiEndpoint = ''
        else:
            self.apiEndpoint = apiEndpoint
        if resource is None:
            self.resource = ''
        else:
            self.resource = resource
        if headersDict is None:
            self.headersDict = {}
        else:
            self.headersDict = headersDict
        if identifiersDict is None:
            self.identifiersDict = {}
        else:
            self.identifiersDict = identifiersDict
        self.apiKey = None
        self.fullUrl = self.constructRequestUrl()

    def setApiEndpoint(self, endpt):
        self.apiEndpoint = endpt

    def setApiKey(self, key):
        self.apiKey = key

    def setRequestType(self, request):
        self.requestType = request

    def setResource(self, res):
        self.resource = res

    def setHeadersDict(self, hd):
        self.headersDict = hd

    def setIdentifiersDict(self, id):
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
        return self.fullUrl
    def toString(self):
        return "apiEndpoint=" + self.apiEndpoint + ", requestType=" + self.requestType + ", resource=" + self.resource + ", headersDict=" + str(
            self.headersDict) + ", identifiersDict=" + str(self.identifiersDict)

    def constructRequestUrl(self):
        url = self.apiEndpoint + "/" + self.resource + "/?"
        req = self.requestType.lower()
        if (req == 'get'):
            try:
                for key, value in self.identifiersDict.items():
                    url += (key + "=" + value + "&")
            except:
                print("Invalid query parameters. Key =", key, ", Value =", value)
        if (url[-1] == '&'): url = url[:-1]  # remove trailing &
        if (url[-1] == '?'): url = url[:-1]  # remove trailing ?
        self.fullUrl = url
        return url

    def executeRequest(self, url1):
        req = self.requestType.lower()
        h = self.headersDict
        if (self.apiKey is not None):
            a = {'apikey': self.apiKey}
            h.update(a)
        if (req == 'get'):
            response = requests.get(url=url1, headers=h)
            return response
        elif (req == 'post'):
            response = requests.post(url=url1, headers=h, json=self.payload)
            return response
        else:
            return "Invalid request type"

    def executeRequest(self):
        url1 = self.constructRequestUrl()
        req = self.requestType.lower()
        h = self.headersDict
        if (self.apiKey is not None):
            a = {'apikey': self.apiKey}
            h.update(a)
        if (req == 'get'):
            response = requests.get(url=url1, headers=h)
            return response
        elif (req == 'post'):
            response = requests.post(url=url1, headers=h, json=self.payload)
            return response
        else:
            return "Invalid request type"


def createDefaultPatientGETRequest():
    GETTest = HTTPRequest('GET')
    GETTest.setApiEndpoint("http://hackathon.siim.org/fhir")
    GETTest.setResource("Patient")
    GETTest.setHeadersDict({'content-type': 'application/json'})
    GETTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
    return GETTest


def createDefaultPatientPOSTRequest():
    POSTTest = HTTPRequest('POST')
    POSTTest.setApiEndpoint("http://hackathon.siim.org/fhir")
    POSTTest.setResource("Patient")
    POSTTest.setHeadersDict({'content-type': 'application/json'})
    POSTTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
    return POSTTest
