import requests
from requests.auth import HTTPDigestAuth
import json

# Replace with the correct URL
url = "http://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&apikey=7854"

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
myResponse = requests.get(url)
#print (myResponse.status_code)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)

    print("The response contains {0} properties".format(len(jData)))
    #print((jData))
    print("\n")
    periods = 5
    count = 0

    #This is to get the meta data before parsing the rest of the data
    print "Meta Data: "
    metaData = jData['Meta Data']
    for i in metaData:
        print i, " : ", metaData[i]
    print


    #this can technichally also get the metadata if you remove the restriction - but why tho 
    for i in jData: #this is to seperate minute data from metadata
        if i != 'Meta Data':
            print i, " : "
            subData = dict(jData[i]) 
            print "\n"
            for j in subData: #this is to each individual minute
                print "    ", j, " : "
                try: 
                    subsubData = dict(subData[j]) 
                    for k in subsubData: #this is to get the data from each indiviudal minute
                        print "        ", k, " : ", subsubData[k]
                    count += 1
                    if count == periods:
                        break
                except:
                    print "        ",  subData[j]
                print "\n"
            print "\n"
            

else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()