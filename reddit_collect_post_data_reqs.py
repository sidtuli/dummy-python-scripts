from urllib.parse import urlparse
from urllib.parse import urlunparse
import requests
from datetime import datetime
import json
import os
import random
import time

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
        #time.sleep(.1)
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
    
    # Open file and dump dict into resulting json file
    with open(filename, 'w') as fp:
        json.dump(resultRedditJsonData, fp)
    

def createRedditDataJson(sourceRedditTextFile, jsonResultFileName) :
    global resultRedditJsonData
    global statuses
    # clear out before so that statuses is not added between method calls
    statuses = {}
    print("Starting time - " + str(datetime.now()))
    
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
    print(statuses)
    updateRedditResponseJsonFile(jsonResultFileName)
    print("Finishing time - " + str(datetime.now()))
    

def printKeys(filename) :
    global resultRedditJsonData
    loadRedditDataJson(filename)
    
    for key in resultRedditJsonData:
        print(key)

def grabCharsAt(fileName, lineNumber, charNumber, charRange):
    charNumber = charNumber if charNumber >= 0 else 0
    charRange = charRange if charRange >= 0 else 0
    lineNumber = lineNumber if lineNumber >= 0 else 0
    with open(fileName) as f:
        lines = f.readlines()
        
        for i in range(0,len(lines)):
            line = lines[i]
            if(i == lineNumber):

                # determine start point of char selection
                charNumber = charNumber if charNumber < len(line) else len(line) - 1

                # determine max of char range
                maxChar = charNumber + charRange if charNumber + charRange < len(line) else len(line) - 1

                # determine min of char range
                minChar = charNumber - charRange if charNumber - charRange >= 0 else 0

                return line[minChar:maxChar+1]
            
def grabRandomEntry(redditResultsJson, writeToFile) :
    global resultRedditJsonData
    with open(redditResultsJson) as f:
        resultRedditJsonData = json.load(f)
        keys = list(resultRedditJsonData.keys())
        randKey = keys[random.randrange(0,len(keys)-1)]
        #sanitizeRedditEntry(randKey)
        if(writeToFile):
            with open("random" + datetime.now().strftime('%Y%m%d%H%M%S') + ".json", 'w') as fp:
                jsontowrite = {randKey:resultRedditJsonData[randKey]}
                json.dump(jsontowrite, fp)
        return resultRedditJsonData[randKey]


