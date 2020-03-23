from flask import Flask, render_template, request, url_for, redirect
import HTTPRequestClass as http
import ParserClass as parser
import JSONResponseClass as jsonResponse
import pathlib
import requests
import time
import jsonify
app = Flask(__name__)

wsgi_app = app.wsgi_app

@app.route('/', methods = ["GET", "POST"])
def hello():
    global demographics_dict
    global file
    global fileType
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
                except: #If we could not find / parse that file.
                    return render_template("index.html",
                                       file_name=file.filename,
                                       file_type=fileType,
                                       prompt="Could not parse that file! Try again!")
                return render_template("index.html",
                                       file_name=file.filename,
                                       file_type=fileType,
                                       given=demographics.getFieldFromDict('given'),
                                       family=demographics.getFieldFromDict('family'),
                                       address=demographics.getFieldFromDict('address'),
                                       city=demographics.getFieldFromDict('city'),
                                       state=demographics.getFieldFromDict('state'),
                                       postalcode=demographics.getFieldFromDict('postalcode'),
                                       birthtime=demographics.getFieldFromDict('birthtime'),
                                       gender=demographics.getFieldFromDict('gender'),
                                       race=demographics.getFieldFromDict('race'))
            else:
                print("HELLO THERE")
                return render_template("index.html",
                                       file_name=file.filename,
                                       file_type="N/A",
                                       prompt="Please attach an XML file and try again!")
        elif 'query' in request.form:
            #We can only extract values from HTML tags, so manually get identifiers dict.
            multiselect = request.form.getlist('queryparams')
            identifiers = {}
            for entry in multiselect:
                split = entry.split(':')
                identifiers[split[0]] = split[1]
            print(identifiers)
            try:
                GETRequest = http.HTTPRequest('GET')
                GETRequest.setApiEndpoint("http://hackathon.siim.org/fhir")
                GETRequest.setResource("Patient")
                GETRequest.setHeadersDict({'content-type': 'application/json'})
                GETRequest.setIdentifiersDict(identifiers)
                #GETRequest.setIdentifiersDict({'_id': 'siimjoe'})
                GETRequest.setApiKey('d6e052ee-18c9-4f3b-a150-302c998e804c')

                response = GETRequest.executeRequest()
                JSONResponse = jsonResponse.createPatientJSONResponse(response)
                text = JSONResponse.getPatientDictionaries()
                entries = JSONResponse.getNumberOfPatientEntries()
            except:
                print("ERROR!")
                return redirect(request.url)
            print("I'm here!")
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
