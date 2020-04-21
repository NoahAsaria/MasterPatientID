import JSONResponseClass as jsonResponse
import ParserClass as parser
import HTTPRequestClass as http


#from os import path

def testPOST():
    payload = {
        "resourceType": "Patient",
        "id": "siimisabella",
        "identifier": [
          {
            "use": "usual",
            "system": "http://www.siim.org/",
            "value": "TCGA-17-Z058",
            "assigner": {
              "display": "TCIA"
            }
          }
        ],
        "active": "true",
        "name": [
          {
            "use": "official",
            "family": "HELLO WORLD",
            "given": [
              "Isabella"
            ]
          },
          {
            "use": "usual",
            "given": [
              "Isabella"
            ]
          }
        ],
        "telecom": [
          {
            "use": "home"
          },
          {
            "system": "phone",
            "value": "(123) 123 1256",
            "use": "work"
          }
        ],
        "gender": "female",
        "birthDate": "1954-03-23",
        "deceasedBoolean": "false",
        "address": [
          {
            "use": "home",
            "line": [
              "1002 Healthcare Dr."
            ],
            "city": "Beaverton",
            "state": "OR",
            "postalCode": "97005"
          }
        ],
        "contact": [
          {
            "relationship": [
              {
                "coding": [
                  {
                    "system": "http://hl7.org/fhir/patient-contact-relationship",
                    "code": "partner"
                  }
                ]
              }
            ],
            "name": {
              "family": "du",
              "_family": {
                "extension": [
                  {
                    "url": "http://hl7.org/fhir/Profile/iso-21090#qualifier",
                    "valueCode": "VV"
                  }
                ]
              },
              "given": [
                "Bénédicte"
              ]
            },
            "telecom": [
              {
                "system": "phone",
                "value": "+33 (237) 998327"
              }
            ]
          }
        ],
        "managingOrganization": {
          "reference": "Organization/siim"
        }
    }
    isabellaPost = http.createDefaultPatientPOSTRequest()
    isabellaPost.setPayload(payload)
    response = isabellaPost.executeRequest()
    print(response.text)

    ##TESTING Parsing local file --> GET request to SIIM Server based on specified 'given' (first name) parameter
    ##from CCD file --> Print dictionaries generated for each entry our GET response returned
def testGETPayloadFromFile():
    file_path = "TestFiles/IsabellaJones-ReferralSummary.xml"
    isabellaRequest = http.createDefaultPatientGETRequest()
    isabellaDemographics = parser.Demographics(file_path)
    isabellaLookupIds = {'given' : isabellaDemographics.getFieldFromDict('given')}
    isabellaRequest.setIdentifiersDict(isabellaLookupIds)
    response = isabellaRequest.executeRequest()
    JSONResponse = jsonResponse.createPatientJSONResponse(response)
    JSONResponse.printPatientDictionaries()

testPOST()
testGETPayloadFromFile()
