# coding=utf-8
"""
Python scripts to detect anomalies in CANoe ASCII log files 
Uses LinkedIn's luminol for anomalie detection (https://github.com/linkedin/luminol)

Useage example: python.exe canIDS.py -i inputfile.asc  
                python.exe canIDS.py -i inputfile.asc -v
"""


import re
import time
import sys
import getopt
from luminol.anomaly_detector import AnomalyDetector


def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:v", ["help", "input="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  
        usage()
        sys.exit(2)
    input = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input = a
        else:
            assert False, "unhandled option"
   
    # this is the regular expression used to parse CANoe logs in ASCII format (.asc)
    regex = r"(\s+)([+-]?\d*\.\d+)(?![-+0-9\.])(\s+)(\d+)(\s+)(\w+)(\s+)(\w+)(\s+)([a-z])(\s+)(\d+)(?:(?!X).)*(Length = )(\d+)(\s+)(BitCount = )(\d+)(\s+)(ID = )(\d+)"

    pattern = re.compile(regex, re.UNICODE)

    inputfile = open(input).read()

    # stores all lines which match the regex 
    matches = re.finditer(regex, inputfile)

    # event_dict stores the values (timestamp + CAN-ID) extracted from the logs 
    event_dict={}

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        myTime = match.group(2)

        # converts absolute time from engine start in seconds from engine start to int
        myTime = float(myTime) * 1000000
    
        # match.group(20) is ID of CAN event in decimal
        event_dict[myTime]=match.group(20)

    #print event_dict  

    my_detector = AnomalyDetector(event_dict,algorithm_name=("exp_avg_detector"))

    # this calculates an anomal yscore for every event in the time series
    score = my_detector.get_all_scores()

    # filter events in time series for anomalies
    anomalies = my_detector.get_anomalies()

    anom_score = []

    print
    
    for attack in anomalies:

        if(attack.exact_timestamp in event_dict):

            if(verbose == True):
                # if script is run with "-v" it will output all anomaies
                print("{timestamp} - ID: {id} - Score: {value}".format(timestamp = attack.exact_timestamp, id = event_dict[attack.exact_timestamp], value = attack.anomaly_score))
           
            elif(attack.anomaly_score > 3.4):
                # if script is not run with "-v" it will output only anomalies with score > 3.4
                print("{timestamp} - ID: {id} - Score: {value}".format(timestamp = attack.exact_timestamp, id = event_dict[attack.exact_timestamp], value = attack.anomaly_score))
            #else:
                #print("Value not found")

if __name__ == "__main__":
   main(sys.argv[1:])

