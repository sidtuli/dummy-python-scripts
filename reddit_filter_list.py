import requests
from urllib.parse import urlparse
from urllib.parse import urlunparse
from datetime import datetime, timedelta
import time

def checkTime(time):
    currentTime = datetime.now()
    monthBackTime = currentTime - timedelta(days=31)
    #print(time)
    #print(monthBackTime)
    return time <= monthBackTime

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
def getRedditJsonRequestData(redditJsonRequestUrl) :
    try:
        #time.sleep(.1)
        response = requests.get(redditJsonRequestUrl, headers = {'User-agent': 'Telexon Bot Requests ' + datetime.now().strftime('%Y%m%d%H%M%S')})
        if(response.status_code == 200) :
            #print(redditJsonRequestUrl.strip())
            return response
        else :
            print(response.status_code)
    except :
        return None

def processRedditUrls(text_file, output_file):

    redditTextLines = []

    resultLines = []
    
    with open(text_file) as f:
        redditTextLines = f.readlines()
        #print(redditTextLines)
    
    for line in redditTextLines:

        redditJsonURL = createRedditJsonRequestUrl(line)
        #print(redditJsonURL)

        if redditJsonURL != None:
            redditJsonData = getRedditJsonRequestData(redditJsonURL)
            if redditJsonData != None:
                time.sleep(15)
                #print(redditJsonData.json()[0]['data'].keys())
                #print(datetime.fromtimestamp(redditJsonData.json()[0]['data']['children'][0]['data']['created']))
                monthOld = checkTime(datetime.fromtimestamp(redditJsonData.json()[0]['data']['children'][0]['data']['created']))

                if monthOld:
                    resultLines.append(line)
    
    
    with open(output_file, 'r+') as output:
        for line in resultLines:
            print(line)
            #output.seek(0)
            #output.truncate(0)
            output.write(line)


processRedditUrls("saved_post.txt", "deleted_post.txt")