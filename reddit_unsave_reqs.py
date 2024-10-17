import requests
import json
from requests.auth import HTTPBasicAuth
import time
import re

def get_client_creds_from_file(file_path) :
        try:
            with open(file_path) as f:
                creds_json = json.load(f)
                return [creds_json["client_id"], creds_json["client_secret"], creds_json["username"], creds_json["password"]]
        except FileNotFoundError :
            print("Could not find the credentials file")
            raise
        except json.decoder.JSONDecodeError:
            print("Unable to parse the credentials file as JSON")
            raise
        except KeyError:
            print("We were unable to find client_id or client_secret in the json")
            raise
        except:
            print("Unable to parse reddit client credentials")
            raise



# Access token code stolen from here - https://stackoverflow.com/questions/70884227/reddit-api-get-access-token
def get_reddit_bearer_token() :
    creds = get_client_creds_from_file("reddit_creds.json")
    headers = {'User-agent': 'Telexon Bot Requests'}
    data = {
        'grant_type': 'password',
        'username': creds[2],
        'password': creds[3]
    }
    token_request = requests.post("https://ssl.reddit.com/api/v1/access_token",
                  data=data,
                  auth=HTTPBasicAuth(creds[0], creds[1]),
                  headers=headers)
    
    if (token_request.status_code == 200):

        #print(token_request)
    
        token_request_data = json.loads(token_request.text)

        token_request_data["expires_in"] = current_millisec_time() + token_request_data["expires_in"]

        #print(token_request_data)

        return token_request_data
        #print(current_millisec_time())
        #print(current_millisec_time() + token_request_data["expires_in"])
    else:
        raise ValueError("Recieved an error in access token request, status code {request_status_code}".format(request_status_code=token_request.status_code))

def unsave_post(reddit_post_fullname, token_data):
    headers = {"Authorization": "bearer " + token_data["access_token"], 'User-agent': 'Telexon Bot Requests'}
    response = requests.post("https://oauth.reddit.com/api/unsave", headers=headers, data={"id":reddit_post_fullname})
    #print(response.text)
    #print(response)

def get_reddit_post_fullname(reddit_link):
    #print(reddit_link)
    regex_match = re.match("https://www.reddit.com/r/[A-z0-9_]+/comments/([A-z0-9]+)",reddit_link)
    if (regex_match == None and "https://www.reddit.com/user" in reddit_link) :
        regex_match = re.match("https://www.reddit.com/user/[A-z0-9_]+/comments/([A-z0-9]+)",reddit_link)
    return "t3_" + regex_match.group(1)
    
'''
def get_reddit_post_fullname(reddit_link):
    reddit_json_request = requests.get(reddit_link+".json", headers = {'User-agent': 'Telexon Bot Requests'})
    reddit_json_object = json.loads(reddit_json_request.text)
    #print(reddit_json_object[0]["data"]["children"][0]['data']['name'])
    return reddit_json_object[0]["data"]["children"][0]['data']['name']
    #return reddit_json_data
'''
# https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
    
# Get current time in milliseconds - https://stackoverflow.com/questions/5998245/how-do-i-get-the-current-time-in-milliseconds-in-python 
def current_millisec_time():
    return round(time.time() * 1000)

def grab_unsave_post_links(unsave_list_text_file):
    with open(unsave_list_text_file) as unsave_file:
        return unsave_file.readlines()

def remove_post_from_file(post_link, file_path):
    with open(file_path, 'r+') as cleaning_file:
        posts = cleaning_file.readlines()
        # https://stackoverflow.com/questions/2769061/how-to-erase-the-file-contents-of-text-file-in-python
        cleaning_file.seek(0)
        cleaning_file.truncate(0)
        #print(posts)

        for post in posts:
            #print(post)
            #print(post_link)
            #print(post)
            #print(re.search(post_link,post) or post_link in post)
            if not (re.search(post_link,post) or post_link in post):
                cleaning_file.write(post.rstrip() + '\n')
                #if('\n' in post):
                #    cleaning_file.write(post)
                #else:
                #    cleaning_file.write(post + "\n")
            else:
                print(post.rstrip())

unsave_posts = grab_unsave_post_links("filter_saved.txt")


for post in unsave_posts :
    post_full_name = get_reddit_post_fullname(post)
    #print(post_full_name)
    token_data = get_reddit_bearer_token()
    unsave_post(post_full_name, token_data)

    remove_post_from_file(post, "filter_saved.txt")
    time.sleep(1)
    
    
    

'''
General flow:
1. Grab file with reddit links
2. Process one link
2a. Get its full name
2b. get oauth token
2c. Run unsave request
3. Remove above reddit post from text file
4. Kick off above steps again
'''


