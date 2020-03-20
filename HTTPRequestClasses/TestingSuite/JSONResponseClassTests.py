import unittest
import HTTPRequestClass as http
import ParserClass as parser
import JSONResponseClass as jsonResponse

class MyTestCase(unittest.TestCase):
    def testCreatePatientJSONResponse(self):
        GETRequest = http.createDefaultPatientGETRequest()
        LookupIds = {'_id': 'siimjoe'}
        GETRequest.setIdentifiersDict(LookupIds)
        response = GETRequest.executeRequest()
        JSONResponse = jsonResponse.createPatientJSONResponse(response)

        dict = {'siimjoe': {'given': 'Joe', 'family': 'SIIM ', 'address': '534 Erewhon St', 'DOB': '1926-03-30', 'gender': 'male'}}
        assert(JSONResponse.getPatientDictionaries() == dict)
        assert(JSONResponse.getNumberOfPatientEntries() == 1)

if __name__ == '__main__':
    unittest.main()
