import os
from bs4 import BeautifulSoup
import lxml
import xml.etree.ElementTree as ET

def parseXML(file):
    tree = ET.parse(file)
    root = tree.getroot()
    #printAllTags(root)
    #printRoot(root)
    return tree

def printRoot(root):
    #print(root.tag.replace("{urn:hl7-org:v3}", ""), ": ", root.attrib, root.text)   
    print(root.tag.replace("{urn:hl7-org:v3}", ""), ": ", root.text)
    printChildrenFromRoot(root, 0)

def printChildrenFromRoot(root, index):
    index = index+1 
    for child in root:
        tabs = ""
        for i in range(0, index):
            tabs=tabs+"\t"
        #print(tabs,child.tag.replace("{urn:hl7-org:v3}", ""), child.attrib, child.text)
        print(tabs,child.tag.replace("{urn:hl7-org:v3}", ""), ": ", child.text)
        printChildrenFromRoot(child, index)

def printAllTags(root):
    allElements = root.iter()
    for elem in allElements:
        print(elem.tag.replace("{urn:hl7-org:v3}", ""))

def printAllText(root):
    allElements = root.iter()
    for elem in allElements:
        print(str(elem.text))

def XMLToString(root):
    return ET.tostring(root)        

def findElement(root, tagToFind):
    allElements = root.iter()
    for elem in allElements:
        tag = elem.tag.replace("{urn:hl7-org:v3}","")
        if tag == tagToFind:
            print(tag, ": ", elem.text)

def createDictWithPatientBasicInfo(root):
    dict = {}
    for child in root:
        if (child.tag == '{urn:hl7-org:v3}recordTarget'):
            for patientRole in child:
                for role in patientRole:
                    if (role.tag.replace("{urn:hl7-org:v3}","") == "addr"):
                        for addrField in role:
                            #Gets streetAddressLine, city, state, postalCode, country
                            shortenedTag = addrField.tag.replace("{urn:hl7-org:v3}","")
                            dict[shortenedTag] = addrField.text

                    if (role.tag.replace("{urn:hl7-org:v3}","") == "patient"):
                        for addrField in role:
                            for name in addrField: #Get first/last name, languageCode
                                shortenedTag = name.tag.replace("{urn:hl7-org:v3}","")
                                if shortenedTag == "family": dict["lastname"] = name.text
                                if shortenedTag == "given": dict["firstname"] = name.text
                                if shortenedTag == "languageCode": dict["Language"] = name.attrib['code']

    print(dict)
    return dict
                            


#print("current directory is : " + dirpath)
dirpath = os.getcwd()
files = []
# r=root, d=directories, f = files
# Get all xml files in the current directory
for r, d, f in os.walk(dirpath):
    for file in f:
        if '.xml' in file:
            files.append(os.path.join(r, file))

for f in files:
    tree = parseXML(f)
    root = tree.getroot()
    findElement(tree.getroot(), "city")

    #createDictWithPatientBasicInfo(root)
    #printAllText(tree.getroot())
    #printRoot(tree.getroot())
