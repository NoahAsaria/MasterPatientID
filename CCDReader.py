import os
from bs4 import BeautifulSoup
import lxml
import xml.etree.ElementTree as ET


def parseXML(file):
    tree = ET.parse(file)
    root = tree.getroot()
    printRoot(root)

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




dirpath = os.getcwd()
#print("current directory is : " + dirpath)

files = []
# r=root, d=directories, f = files
# Get all xml files in the current directory
for r, d, f in os.walk(dirpath):
    for file in f:
        if '.xml' in file:
            files.append(os.path.join(r, file))


for f in files:
    parseXML(f)
