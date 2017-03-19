import requests
from requests.auth import HTTPDigestAuth
import json
from collections import OrderedDict
import sys
import matplotlib.pyplot as plt
import numpy as np


def analyzeResponse():
    print("The response contains {0} properties".format(len(jData)))
    print("\n")

def getMetaDataString():
     #This is to get the meta data before parsing the rest of the data
    string = "Meta Data: \n"
    metaData = jData['Meta Data']
    for i in metaData:
        string += i + " : " + metaData[i] + "\n"
    return string

#returns data for given amount of minutes
#@param periods the number of minutes
def getMinuteDataString(periods):
    string = ""
    count = 0
    mins = periods
    #this can technichally also get the metadata if you remove the restriction - but why tho 
    for i in jData: #this is to seperate minute data from metadata
        if i != 'Meta Data': #remove this line if you want metadata
            string += i + " : \n"
            subData = OrderedDict(jData[i]) 
            string += "\n"
            for j in subData: #this is to each individual minute
                string += "    " + j + " : \n"
                try: 
                    subsubData = OrderedDict(subData[j]) 
                    for k in subsubData: #this is to get the data from each indiviudal minute
                        string += "        " + k + " : " + str(subsubData[k]) + "\n"
                    count += 1
                    if count == mins:
                        break
                except:
                    string += "        " +  str(subData[j]) + "\n"
                string += "\n"
            string += "\n"
    return string

def getTicker():
    return symbol

def getMostRecent():
    return getMinuteDataString(1)

def makeAPICall():
    url = "http://www.alphavantage.co/query?function=" + function + "&symbol=" + symbol + "&interval=" + interval + "&apikey=" + apikey + "&series_type=" + series_type + "&time_period=" + time_period
    myResponse = requests.get(url)
    jData = json.loads(myResponse.content, object_pairs_hook=OrderedDict)
    return (url, myResponse, jData)

def checkFunction(input):
    for id in functions:
        if input == id:
            return True
    return False

def graphValues(valType, mins):
    count = 0
    counter = []
    time = [] 
    values = []
    for i in jData: #this is to seperate minute data from metadata
        if i != 'Meta Data': #remove this line if you want metadata
            subData = OrderedDict(jData[i]) 
            for j in subData: #this is to each individual minute
                time.append(j)
                try: 
                    subsubData = OrderedDict((subData[j])) 
                    for k in subsubData: #this is to get the data from each indiviudal minute
                        if valType in k:
                            values.append((subsubData[k]))
                    count += 1
                    counter.append(count)
                    if count == mins:
                        break
                except:
                    print
    intvals = []           
    for val in reversed(values):
        intvals.append(float(val))
    data = {}
    intvals = np.array(intvals)
    counter = np.array(counter)
    #plt.xticks(counter, time)
    #plt.xticks(rotation=90)
    plt.plot(counter, intvals)

    
   
    # Make space for and rotate the x-axis tick labels  

functions = {1 : "EMA", 2 : "SMA", 4 : "TIME_SERIES_DAILY", 3 : "TIME_SERIES_INTRADAY", 5: "TIME_SERIES_MONTHLY" }   

running = True 
while running:
    try:
        print
        # Add into API call
        print "Availible Functions: ", functions
        print "Enter Function Number: ", 
        function = input()
        if checkFunction:
            function = functions[function]
        else:
            raise ValueError('Incorrect Function ID')

        if len(sys.argv) == 1:
            print "Enter Ticker: ", 
            symbol = raw_input().upper()
        else:
            symbol = sys.argv[1].upper() 
        interval = "1min"
        apikey = "7854"
        series_type = "close"
        time_period = "60"
        #How many Periods?
        print "Enter Amount of Periods: ", 
        periods = input()
        if periods <= 0:  
            raise ValueError('Period Must be Greater than 0')


        (url, myResponse, jData) = makeAPICall()

        if (myResponse.ok):
            print getTicker()
            print getMinuteDataString(periods)
        else:
            # If response code is not ok (200), print the resulting http error code with description
            myResponse.raise_for_status()
            raise ValueError('Bad Server Response')

        running = False
    except:
        print "Please Enter Valid Information" 
        running = False       
#print getMetaDataString()
print "Graph Value: ", 
inp = raw_input()
graphValues(inp, periods)
#graphValues("close", periods)
#graphValues("low", periods)
#graphValues("high", periods)
plt.show()
#print url