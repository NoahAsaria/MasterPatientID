##11/13/19
#NOAH ASARIA

##Initializing pyCCDA package based on Example Usage
##Link: https://github.com/MemoirHealth/ccda-parser

from pyCCDA import CCDA
import os


dirpath = os.getcwd()
files = []
# r=root, d=directories, f = files
# Get all xml files in the current directory
for r, d, f in os.walk(dirpath):
    for file in f:
        if '.xml' in file:
            files.append(os.path.join(r, file))

for f in files:
   ccd = CCDA(f.read())
   # ccd.type   # The document type ('ccda', 'c32', and such)
   # ccd.source # The parsed source data (XML) with added querying methods
   # ccd.data   # The final parsed document data
name = ccd.data.demographics.name
print(name.prefix, name.given, name.family)