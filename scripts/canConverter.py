# coding=utf-8
"""
Python scripts to detect anomalies in CANoe ASCII log files 
Uses LinkedIn's luminol for anomalie detection (https://github.com/linkedin/luminol)

Useage example: python.exe canConverter.py -i inputfile.asc  -o outputfile.csv
"""

import re
import time
import sys
import getopt
import csv
from luminol.anomaly_detector import AnomalyDetector


def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:v", ["help","infile=", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  
        usage()
        sys.exit(2)
    output = None
    infile = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in("-i", "--infile"):
            infile = a
        else:
            assert False, "unhandled option"
   

    # this is the regular expression used to parse CANoe logs in ASCII format (.asc)
    regex = r"(\s+)([+-]?\d*\.\d+)(?![-+0-9\.])(\s+)(\d+)(\s+)(\w+)(\s+)(\w+)(\s+)([a-z])(\s+)(\d+)(?:(?!X).)*(Length = )(\d+)(\s+)(BitCount = )(\d+)(\s+)(ID = )(\d+)"

    pattern = re.compile(regex, re.UNICODE)

    inputfile = open(infile).read()

    matches = re.finditer(regex, inputfile)
  
    event_dict={}

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        myTime = match.group(2)
        
        # converts absolute time from engine start in seconds from engine start to int
        myTime = float(myTime) * 1000000
    
        # match.group(20) is ID of CAN event in decimal
        event_dict[myTime]=match.group(20)

    if(verbose == True):
        print event_dict

    with open(output, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in event_dict.items():
            writer.writerow([key, value])

if __name__ == "__main__":
   main(sys.argv[1:])