def parseRedditEntries(redditResultsJson, keyForVal) :
    #global resultRedditJsonData
    print("parsing for key: " + keyForVal)
    with open(redditResultsJson) as f:
        resultRedditJsonData = json.load(f)
        valTally = {}
        for redditEntryKey in resultRedditJsonData.keys() :
            for i in range(0, len(resultRedditJsonData[redditEntryKey])) :

                if keyForVal in resultRedditJsonData[redditEntryKey][i].keys() :
                    value = grabRedditKeyValue(resultRedditJsonData[redditEntryKey][i][keyForVal])
                    if not(value in valTally.keys()) :
                        valTally[value] = 0
                    valTally[value] += 1
                    
                    
                # process inner data object
                if("data" in resultRedditJsonData[redditEntryKey][i].keys()) :
                    if keyForVal in resultRedditJsonData[redditEntryKey][i]["data"].keys():
                        value = grabRedditKeyValue(resultRedditJsonData[redditEntryKey][i]["data"][keyForVal])
                        if not(value in valTally.keys()) :
                            valTally[value] = 0
                        valTally[value] += 1
                    
                    # check further to children nodes in data
                    if "children" in resultRedditJsonData[redditEntryKey][i]["data"].keys() :
                        # iterate over children
                        for childrenIndex in range(0,len(resultRedditJsonData[redditEntryKey][i]["data"]["children"])):
                            if keyForVal in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys():
                                value = grabRedditKeyValue(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex][keyForVal])
                                if not(value in valTally.keys()) :
                                    valTally[value] = 0
                                valTally[value] += 1
                                     
                            if "data" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys() :
                                if keyForVal in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys():
                                    value = grabRedditKeyValue(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"][keyForVal])
                                    if not(value in valTally.keys()) :
                                        valTally[value] = 0
                                    valTally[value] += 1
        print(valTally)
def grabRedditKeyValue(value) :
    if type(value) == list:
        print(value)
        return len(value)
    if type(value) == dict:
        print(value)
        return len(value.keys())
    else:
        return value
def deleteEntryFromJson(jsonResultFile, entryKeyDelete):
    global resultRedditJsonData
    loadRedditDataJson(jsonResultFile)

    if entryKeyDelete in resultRedditJsonData.keys() :
        del resultRedditJsonData[entryKeyDelete]
    
    updateRedditResponseJsonFile(jsonResultFile)

def deleteField(redditResultsJson) :
    global resultRedditJsonData
    loadRedditDataJson(redditResultsJson)

    for entryKey in resultRedditJsonData.keys():
        sanitizeRedditEntry(entryKey)

    updateRedditResponseJsonFile(redditResultsJson)
    
def sanitizeRedditEntry(redditEntryKey):
    global resultRedditJsonData
    # we know this will be a list so we can parse that and process each object
    for i in range(0, len(resultRedditJsonData[redditEntryKey])) :

        keysToDeleteUpperLayer = [] #["modhash","can_gild","is_meta","visited","pinned","quarantine","can_mod_post","contest_mode","hidden","stickied","locked","saved","gilded","archived","whitelist_status","parent_whitelist_status","is_robot_indexable","clicked","total_awards_received","is_created_from_ads_ui","distinguished","is_crosspostable","author_is_blocked","allow_live_comments","spoiler","hide_score","top_awarded_type","author_premium","send_replies","is_reddit_media_domain","link_flair_background_color","all_awardings","author_flair_type","author_flair_background_color","author_flair_template_id","author_flair_text_color","subreddit_subscribers","author_patreon_flair","gildings","link_flair_text_color","score","edited","created_utc","wls","pwls","upvote_ratio","downs","suggested_sort","treatment_tags","content_categories"]
        for deleteKey in resultRedditJsonData[redditEntryKey][i].keys() :
            #print(deleteKey)
            if (checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i][deleteKey])) :
                keysToDeleteUpperLayer.append(deleteKey)

        for keyToDeleteUpperLayer in keysToDeleteUpperLayer:
            if keyToDeleteUpperLayer in resultRedditJsonData[redditEntryKey][i].keys():
                del resultRedditJsonData[redditEntryKey][i][keyToDeleteUpperLayer]
            
        # process inner data object
        if("data" in resultRedditJsonData[redditEntryKey][i].keys()) :
            keysToDeleteDataLayer = [] # ["modhash","can_gild","is_meta","visited","pinned","quarantine","can_mod_post","contest_mode","hidden","stickied","locked","saved","gilded","archived","whitelist_status","parent_whitelist_status","is_robot_indexable","clicked","total_awards_received","is_created_from_ads_ui","distinguished","is_crosspostable","author_is_blocked","allow_live_comments","spoiler","hide_score","top_awarded_type","author_premium","send_replies","is_reddit_media_domain","link_flair_background_color","all_awardings","author_flair_type","author_flair_background_color","author_flair_template_id","author_flair_text_color","subreddit_subscribers","author_patreon_flair","gildings","link_flair_text_color","score","edited","created_utc","wls","pwls","upvote_ratio","downs","suggested_sort","treatment_tags"]
            for deleteDataKey in resultRedditJsonData[redditEntryKey][i]["data"].keys() :
                if (checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"][deleteDataKey])) :
                    keysToDeleteDataLayer.append(deleteDataKey)
            for keyToDeleteDataLayer in keysToDeleteDataLayer:
                if keyToDeleteDataLayer in resultRedditJsonData[redditEntryKey][i]["data"].keys():
                    del resultRedditJsonData[redditEntryKey][i]["data"][keyToDeleteDataLayer]
            
            # check further to children nodes in data
            if "children" in resultRedditJsonData[redditEntryKey][i]["data"].keys() :
                
                for childrenIndex in range(0,len(resultRedditJsonData[redditEntryKey][i]["data"]["children"])):
                   keysToDeleteChildLayer = [] # ["modhash","can_gild","is_meta","visited","pinned","quarantine","can_mod_post","contest_mode","hidden","stickied","locked","saved","gilded","archived","whitelist_status","parent_whitelist_status","is_robot_indexable","clicked","total_awards_received","is_created_from_ads_ui","distinguished","is_crosspostable","author_is_blocked","allow_live_comments","spoiler","hide_score","top_awarded_type","author_premium","send_replies","is_reddit_media_domain","link_flair_background_color","all_awardings","author_flair_type","author_flair_background_color","author_flair_template_id","author_flair_text_color","subreddit_subscribers","author_patreon_flair","gildings","link_flair_text_color","score","edited","created_utc","wls","pwls","upvote_ratio","downs","suggested_sort","treatment_tags","content_categories"]
                   for deleteChildrenKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys() :
                        if (checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex][deleteChildrenKey])) :
                           keysToDeleteChildLayer.append(deleteChildrenKey)
                        
                        for keyToDeleteChildLayer in keysToDeleteChildLayer :
                            if keyToDeleteChildLayer in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys():
                                del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex][keyToDeleteChildLayer]

                        
                        if "data" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys() :
                            keysToDeleteChildDataLayer = [] #["modhash","can_gild","is_meta","visited","pinned","quarantine","can_mod_post","contest_mode","hidden","stickied","locked","saved","gilded","archived","whitelist_status","parent_whitelist_status","is_robot_indexable","clicked","total_awards_received","is_created_from_ads_ui","distinguished","is_crosspostable","author_is_blocked","allow_live_comments","spoiler","hide_score","top_awarded_type","author_premium","send_replies","is_reddit_media_domain","link_flair_background_color","all_awardings","author_flair_type","author_flair_background_color","author_flair_template_id","author_flair_text_color","subreddit_subscribers","author_patreon_flair","gildings","link_flair_text_color","score","edited","created_utc","wls","pwls","upvote_ratio","downs","suggested_sort","treatment_tags","content_categories"]
                            for deleteChildDataKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys() :
                               if((checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"][deleteChildDataKey]))) :
                                   keysToDeleteChildDataLayer.append(deleteChildDataKey)
                            
                            for keyToDeleteChildDataLayer in keysToDeleteChildDataLayer :
                                if keyToDeleteChildDataLayer in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys():
                                    del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"][keyToDeleteChildDataLayer]
                            
                            if "replies" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys() :
                                #for replyIndex in range(0, len(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"])) :

                                keysToDeleteChildDataRepliesLayer = []

                                for deleteChildDataRepliesKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"].keys() :
                                    if((checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"][deleteChildDataRepliesKey]))) :
                                        keysToDeleteChildDataRepliesLayer.append(deleteChildDataRepliesKey)
                                for keyToDeleteChildDataRepliesLayer in keysToDeleteChildDataRepliesLayer :
                                    del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"][keyToDeleteChildDataRepliesLayer]

                                if "data" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"].keys() :
                                    keysToDeleteChildDataRepliesDataLayer = []

                                    for deleteChildDataRepliesDataKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"].keys() :
                                        if((checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"][deleteChildDataRepliesDataKey]))) :
                                            keysToDeleteChildDataRepliesDataLayer.append(deleteChildDataRepliesDataKey)
                                    
                                    for keyToDeleteChildDataRepliesDataLayer in keysToDeleteChildDataRepliesDataLayer :
                                        del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"][keyToDeleteChildDataRepliesDataLayer]

                                    if "children" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]:
                                        #print(len(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"]))

                                        for replyChildrenIndex in range(0,len(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"])):
                                            keysToDeleteChildDataRepliesDataChildLayer = []
                                            for deleteToDeleteChildDataRepliesDataChildLayerKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"][replyChildrenIndex].keys() :
                                                if(checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"][replyChildrenIndex][deleteToDeleteChildDataRepliesDataChildLayerKey])):
                                                    keysToDeleteChildDataRepliesDataChildLayer.append(deleteToDeleteChildDataRepliesDataChildLayerKey)
                                            
                                            for keyToDeleteChildDataRepliesDataChildLayer in keysToDeleteChildDataRepliesDataChildLayer:
                                                del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"][replyChildrenIndex][keyToDeleteChildDataRepliesDataChildLayer]

                                            if "data" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"][replyChildrenIndex].keys():
                                                keysToDeleteChildDataRepliesDataChildDataLayer = []
                                                for deleteToDeleteChildDataRepliesDataChildDataLayerKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"][replyChildrenIndex]["data"].keys() :
                                                    if(checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"][replyChildrenIndex]["data"][deleteToDeleteChildDataRepliesDataChildDataLayerKey])):
                                                        keysToDeleteChildDataRepliesDataChildDataLayer.append(deleteToDeleteChildDataRepliesDataChildDataLayerKey)
                                            
                                                for keyToDeleteChildDataRepliesDataChildDataLayer in keysToDeleteChildDataRepliesDataChildDataLayer:
                                                    del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"]["data"]["children"][replyChildrenIndex]["data"][keyToDeleteChildDataRepliesDataChildDataLayer]
                    
def checkKeyForDeletion(valueToCheck) :
    if valueToCheck == None:
        return True
    if type(valueToCheck) == list and len(valueToCheck) == 0 :
        return True
    if type(valueToCheck) == dict and len(valueToCheck.keys()) == 0:
        return True
    if type(valueToCheck) == str and valueToCheck == "" :
        return True
    
def collectKeys(redditResultsJson) :
    global resultRedditJsonData
    loadRedditDataJson(redditResultsJson)
    allKeys = set()
    
    for entryKey in resultRedditJsonData.keys():
        allKeys.update(collectKeysForEntry(entryKey))
    return allKeys

def collectKeysForEntry(redditEntryKey):
    global resultRedditJsonData
    resultKeys = set()
    for i in range(0, len(resultRedditJsonData[redditEntryKey])) :

        
        resultKeys.update(resultRedditJsonData[redditEntryKey][i].keys())

        if("data" in resultRedditJsonData[redditEntryKey][i].keys()) :
            resultKeys.update(resultRedditJsonData[redditEntryKey][i]["data"].keys())

            if "children" in resultRedditJsonData[redditEntryKey][i]["data"].keys():
                #print("children exists")
                for childrenIndex in range(0,len(resultRedditJsonData[redditEntryKey][i]["data"]["children"])):
                    #print(len(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys()))
                    resultKeys.update(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys())

                    if "data" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys() :
                        #print(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys())
                        resultKeys.update(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys())

                        if "replies" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys() :
                            resultKeys.update(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"]["replies"].keys())
                        
    return resultKeys

#print(grabCharsAt("result.json", 0 , 1, 300))

createRedditDataJson("jojo.txt", "result_test.json")
createRedditDataJson("jojo.txt", "result.json")
deleteField("result.json")

#print(grabRandomEntry("result.json",True))


#parseRedditEntries("result.json","kind")
#collectKeys("result.json")