from urllib.parse import urlparse
from urllib.parse import urlunparse
import requests
from datetime import datetime
import json
import os
import random

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
    
    # Open file and dump dict into resulting json file
    with open(filename, 'w') as fp:
        json.dump(resultRedditJsonData, fp)
    

def createRedditDataJson(sourceRedditTextFile, jsonResultFileName) :
    global resultRedditJsonData
    global statuses
    
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
            
def grabRandomEntry(redditResultsJson) :
    global resultRedditJsonData
    with open(redditResultsJson) as f:
        resultRedditJsonData = json.load(f)
        keys = list(resultRedditJsonData.keys())
        randKey = keys[random.randrange(0,len(keys)-1)]
        #resultRedditJsonData
        #print(resultRedditJsonData[randKey][0])
        #print(resultRedditJsonData[keys[len(keys)-1]])
        #print(resultRedditJsonData[randKey])
        #print(randKey)
        sanitizeRedditEntry(randKey)
        return resultRedditJsonData[randKey]
    
def parseRedditEntry(redditEntryJson) :
    #data = redditEntryJson["data"]
    #data = redditEntryJson["data"]["children"]
    data = redditEntryJson["data"]["children"][0]["data"]
    if(type(data) == dict):
        keys = data.keys()
        print(keys)
    if(type(data) == list):
        print("elts: " + str(len(data)))
        print(data)

