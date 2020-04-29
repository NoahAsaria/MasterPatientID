import unittest
import PatientJSONResponse as jsonResponse
import AllergiesJSONResponse as allergyJSONResponse
import HTTPRequest as http


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

    def testCreateAllergiesJSONResponse(self):
        GETTest = http.HTTPRequest('GET')
        GETTest.setApiEndpoint("http://hackathon.siim.org/fhir")
        GETTest.setResource("AllergyIntolerance")
        GETTest.setHeadersDict({'content-type': 'application/json'})
        GETTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
        response = GETTest.executeRequest()
        #print("response text: ", response.text)
        JSONResponse = allergyJSONResponse.createAllergyJSONResponse(response)

        assert(1 == 1)
if __name__ == '__main__':
    unittest.main()
