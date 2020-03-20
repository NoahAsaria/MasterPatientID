from flask import Flask, render_template, request
import HTTPRequestClass as http
import ParserClass as parser
import JSONResponseClass as jsonResponse
import pathlib
import time
app = Flask(__name__)

wsgi_app = app.wsgi_app

@app.route('/', methods = ["GET", "POST"])
def hello():
    if request.method=="POST":
        file = request.files["file"]
        file.save(os.path.join("UploadedFiles", file.filename))
        fileType = pathlib.Path(file.filename).suffix.lower()
        demographics_dict = "NA"
        if (fileType == '.xml'):
            try:
                demographics = parser.createNewDemographicsInstance('UploadedFiles/'+file.filename)
                demographics_dict = demographics.getDemographicDict()
                print(demographics_dict)
            except:
                return render_template("index.html",
                                       file_name=file.filename,
                                       file_type=fileType,
                                       demographics = "Error! Could not parse that file!")
            return render_template("index.html",
                               file_name=file.filename,
                               file_type=fileType,
                               demographics = str(demographics_dict))
        else:
            return render_template("index.html",
                                   file_name="NA",
                                   file_type="NA",
                                   demographics = demographics_dict)
    return render_template("index.html", message="Upload a file",
                           file_name="",
                           file_type="",
                           demographics = "NA")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
