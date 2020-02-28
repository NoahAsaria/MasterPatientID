import HTTPRequestClass as http
import ParserClass as parser
import JSONResponseClass as JSON
import logging
logging.basicConfig(filename='logs.txt', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

#GETSIIMResponseFromDemographicsFile(String filepath, List identifierList): Parses file, GET call to Patient resource
#with identifier parameters
    #identifierList: ex) {given, family, address} --> GET http://hackathon.../Patient/?given= &family= &address=
def getPatientGETResponseFromDemographicsFile(filepath, identifierList):
    logging.info("In getPatientGETResponseFromDemographicsFile class")
    idList = {}
    tempRequest = http.createDefaultPatientGETRequest()
    tempDemographics = parser.Demographics(filepath)
    try:
        for id in identifierList:
            idList.update({id : tempDemographics.getFieldFromDict(id)})
            #print(id, tempDemographics.getFieldFromDict(id))
        logging.info("Parsed identifiers from file Demographics object")
    except:
        logging.ERROR("Could not parse demographics!")
        print("Parser lookup failed!")
    tempRequest.setIdentifiersDict(idList)
    response = tempRequest.executeRequest()
    return response


def getPOSTPayloadToSIIMPatient(payload):
    tempRequest = http.createDefaultPatientPOSTRequest()
    tempRequest.setPayload(payload)
    response = tempRequest.executeRequest()
    return response


def getServerJSONDemographicObjectFromFilepath(path, ids):
    try:
        response = getPatientGETResponseFromDemographicsFile(path, ids)
        PatientsJSON = JSON.createPatientJSONResponse(response)
        return PatientsJSON
    except:
        print("Error generating response!")

