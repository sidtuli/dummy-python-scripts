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
    with open(redditResultsJson) as f:
        resultRedditJsonData = json.load(f)
        keys = list(resultRedditJsonData.keys())
        randKey = keys[random.randrange(0,len(keys)-1)]
        #resultRedditJsonData
        #print(resultRedditJsonData[randKey][0])
        return resultRedditJsonData[randKey][0]
    
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

    i = 0

    for entryKey in resultRedditJsonData.keys():
        #del resultRedditJsonData[entry][0]["kind"]
        #if(i == 0) :
        #    print(entryKey)
        #i+=1
        sanitizeRedditEntry(entryKey)
    
    updateRedditResponseJsonFile(redditResultsJson)
    
def sanitizeRedditEntry(redditEntryKey):
    global resultRedditJsonData
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

    # delete "kind" from data's first layer children object
    if len(resultRedditJsonData[redditEntryKey][0]["data"]["children"]) == 1:
        if "kind" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["kind"]
        # delete "locked" from data's first layer children data object
        if "locked" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["locked"]
        # delete "archived" from data's first layer children data object
        if "archived" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["archived"]
        # delete "mod_reports" from data's first layer children data object
        if "mod_reports" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys() and len(resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["mod_reports"]) == 0:
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["mod_reports"]
        # delete "archived" from data's first layer children data object
        if "pinned" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["pinned"]
        # delete "is_meta" from data's first layer children data object
        if "is_meta" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["is_meta"]
        # delete "hidden" from data's first layer children data object
        if "hidden" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["hidden"]
        # delete "gilded" from data's first layer children data object
        if "gilded" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["gilded"]
        # delete "banned_by" from data's first layer children data object
        if "banned_by" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["banned_by"]
        # delete "contest_mode" from data's first layer children data object
        if "contest_mode" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["contest_mode"]
        # delete "quarantine" from data's first layer children data object
        if "quarantine" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["quarantine"]
        # delete "can_mod_post" from data's first layer children data object
        if "can_mod_post" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["can_mod_post"]
        # delete "can_gild" from data's first layer children data object
        if "can_gild" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["can_gild"]
        # delete "whitelist_status" from data's first layer children data object
        if "whitelist_status" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["whitelist_status"]
        # delete "category" from data's first layer children data object
        if "category" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["category"]
        # delete "edited" from data's first layer children data object
        if "edited" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["edited"]
        # delete "gildings" from data's first layer children data object
        if "gildings" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["gildings"]
        # delete "content_categories" from data's first layer children data object
        if "content_categories" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["content_categories"]
        # delete "mod_reason_title" from data's first layer children data object
        if "mod_reason_title" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["mod_reason_title"]
        # delete "saved" from data's first layer children data object
        if "saved" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["saved"]
        # delete "clicked" from data's first layer children data object
        if "clicked" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["clicked"]
        # delete "pwls" from data's first layer children data object
        if "pwls" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["pwls"]
        # delete "upvote_ratio" from data's first layer children data object
        if "upvote_ratio" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["upvote_ratio"]
        # delete "awarders" from data's first layer children data object
        if "awarders" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["awarders"]
        # delete "downs" from data's first layer children data object
        if "downs" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["downs"]
        # delete "top_awarded_type" from data's first layer children data object
        if "top_awarded_type" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["top_awarded_type"]
        # delete "parent_whitelist_status" from data's first layer children data object
        if "parent_whitelist_status" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["parent_whitelist_status"]
        # delete "is_robot_indexable" from data's first layer children data object
        if "is_robot_indexable" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["is_robot_indexable"]
        # delete "num_duplicates" from data's first layer children data object
        if "num_duplicates" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["num_duplicates"]
        # delete "discussion_type" from data's first layer children data object
        if "discussion_type" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["discussion_type"]
        # delete "author_is_blocked" from data's first layer children data object
        if "author_is_blocked" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["author_is_blocked"]
        # delete "mod_reason_by" from data's first layer children data object
        if "mod_reason_by" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["mod_reason_by"]
        # delete "approved_by" from data's first layer children data object
        if "approved_by" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["approved_by"]
        # delete "allow_live_comments" from data's first layer children data object
        if "allow_live_comments" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["allow_live_comments"]
        # delete "is_reddit_media_domain" from data's first layer children data object
        if "is_reddit_media_domain" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["is_reddit_media_domain"]
        # delete "banned_at_utc" from data's first layer children data object
        if "banned_at_utc" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["banned_at_utc"]
        # delete "suggested_sort" from data's first layer children data object
        if "suggested_sort" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["suggested_sort"]
        # delete "is_created_from_ads_ui" from data's first layer children data object
        if "is_created_from_ads_ui" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["is_created_from_ads_ui"]
        # delete "distinguished" from data's first layer children data object
        if "distinguished" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["distinguished"]
        # delete "is_crosspostable" from data's first layer children data object
        if "is_crosspostable" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["is_crosspostable"]
        # delete "hide_score" from data's first layer children data object
        if "hide_score" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["hide_score"]
        # delete "all_awardings" from data's first layer children data object
        if "all_awardings" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["all_awardings"]
        # delete "link_flair_background_color" from data's first layer children data object
        if "link_flair_background_color" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["link_flair_background_color"]
        # delete "view_count" from data's first layer children data object
        if "view_count" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["view_count"]
        # delete "total_awards_received" from data's first layer children data object
        if "total_awards_received" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["total_awards_received"]
        # delete "subreddit_type" from data's first layer children data object
        if "subreddit_type" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["subreddit_type"]
        # delete "is_original_content" from data's first layer children data object
        if "is_original_content" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["is_original_content"]
        # delete "send_replies" from data's first layer children data object
        if "send_replies" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["send_replies"]
        # delete "author_flair_text_color" from data's first layer children data object
        if "author_flair_text_color" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["author_flair_text_color"]
        # delete "stickied" from data's first layer children data object
        if "stickied" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["stickied"]
        # delete "approved_at_utc" from data's first layer children data object
        if "approved_at_utc" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["approved_at_utc"]
        # delete "user_reports" from data's first layer children data object
        if "user_reports" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["user_reports"]
        # delete "visited" from data's first layer children data object
        if "visited" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["visited"]
        # delete "removed_by" from data's first layer children data object
        if "removed_by" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["removed_by"]
        # delete "wls" from data's first layer children data object
        if "wls" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["wls"]
        # delete "treatment_tags" from data's first layer children data object
        if "treatment_tags" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["treatment_tags"]
        # delete "likes" from data's first layer children data object
        if "likes" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["likes"]
        # delete "subreddit_subscribers" from data's first layer children data object
        if "subreddit_subscribers" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["subreddit_subscribers"]
        # delete "author_flair_template_id" from data's first layer children data object
        if "author_flair_template_id" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["author_flair_template_id"]
        # delete "author_flair_background_color" from data's first layer children data object
        if "author_flair_background_color" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["author_flair_background_color"]
        # delete "spoiler" from data's first layer children data object
        if "spoiler" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["spoiler"]
        # delete "removal_reason" from data's first layer children data object
        if "removal_reason" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["removal_reason"]
        # delete "author_flair_type" from data's first layer children data object
        if "author_flair_type" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["author_flair_type"]
        # delete "is_self" from data's first layer children data object
        if "is_self" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["is_self"]
        # delete "created_utc" from data's first layer children data object
        if "created_utc" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["created_utc"]
        # delete "report_reasons" from data's first layer children data object
        if "report_reasons" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["report_reasons"]
        # delete "author_patreon_flair" from data's first layer children data object
        if "author_patreon_flair" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["author_patreon_flair"]
        # delete "author_premium" from data's first layer children data object
        if "author_premium" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["author_premium"]
        # delete "score" from data's first layer children data object
        if "score" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["score"]
        # delete "num_reports" from data's first layer children data object
        if "num_reports" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["num_reports"]
        # delete "link_flair_text_color" from data's first layer children data object
        if "link_flair_text_color" in resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"].keys():
            del resultRedditJsonData[redditEntryKey][0]["data"]["children"][0]["data"]["link_flair_text_color"]
        
        



