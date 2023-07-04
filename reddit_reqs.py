from urllib.parse import urlparse
from urllib.parse import urlunparse
import requests
import time
from datetime import datetime
import json
import os

#Dict that will serve to load in initial reddit data from file and also later write out results
resultRedditJsonData = {}
statuses = {}

# This method will load in the reddit json specified to resultRedditJsonData
# If the file doesn't exist we don't load in anything and resultRedditJsonData will start empty
def loadRedditDataJson(jsonResultFileName) :
    global resultRedditJsonData
    with open(jsonResultFileName) as f :
        resultRedditJsonData = json.load(f)

# We clean up the reddit url from the raw text file pull and return a request link
def createRedditJsonRequestUrl(rawRedditUrl) :
    # remove whitespace
    rawRedditUrl = rawRedditUrl.strip()
    # If empty we return None to signal bad url
    if rawRedditUrl == "" :
        return None
    
    # Parse url from raw line
    urlParts = urlparse(rawRedditUrl)

    #If not reddit link, we exit early
    if(not(urlParts.netloc == "www.reddit.com")) :
        return None
    
    # Remove query parts from raw reddit
    newLink = urlunparse((urlParts.scheme, urlParts.netloc, urlParts.path, urlParts.params, '', urlParts.fragment))

    # Create json request link from url above with removing last slash and adding json suffix
    redditJsonRequestLink = newLink[:newLink.rfind('/')]  + ".json"

    #Request link
    return redditJsonRequestLink

# Make reddit json data request 
def getRedditJsonRequestData(rawRedditUrl, redditJsonRequestUrl) :
    global resultRedditJsonData
    global statuses

    if(rawRedditUrl.strip() in resultRedditJsonData.keys()) :
        return None
    try:
        response = requests.get(redditJsonRequestUrl, headers = {'User-agent': 'Telexon Bot Requests ' + datetime.now().strftime('%Y%m%d%H%M%S')})
        if(response.status_code == 200) :
            print(rawRedditUrl.strip())
            return response
        else :
            if not(response.status_code in statuses) :
                statuses[response.status_code] = 0
            statuses[response.status_code] += 1
    except :
        return None
    
def insertIntoRedditJson(responseData, rawUrlLine) :

    global resultRedditJsonData
    resultRedditJsonData[rawUrlLine.strip()] = responseData.json()

def updateRedditResponseJsonFile(filename) :
    global resultRedditJsonData
    global statuses
    # Open file and dump dict into resulting json file
    with open(filename, 'w') as fp:
        json.dump(resultRedditJsonData, fp)
    print(statuses)

def createRedditDataJson(sourceRedditTextFile, jsonResultFileName) :
    global resultRedditJsonData
    loadRedditDataJson(jsonResultFileName)
    keysBefore = str(len(resultRedditJsonData.keys()))
    

    # start reading in reddit urls from source text file
    with open(sourceRedditTextFile) as f:
        # each line is a raw url so we start reading those in
        lines = f.readlines()
        for line in lines:
            requestUrl = createRedditJsonRequestUrl(line)
            if not (requestUrl == None) :
                redditResponse = getRedditJsonRequestData(line, requestUrl)
                if not(redditResponse == None) :
                    insertIntoRedditJson(redditResponse, line)
    
    print("Keys Before: " + keysBefore)
    print("Keys After: " + str(len(resultRedditJsonData.keys())))
    updateRedditResponseJsonFile(jsonResultFileName)
    

def printKeys(filename) :
    global resultRedditJsonData
    loadRedditDataJson(filename)
    
    for key in resultRedditJsonData:
        print(key)
