import csv
import datetime
import xml.etree.ElementTree as ET
import json
import logging
import pathlib
from pathlib import Path
import pprint

#getAllFiles
    #input: directory name
    #output: list containing element-tree parsings of each file in directory
def getAllFiles(directory):
    directoryPath = Path(directory)
    data = []
    assert(directoryPath.is_dir())
    for f in directoryPath.iterdir():
        data.append(ET.parse(f))
    return data

#printAllChildrenNames
    #input: list
    #output: all child tag/attributes within list elements
def printAllChildrenNames(xmlList):
    for ccd in xmlList:
        root = ccd.getroot()
        for child in root:
           print(child.tag)
           print(child.attrib)

printAllChildrenNames(getAllFiles('example_data'))