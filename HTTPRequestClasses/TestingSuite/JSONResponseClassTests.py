import unittest
import JSONResponseClass as jsonResponse
import HTTPRequestClass as http


class MyTestCase(unittest.TestCase):
    def testCreatePatientJSONResponse(self):
        GETRequest = http.createDefaultPatientGETRequest()
        LookupIds = {'_id': 'siimjoe'}
        GETRequest.setIdentifiersDict(LookupIds)
        response = GETRequest.executeRequest()
        JSONResponse = jsonResponse.createPatientJSONResponse(response)

        dict = {'siimjoe': {'given': 'Joe', 'family': 'SIIM ', 'address': '534 Erewhon St', 'birthtime': '1926-03-30', 'gender': 'male', 'state': 'Vic', 'city': 'PleasantVille', 'postalcode': '3999'}}
        assert(JSONResponse.getPatientDictionaries() == dict)
        assert(JSONResponse.getNumberOfPatientEntries() == 1)

if __name__ == '__main__':
    unittest.main()
