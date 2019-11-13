#11/13/19
#NOAH ASARIA

#Initialization setup for bluebutton.py module
#Setup readme available: https://github.com/ctsit/bluebutton.py

import os
import subprocess
from bluebutton import BlueButton

dirpath = os.getcwd()
files = []
# r=root, d=directories, f = files
# Get all xml files in the current directory
for r, d, f in os.walk(dirpath):
    for file in f:
        if '.xml' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)
    with open(f) as fp:
        ccd = BlueButton(fp.read())

        ccd.type   # The document type ('ccda', 'c32', and such)
        ccd.source # The parsed source data (XML) with added querying methods
        ccd.data   # The final parsed document data

        name = ccd.data.demographics.name
        print(name.prefix, name.given, name.family)

        print('Medications:')
        for medication in ccd.data.medications:
            print(medication.product.name)