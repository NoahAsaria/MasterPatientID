import JSONResponseClass as JSON
import ParserClass as parser
import HTTPRequestClass as http
import logging
logFormat = '%(asctime)s: %(levelname)s: %(message)s @ %(filename)s : %(funcName)s: --> line %(lineno)d'
logging.basicConfig(filename='logs/log.txt', format=logFormat,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

#GETSIIMResponseFromDemographicsFile(String filepath, List identifierList): Parses file, GET call to Patient resource
#with identifier parameters
    #identifierList: ex) {given, family, address} --> GET http://hackathon.../Patient/?given= &family= &address=
def getPatientGETResponseFromDemographicsFile(filepath, identifierList):
    logging.info("In getPatientGETResponseFromDemographicsFile")
    idList = {}
    tempRequest = http.createDefaultPatientGETRequest()
    tempDemographics = parser.Demographics(filepath)
    logging.debug("filepath argument: %s", filepath)
    logging.debug("identifierList argument: %s", identifierList)
    try:
        for id in identifierList:
            idList.update({id : tempDemographics.getFieldFromDict(id)})
        tempRequest.setIdentifiersDict(idList)
        logging.info("Finished parsing identifiers from file Demographics object")
    except:
        logging.ERROR("Could not parse demographics!")
    try:
        response = tempRequest.executeRequest()
        logging.info("Executed request successfully!")
    except:
        logging.ERROR("Failed executing request!")
    return response


def getPOSTPayloadToSIIMPatient(payload):
    logging.debug("payload: %s", payload)
    tempRequest = http.createDefaultPatientPOSTRequest()
    tempRequest.setPayload(payload)
    response = tempRequest.executeRequest()
    logging.info("Excecuted POST request")
    return response


def getServerJSONDemographicObjectFromFilepath(path, ids):
    try:
        response = getPatientGETResponseFromDemographicsFile(path, ids)
        PatientsJSON = JSON.createPatientJSONResponse(response)
        return PatientsJSON
    except:
       logging.error("createJSONResponse failed %s", PatientsJSON)

