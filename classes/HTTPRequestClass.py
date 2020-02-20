import requests
import json
import urllib
import logging

#Refer to https://stackoverflow.com/questions/4841782/python-constructor-and-default-value
#HTTPRequest(apiEndpoint, requestType, resource, headersDict, identifiersDict):
#apiEndpoint = http://hackathon.siim.org/fhir/
#requestType = POST/GET/PUT/...
#resource = Patient (endpoint becomes apiEndpoint/resource)
#headersDict = HEADERS = {'content-type': 'application/json', 'apikey': API_KEY}
#identifiersDict = {"id": "siimjoe", "name": "joseph", ...}
#apiKey must be passed in via setApiKey
class HTTPRequest:
    def __init__(self, apiEndpoint=None, requestType=None, resource=None, headersDict=None, identifiersDict=None):
        if apiEndpoint is None:
            self.apiEndpoint = ''
        else:
            self.apiEndpoint = apiEndpoint
        if requestType is None:
            self.requestType = ''
        else:
            self.requestType = requestType
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
    def setApiEndpoint(self, endpt):
        self.apiEndpoint = endpt
    def setApiKey(self, key):
        self.apiKey = key
        print(self.apiKey)
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
    def toString(self):
        return "apiEndpoint=" + self.apiEndpoint + ", requestType=" + self.requestType + ", resource=" + self.resource + \
        ", headersDict=" + str(self.headersDict) + ", identifiersDict=" + str(self.identifiersDict)

    #constructRequestUrl(self): 
    #url = apiEndpoint/resourceType/?id1=key1&id2=key2&...
    #Ex: http://hackathon.siim.org//fhir/Patient/?_id=siimjoe&_resourceType=Patient
    def constructRequestUrl(self):
        url = self.apiEndpoint + "/" + self.resource + "/?"
        for key in self.identifiersDict:
            url += (key + "=" + self.identifiersDict[key] +"&")
        return url
    
    def executeRequest(self, url1):
        req = self.requestType.lower()
        h = self.headersDict
        if (self.apiKey is not None):
            a = {'apikey': self.apiKey}
            print(h.update(a))
        if (req == 'get'):
            response = requests.get(url = url1, headers = h)
            return response
        elif (req == 'post'):
            response = requests.post(url = url1, headers = h, json = self.payload)
            return response
        else:
            return "Invalid request type"
  
