import unittest
import HTTPRequestClass as http


class MyTestCase(unittest.TestCase):

    def test_GETHappyPath(self):
        GETTest = http.HTTPRequest('GET')
        GETTest.setApiEndpoint("http://hackathon.siim.org/fhir")
        GETTest.setResource("Patient")
        GETTest.setHeadersDict({'content-type': 'application/json'})
        GETTest.setIdentifiersDict({'gender': 'male', '_id': 'siimjoe'})
        GETTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
        url = GETTest.constructRequestUrl()

        assert (GETTest.getResource() == "Patient")
        assert (GETTest.getHeadersDict() == {'content-type': 'application/json'})
        assert (GETTest.getApiEndpoint() == "http://hackathon.siim.org/fhir")
        assert (GETTest.getIdentifiersDict() == {'gender': 'male', '_id': 'siimjoe'})
        assert (GETTest.toString() == "apiEndpoint=http://hackathon.siim.org/fhir, requestType=GET, resource=Patient, headersDict={'content-type': 'application/json'}, identifiersDict={'gender': 'male', '_id': 'siimjoe'}")
        assert (url == "http://hackathon.siim.org/fhir/Patient/?gender=male&_id=siimjoe")
        assert (GETTest.executeRequest().status_code == 200)

    def test_POSTHappyPath(self):
        payload = {
            "resourceType": "Patient",
            "id": "siimnoah",
            "name": [{
                "family": "Asaria",
                "given": ["Noah", "J."]
            }],
            "gender": "male",
            "birthDate": "1997-12-29",
            "telecom": [{
                "system": "phone",
                "value": "(111) 123 1234",
                "use": "home"
            }],
            "address": [{
                "use": "home",
                "line": [
                    "123 Sunnyside Lane"
                ],
                "city": "PleasantVille",
                "state": "IL",
                "postalCode": "12345"
            }],
            "search": {
                "mode": "match"
            }
        }
        POSTTest = http.HTTPRequest('POST')
        POSTTest.setApiEndpoint("http://hackathon.siim.org/fhir")
        POSTTest.setResource("Patient")
        POSTTest.setHeadersDict({'content-type': 'application/json'})
        POSTTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
        POSTTest.setPayload(payload)
        url = POSTTest.constructRequestUrl()

        assert (url == "http://hackathon.siim.org/fhir/Patient/")
        assert (POSTTest.executeRequest().status_code == 201)

    def test_defaultGETRequestHappyPath(self):
        GETDefault = http.createDefaultPatientGETRequest()
        GETDefault.setIdentifiersDict({'gender': 'male' , '_id' : 'siimjoe'})

        assert (GETDefault.getResource() == "Patient")
        assert (GETDefault.getHeadersDict() == {'content-type': 'application/json'})
        assert (GETDefault.getApiEndpoint() == "http://hackathon.siim.org/fhir")
        assert (GETDefault.getIdentifiersDict() == {'gender': 'male', '_id': 'siimjoe'})
        assert (GETDefault.toString() == "apiEndpoint=http://hackathon.siim.org/fhir, requestType=GET, resource=Patient, headersDict={'content-type': 'application/json'}, identifiersDict={'gender': 'male', '_id': 'siimjoe'}")
        assert (GETDefault.getFullURL() == "http://hackathon.siim.org/fhir/Patient/?gender=male&_id=siimjoe")
        assert (GETDefault.executeRequest().status_code == 200)

    def test_defaultPOSTRequestHappyPath(self):
        payload = {
            "resourceType": "Patient",
            "id": "siimnoah",
            "name": [{
                "family": "Asaria",
                "given": ["Noah", "J."]
            }],
            "gender": "male",
            "birthDate": "1997-12-29",
            "telecom": [{
                "system": "phone",
                "value": "(111) 123 1234",
                "use": "home"
            }],
            "address": [{
                "use": "home",
                "line": [
                    "123 Sunnyside Lane"
                ],
                "city": "PleasantVille",
                "state": "IL",
                "postalCode": "12345"
            }],
            "search": {
                "mode": "match"
            }
        }
        POSTDefault = http.createDefaultPatientPOSTRequest()
        POSTDefault.setPayload(payload)
        POSTDefault.executeRequest()

        assert (POSTDefault.getFullURL() == "http://hackathon.siim.org/fhir/Patient/")
        assert (POSTDefault.executeRequest().status_code == 201)

    def test_Allergies(self):
        GETTest = http.HTTPRequest('GET')
        GETTest.setApiEndpoint("http://hackathon.siim.org/fhir")
        GETTest.setResource("AllergyIntolerance")
        GETTest.setHeadersDict({'content-type': 'application/json'})
        GETTest.setIdentifiersDict({"code" : ['aspirin', 'Bicillin L-A']})
        GETTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
        GETTest.executeRequest()


def main():
    MyTestCase().test_defaultGETRequestHappyPath()
    MyTestCase().test_defaultPOSTRequestHappyPath()
    MyTestCase().test_GETHappyPath()
    MyTestCase().test_POSTHappyPath()
    MyTestCase().test_Allergies()

if __name__ == '__main__':
    unittest.main()
