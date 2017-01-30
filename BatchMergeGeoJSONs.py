#Batch merge GeoJSONs into a single file.
#Requires Python 2.7+ to run.

#Based on this GIST: https://gist.github.com/uncheckederror/12f99fca2aaf7db9ad1a6c9563ea1417

#For modifying JSON structured files
from json import load, JSONEncoder

#For grabbing all the GeoJSON files in a specified folder.
import glob
import os

#For parsing GeoJSON's formatting.
from re import compile
charfloat_pat = compile(r'^[\[,\,]-?\d+\.\d+(e-?\d+)?$')

#Variables for hard coding. Comment out the three user input processing calls below these four methods to skip the command prompts.
inputFiles = []
outputFile = ""

#Taking user input for folder location.
def fileLocation():
    inputPath = str(raw_input("\nWhat folder are the GeoJSONs that you want to merge located in?\nThe file path should be formated like this:\nC:\Temp\AuburnData_Clean.csv\n"))
    for inputfile in glob.glob(os.path.join(inputPath, '*.geojson')):
        inputFiles.append(inputfile)
        
    print "\nIs this the correct file location? " + str(inputPath)
    if userCheck() == False:
        fileLocation()
    else:
        return inputFiles

#Taking user input for output file name and location.
def outputLocation():
    outputFile = str(raw_input("Where to you want the merged GeoJSON file to be placed and what do you want it named?\nPlease format your response like this:\nC:\Temp\AuburnData_Clean_geocoded.geojson and remember to append the .geojson file type.\n"))
    print "\nIs this the correct file location? " + str(outputFile)
    if userCheck() == False:
        outputLocation()
    else:
        return outputFile
        
#Having users verify their inputs.      
def userCheck():
    verifyFile = str(raw_input("(Y)es or No? "))
    valid = ['Yes', 'yes', 'y', 'Y', 'True', 'true', 'yse', 'Yse', 'YES','']
    if verifyFile in valid:
        print "\nInformation verified by user."
    else:
        return False

#User input processing calls. Comment out these method calls to skip user input.                
inputFiles = fileLocation()
outputFile = outputLocation()

#For troubleshooting.
print "\ninputFiles = " + str(inputFiles) + "\noutputFile = " + str(outputFile) + "\n\n*****Begin Processing*****\n"    

#Where the GeoJSON merging is actually done.
def mergeGeoJSONs():

    outjson = dict(type='FeatureCollection', features=[])
    
    for infile in inputFiles:
        injson = load(open(infile))
        
        if injson.get('type', None) != 'FeatureCollection':
            raise Exception('Sorry, "%s" does not look like GeoJSON' % infile)
        
        if type(injson.get('features', None)) != list:
            raise Exception('Sorry, "%s" does not look like GeoJSON' % infile)
        
        outjson['features'] += injson['features']

    encoder = JSONEncoder(separators=(',', ':'))
    encoded = encoder.iterencode(outjson)
    
    format = '%.' + str(2) + 'f'
    output = open(outputFile, 'w')
    
    for token in encoded:
        if charfloat_pat.match(token):
            # in python 2.7, we see a character followed by a float literal
            output.write(token[0] + format % float(token[1:]))

        else:
            output.write(token)

    #End processing message.
    print "\n*****Processing Complete*****\n\n" + "You can find the new GeoJSON file at " + outputFile

#GeoJSON merging call.
mergeGeoJSONs()
