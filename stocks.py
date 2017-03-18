import requests
from requests.auth import HTTPDigestAuth
import json
from collections import OrderedDict

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


# Add into API call
funtion = "TIME_SERIES_INTRADAY"
symbol = "TSLA"
interval = "1min"
apikey = "7854"
#How many Minutes?
periods = 10


url = "http://www.alphavantage.co/query?function=" + funtion + "&symbol=" + symbol + "&interval=" + interval + "&apikey=" + apikey
myResponse = requests.get(url)
# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content, object_pairs_hook=OrderedDict)

    print("The response contains {0} properties".format(len(jData)))
    print("\n")

    print getMetaDataString()
    print getMinuteDataString(periods)
            

else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()
