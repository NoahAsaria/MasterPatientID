import PatientJSONResponseClass as jsonResponse
import ParserClass as parser
import HTTPRequestClass as http


POSTTest = http.HTTPRequest('POST')
payload1 = {
  "resourceType": "AllergyIntolerance",
  "id": "ai83726462664827",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Penicillin - Hives and Airway compromise</div>"
  },
  "recordedDate": "2008-05-24",
  "patient": {
    "reference": "Patient/siimneela"
  },
  "reporter": {
    "reference": "Practitioner/siimjoe"
  },

  "status": "confirmed",
  "criticality": "high",
  "type": "allergy",
  "category": ["medication"],
  "reaction": [
    {
        "substance": {
            "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "1191",
                "display": "ASPIRIN"
            },
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "215674",
                "display": "Bicillin L-A"
            }
            ],
        },
      "manifestation": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "247472004",
              "display": "Hives"
            },
            {
              "system": "http://snomed.info/sct",
              "code": "44416002",
              "display": "Airway constriction"
            }
          ]
        }
      ]
    }
  ]
}


payload2 = {
  "resourceType": "AllergyIntolerance",
  "id": "ai83726462664827",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Penicillin - Hives and Airway compromise</div>"
  },
  "recordedDate": "2008-05-24",
  "patient": {
    "reference": "Patient/siimsally"
  },
  "reporter": {
    "reference": "Practitioner/siimmd"
  },
  "substance": {
      "coding": [
      {
        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
        "code": "314422",
        "display": "ALLERGENIC EXTRACT, PENICILLIN"
      }
    ]
  },
  "status": "confirmed",
  "criticality": "high",
  "type": "allergy",
  "category": ["medication"],
  "reaction": [
    {
      "manifestation": [
        {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "247472004",
              "display": "Hives"
            },
            {
              "system": "http://snomed.info/sct",
              "code": "44416002",
              "display": "Airway constriction"
            }
          ]
        }
      ]
    }
  ]
}

#Upload test #1: FHIR Accurate
POSTTest.setApiEndpoint("http://hackathon.siim.org/fhir")
POSTTest.setResource("AllergyIntolerance")
POSTTest.setHeadersDict({'content-type': 'application/json'})
POSTTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
POSTTest.setPayload(payload1)
POSTTest.executeRequest()

#Upload test #2: Original
#POSTTest.setPayload(payload2)
#POSTTest.executeRequest()
GETTest = http.HTTPRequest('GET')
GETTest.setApiEndpoint("http://hackathon.siim.org/fhir")
GETTest.setResource("AllergyIntolerance")
GETTest.setHeadersDict({'content-type': 'application/json'})
GETTest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')
print("text: ", GETTest.executeRequest().text)