def parseRedditEntries(redditResultsJson) :
    global resultRedditJsonData
    with open(redditResultsJson) as f:
        resultRedditJsonData = json.load(f)
        keys = list(resultRedditJsonData.keys())
        valTally = {}
        valueToCheck = "num_reports"
        for key in keys:
            currVal = "no key here"
            #currKind = type(resultRedditJsonData[key])
            #currKind = resultRedditJsonData[key][0]["kind"]
            #currVal = resultRedditJsonData[key][0]["data"]["after"]
            #currVal = resultRedditJsonData[key][0]["data"]["dist"]
            #currVal = resultRedditJsonData[key][0]["data"]["modhash"]
            #currVal = resultRedditJsonData[key][0]["data"]["geo_filter"]
            #currVal = resultRedditJsonData[key][0]["data"]["before"]
            #currVal = len(resultRedditJsonData[key][0]["data"]["children"])
            '''if("locked" in resultRedditJsonData[key][0]["data"]["children"][0]["data"].keys()):
                currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["locked"]
                if(currVal == "True" or currVal):
                    print(key)'''
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["locked"]
            '''if("archived" in resultRedditJsonData[key][0]["data"]["children"][0]["data"].keys()):
                currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["archived"]'''
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["archived"]
            #currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["mod_reports"])
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["pinned"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["is_meta"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["hidden"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["gilded"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["banned_by"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["contest_mode"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["quarantine"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["can_mod_post"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["can_gild"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["whitelist_status"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["category"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["edited"]
            '''currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["gildings"].keys())
            if(currVal > 0):
                for gild in resultRedditJsonData[key][0]["data"]["children"][0]["data"]["gildings"].keys():
                    print(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["gildings"][gild])'''
            '''currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["content_categories"] if resultRedditJsonData[key][0]["data"]["children"][0]["data"]["content_categories"] == None else len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["content_categories"])
            if(currVal != None and currVal > 0) :
                for i in range(0, len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["content_categories"])) :
                    print(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["content_categories"][i])'''
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["post_hint"] if "post_hint" in resultRedditJsonData[key][0]["data"]["children"][0]["data"].keys() else currVal
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["mod_reason_title"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["saved"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["clicked"]
            '''ignore, still keeping
            currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["link_flair_richtext"])
            if (currVal > 0) :
                for i in range(0, len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["link_flair_richtext"])) :
                    print(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["link_flair_richtext"][i])'''
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["pwls"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["upvote_ratio"]
            #currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["awarders"])
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["downs"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["top_awarded_type"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["parent_whitelist_status"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["is_robot_indexable"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["num_duplicates"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["discussion_type"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_is_blocked"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["mod_reason_by"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["removed_by_category"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["ups"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["removal_reason"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["suggested_sort"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["banned_at_utc"]
            # keeping - currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["url_overridden_by_dest"] if "url_overridden_by_dest" in resultRedditJsonData[key][0]["data"]["children"][0]["data"].keys() else currVal
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["is_reddit_media_domain"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["approved_by"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["allow_live_comments"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["is_created_from_ads_ui"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["no_follow"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["distinguished"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["is_crosspostable"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["hide_score"]
            #currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["user_reports"])
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["approved_at_utc"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["stickied"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_flair_text_color"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["send_replies"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["is_original_content"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["subreddit_type"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["total_awards_received"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["view_count"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["link_flair_background_color"]
            #currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["all_awardings"])
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["link_flair_text_color"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["report_reasons"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["score"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_premium"] if "author_premium" in resultRedditJsonData[key][0]["data"]["children"][0]["data"].keys() else currVal
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_patreon_flair"] if "author_patreon_flair" in resultRedditJsonData[key][0]["data"]["children"][0]["data"].keys() else currVal
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["created_utc"]
            #keep ? - currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["num_crossposts"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["subreddit_subscribers"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["visited"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_flair_type"] if "author_flair_type" in resultRedditJsonData[key][0]["data"]["children"][0]["data"].keys() else currVal
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["removal_reason"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["is_self"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["wls"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["spoiler"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_flair_background_color"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["link_flair_css_class"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_flair_template_id"]
            #keep? - currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["secure_media"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_flair_css_class"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["likes"]
            #currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["treatment_tags"])
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["removed_by"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["num_reports"]
            '''keep - currVal = len(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["secure_media_embed"].keys())
            if currVal > 0 :
                for key in resultRedditJsonData[key][0]["data"]["children"][0]["data"]["secure_media_embed"].keys():
                    print(resultRedditJsonData[key][0]["data"]["children"][0]["data"]["secure_media_embed"][key])'''
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_flair_background_color"]
            #currVal = resultRedditJsonData[key][0]["data"]["children"][0]["data"]["author_flair_background_color"]
            
            if not (currVal in valTally.keys()):
                valTally[currVal] = 0
                #print("New entry? " + key)
                #print(resultRedditJsonData[key])
            valTally[currVal] += 1
        print("Checking value: " + valueToCheck)
        print(valTally)

def deleteEntryFromJson(jsonResultFile, entryKeyDelete):
    global resultRedditJsonData
    loadRedditDataJson(jsonResultFile)

    if entryKeyDelete in resultRedditJsonData.keys() :
        del resultRedditJsonData[entryKeyDelete]
    
    updateRedditResponseJsonFile(jsonResultFile)

def deleteField(redditResultsJson) :
    global resultRedditJsonData
    loadRedditDataJson(redditResultsJson)
    
    #listLens = {}

    for entryKey in resultRedditJsonData.keys():
        #if(not(len(resultRedditJsonData[entryKey]) in listLens.keys())):
        #    listLens[len(resultRedditJsonData[entryKey])] = 0
        #listLens[len(resultRedditJsonData[entryKey])] += 1
        sanitizeRedditEntry(entryKey)

    
    updateRedditResponseJsonFile(redditResultsJson)
    #print(listLens)
    
def sanitizeRedditEntry(redditEntryKey):
    global resultRedditJsonData
    # we know this will be a list so we can parse that and process each object
    #print(resultRedditJsonData[redditEntryKey])
    #print(redditEntryKey in resultRedditJsonData)
    #print(type(resultRedditJsonData[redditEntryKey]))
    for i in range(0, len(resultRedditJsonData[redditEntryKey])) :
        #print(i)
        #print(resultRedditJsonData[redditEntryKey][i])

        keysToDeleteUpperLayer = ["modhash", "can_gild"]
        for deleteKey in resultRedditJsonData[redditEntryKey][i].keys() :
            #print(deleteKey)
            if (checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i][deleteKey])) :
                keysToDeleteUpperLayer.append(deleteKey)

        for keyToDeleteUpperLayer in keysToDeleteUpperLayer:
            if keyToDeleteUpperLayer in resultRedditJsonData[redditEntryKey][i].keys():
                del resultRedditJsonData[redditEntryKey][i][keyToDeleteUpperLayer]
            
        # process inner data object
        
        if("data" in resultRedditJsonData[redditEntryKey][i].keys()) :
            keysToDeleteDataLayer = ["modhash", "can_gild"]
            for deleteDataKey in resultRedditJsonData[redditEntryKey][i]["data"].keys() :
                if (checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"][deleteDataKey])) :
                    #print(deleteDataKey)
                    #del resultRedditJsonData[redditEntryKey][i]["data"][deleteDataKey]
                    keysToDeleteDataLayer.append(deleteDataKey)
            for keyToDeleteDataLayer in keysToDeleteDataLayer:
                #print(keyToDeleteDataLayer)
                if keyToDeleteDataLayer in resultRedditJsonData[redditEntryKey][i]["data"].keys():
                    del resultRedditJsonData[redditEntryKey][i]["data"][keyToDeleteDataLayer]
            
            # check further to children nodes in data
            if "children" in resultRedditJsonData[redditEntryKey][i]["data"].keys() :
                
                for childrenIndex in range(0,len(resultRedditJsonData[redditEntryKey][i]["data"]["children"])):
                   #print(children)
                   keysToDeleteChildLayer = ["modhash", "can_gild"]
                   for deleteChildrenKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex] :
                        if (checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex][deleteChildrenKey])) :
                           #print(deleteChildrenKey)
                           keysToDeleteChildLayer.append(deleteChildrenKey)
                        
                        for keyToDeleteChildLayer in keysToDeleteChildLayer :
                            if keyToDeleteChildLayer in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys():
                                del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex][keyToDeleteChildLayer]

                        
                        if "data" in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex].keys() :
                            keysToDeleteChildDataLayer = ["modhash", "can_gild"]
                            for deleteChildDataKey in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys() :
                               if((checkKeyForDeletion(resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"][deleteChildDataKey]))) :
                                   #print(deleteChildDataKey)
                                   keysToDeleteChildDataLayer.append(deleteChildDataKey)
                            
                            for keyToDeleteChildDataLayer in keysToDeleteChildDataLayer :
                                if keyToDeleteChildDataLayer in resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"].keys():
                                    del resultRedditJsonData[redditEntryKey][i]["data"]["children"][childrenIndex]["data"][keyToDeleteChildDataLayer]
                               
                       

    
    ''' FOR NOW WE'RE IGNORING ALL OF THIS AS PREVIOUS DATA ANALYSIS, PREFIXING THIS CODE WITH NEW CODE THAT JUST SACANS FOR EMPTY AND NULL KEYS FOR NOW
    #entry = resultRedditJsonData[redditEntryKey][0]

    #if(type(entry) == list):
    #    entry = entry[0]

    # delete "kind" from outer object
    if "kind" in resultRedditJsonData[redditEntryKey][0].keys():
        del resultRedditJsonData[redditEntryKey][0]["kind"]

    #entry = entry["data"]

    # delete "after" from data
    if "after" in resultRedditJsonData[redditEntryKey][0]["data"].keys():
        del resultRedditJsonData[redditEntryKey][0]["data"]["after"]
    
    # delete "dist" from data
    if "dist" in resultRedditJsonData[redditEntryKey][0]["data"].keys():
        del resultRedditJsonData[redditEntryKey][0]["data"]["dist"]

    # delete "modhash" from data
    if "modhash" in resultRedditJsonData[redditEntryKey][0]["data"].keys():
        del resultRedditJsonData[redditEntryKey][0]["data"]["modhash"]
    
    # delete "geo_filter" from data
    if "geo_filter" in resultRedditJsonData[redditEntryKey][0]["data"].keys():
        del resultRedditJsonData[redditEntryKey][0]["data"]["geo_filter"]
    
    # delete "before" from data
    if "before" in resultRedditJsonData[redditEntryKey][0]["data"].keys():
        del resultRedditJsonData[redditEntryKey][0]["data"]["before"]

    print(len(resultRedditJsonData[redditEntryKey][0]["data"]["children"]))
    if len(resultRedditJsonData[redditEntryKey][0]["data"]["children"]) == 1:
        # keys we don't care to check too hard and delete automatically
        keysToDelete = ["kind","locked","archived","mod_reports","pinned","is_meta","hidden","gilded","banned_by","contest_mode","quarantine","can_mod_post","can_gild",
                        "whitelist_status","category","edited","gildings","content_categories","mod_reason_title","saved","clicked","pwls","upvote_ratio","awarders","downs",
                        "top_awarded_type","parent_whitelist_status","is_robot_indexable","num_duplicates","discussion_type","author_is_blocked","mod_reason_by","approved_by",
                        "allow_live_comments","is_reddit_media_domain","banned_at_utc","suggested_sort","is_created_from_ads_ui","distinguished","is_crosspostable","hide_score",
                        "all_awardings","link_flair_background_color","view_count","total_awards_received","subreddit_type","is_original_content","send_replies",
                        "author_flair_text_color","all_awardings","link_flair_background_color","view_count","total_awards_received","subreddit_type","is_original_content",
                        "send_replies","stickied","approved_at_utc","user_reports","visited","removed_by","wls","treatment_tags","likes","subreddit_subscribers",
                        "author_flair_template_id","author_flair_background_color","spoiler","removal_reason","author_flair_type","is_self","created_utc","report_reasons",
                        "author_patreon_flair","author_premium","score","num_reports","num_reports","link_flair_text_color"]
        
        # find extra keys to delete 
        for key in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            if key == None :
                keysToDelete.append(key)
            elif type(resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"][key]) == list and len(resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"][key]):
                keysToDelete.append(key)

        for key in keysToDelete :
            #print(resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys())
            if key in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
                print(key + " DELETING THIS KEY NOW")
                print(resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"][key])
                del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"][key]
                #print(resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"][key])
        '''
        
def checkKeyForDeletion(valueToCheck) :
    if valueToCheck == None:
        return True
    if type(valueToCheck) == list and len(valueToCheck) == 0 :
        return True
    if type(valueToCheck) == dict and len(valueToCheck.keys()) == 0:
        return True
    if type(valueToCheck) == str and valueToCheck == "" :
        return True
    
#print(grabCharsAt("result.json", 0 , 191096891, 300))

createRedditDataJson("jojo.txt", "result.json")
deleteField("result.json")
#grabRandomEntry("result.json")
#print(grabRandomEntry("result.json"))

#parseRedditEntry(grabRandomEntry("result5.json"))
#parseRedditEntries("result5.json")




