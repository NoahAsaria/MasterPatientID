from flask import Flask, render_template, request, redirect
import PatientJSONResponseClass as jsonResponse
import AllergiesJSONResponseClass as jsonAllergyResponse
import ParserClass as parser
import HTTPRequestClass as http
import pathlib
import DictionaryMatchClass as matcher
import RXLookup as rx

app = Flask(__name__)

wsgi_app = app.wsgi_app

@app.route('/', methods = ["GET", "POST"])
def hello():
    global demographics_dict
    global file
    global fileType
    global demographicIdentifiers
    if request.method=="POST":
        if 'file' in request.files: #If the 'file' form button was clicked
            file = request.files["file"] #Grab file contained with name "file" from HTML page
            if(file.filename == ''):
                return redirect(request.url) #If nothing was entered, refresh the page
            file.save(os.path.join("UploadedFiles", file.filename)) #Save the file.
            fileType = pathlib.Path(file.filename).suffix.lower() #Get file extension.
            if (fileType == '.xml'):
                try:
                    demographics = parser.createNewDemographicsInstance('UploadedFiles/'+file.filename) #Pull file from uploads folder and parse
                    demographics_dict = demographics.getDemographicDict()
                    allergies_dict = demographics.getAllergiesDict()
                    allergies = allergies_dict['allergies']
                    for i in range(len(allergies),10): #Pad the allergies from file to pass to front-end
                        allergies.append("")
                except: #If we could not find / parse that file.
                    return render_template("index.html",
                                       file_name=file.filename,
                                       file_type=fileType,
                                       prompt="Could not parse that file! Try again!")
                return render_template("index.html",
                                       file_name=file.filename,
                                       file_type=fileType,
                                       given=demographics.getFieldFromDemographicDict('given'),
                                       family=demographics.getFieldFromDemographicDict('family'),
                                       address=demographics.getFieldFromDemographicDict('address'),
                                       city=demographics.getFieldFromDemographicDict('city'),
                                       state=demographics.getFieldFromDemographicDict('state'),
                                       postalcode=demographics.getFieldFromDemographicDict('postalcode'),
                                       birthtime=demographics.getFieldFromDemographicDict('birthtime'),
                                       gender=demographics.getFieldFromDemographicDict('gender'),
                                       race=demographics.getFieldFromDemographicDict('race'),
                                       allergy0 = allergies[0],
                                       allergy1 = allergies[1],
                                       allergy2 = allergies[2],
                                       allergy3 = allergies[3],
                                       allergy4 = allergies[4],
                                       allergy5 = allergies[5],
                                       allergy6 = allergies[6],
                                       allergy7 = allergies[7],
                                       allergy8 = allergies[8],
                                       allergy9 = allergies[9])
            else:
                return render_template("index.html",
                                       file_name=file.filename,
                                       file_type="N/A",
                                       prompt="Please attach an XML file and try again!")
        elif 'query' in request.form:
            #demographicIdentifiers = demographic parameters user selects (after extracted from CCD file) in form
            #allergyidentifiers = allergy parameters user selects (after extracted from CCD file)
            #PatientJSONDicts = demographic data extracted from SIIM Server query (in the form {id : {given : value, family : value ...}}
            #allergyJSONDicts = allergy data extracted from SIIM Server query (in the form {id : {allergies: [code1, code2, ...]}})

            #We can only extract values from HTML tags, so manually get identifiers dict.
            multiselect = request.form.getlist('queryparams')
            demographicIdentifiers = {}
            allergymultiselect = request.form.getlist('allergyparams')
            allergyIdentifiers = {"code" : []}
            for entry in multiselect: #Get demographic identifiers
                #print("entry: ", entry)
                split = entry.split(':')
                demographicIdentifiers[split[0]] = split[1]

            for entry in allergymultiselect:
                #print("allergy entry: ", entry)
                split = entry.split(':')
                allergyIdentifiers["code"].append(rx.lookup(split[1])) #This will produce a url like ../AllergyIntolerance?display="Hives"&display="Rashes"... Bascially we need to query by code per SIIM rules


            try:
                #Handle the demographics selected
                GETRequest = http.HTTPRequest('GET')
                GETRequest.setApiEndpoint("http://hackathon.siim.org/fhir")
                GETRequest.setResource("Patient")
                GETRequest.setHeadersDict({'content-type': 'application/json'})
                GETRequest.setIdentifiersDict(demographicIdentifiers)
                GETRequest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')

                response = GETRequest.executeRequest()
                JSONResponse = jsonResponse.createPatientJSONResponse(response)
                PatientJSONDicts = JSONResponse.getPatientDictionaries()

                #Handle the allergies selected
                GETRequest.setResource("AllergyIntolerance")
                GETRequest.setIdentifiersDict(allergyIdentifiers)
                allergyResponse = GETRequest.executeRequest()
                allergyJSONResponse = jsonAllergyResponse.createAllergyJSONResponse(allergyResponse)
                AllergyJSONDicts = allergyJSONResponse.getAllergyDictionaries()

                print("CCD Allergy Parameters: ", allergyIdentifiers)
                print("CCD Demographic Parameters: ", demographicIdentifiers)
                print("Allergy JSON Dicts: ", AllergyJSONDicts)
                print("Demographic JSON Dicts: ", PatientJSONDicts)
                #Keep only allergiesJSONDict found also in PatientJSONDict
                AllergyJSONDicts = matcher.intersection(PatientJSONDicts, AllergyJSONDicts)
                allergyMatches = matcher.unweightedAllergyDictionaryMatch(allergyIdentifiers, AllergyJSONDicts)
                matchDicts = matcher.sortStringDict(matcher.weightedPatientDictionaryMatch(demographics_dict,PatientJSONDicts,allergyMatches))


                text = matcher.formatMatchDict(matchDicts)
                text += "<strong><br>Patient Information Queried: " + str(demographicIdentifiers) + "<br></strong>"
                text += str(demographics_dict)
                text += "<strong><br><br>Demographics Data matched:<br></strong>" + matcher.formatJSONDicts(PatientJSONDicts)
                text += "<strong><br>Allergy Data matched:<br></strong>" + matcher.formatJSONDicts(AllergyJSONDicts)
                entries = JSONResponse.getNumberOfPatientEntries()
            except:
                print("ERROR!")
                return redirect(request.url)
            return render_template("index.html",
                                   showResponse="True",
                                   numResults=entries,
                                   responseText=text)
        else: return redirect(request.url)
    return render_template("index.html")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)

