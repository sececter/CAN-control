import re
import time
import sys
import getopt
from luminol.anomaly_detector import AnomalyDetector
from luminol.correlator import Correlator


def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:c:v", ["help", "input=" "correlate="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    input = None
    correlate = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input = a
        elif o in ("-c", "--correlate"):
            correlate = a
        else:
            assert False, "unhandled option"
   
    regex = r"(\s+)([+-]?\d*\.\d+)(?![-+0-9\.])(\s+)(\d+)(\s+)(\w+)(\s+)(\w+)(\s+)([a-z])(\s+)(\d+)(?:(?!X).)*(Length = )(\d+)(\s+)(BitCount = )(\d+)(\s+)(ID = )(\d+)"

    pattern = re.compile(regex, re.UNICODE)


    file1 = open(input).read()
    matches1 = re.finditer(regex, file1)

    file2 = open(correlate).read()
    matches2 = re.finditer(regex, file2)

    mydict1={}
    mydict2={}

    for matchNum, match in enumerate(matches1):
        matchNum = matchNum + 1
        myTime = match.group(2)

        myTime = float(myTime) * 1000000
    
        mydict1[myTime]=match.group(20)

    for matchNum, match in enumerate(matches2):
        matchNum = matchNum + 1
        myTime = match.group(2)

        myTime = float(myTime) * 1000000
    
        mydict2[myTime]=match.group(20)

    #print mydict1  

    my_detector1 = AnomalyDetector(mydict1,algorithm_name=("exp_avg_detector"))
    score1 = my_detector1.get_all_scores()

    anomalies = my_detector1.get_anomalies()
    for a in anomalies:
        time_period = a.get_time_window()
        my_correlator = Correlator(mydict1, mydict2, time_period)

        if my_correlator.is_correlated(treshold=0.8):
            print "mydict2 correlate with mydict at time period (%d, %d)" % time_period 


if __name__ == "__main__":
   main(sys.argv[1:])

