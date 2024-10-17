import re
import json

def process_file(input_text_file, output_file=None):
    lines = []
    lines = read_file(input_text_file)

    subreddit_dict = {}

    for line in lines:
        
        subreddit_name = grab_subreddit_name(line)

        if subreddit_name == None:
            continue

        if subreddit_name in subreddit_dict:
            subreddit_dict[subreddit_name] = subreddit_dict[subreddit_name] + 1
        else :
            subreddit_dict[subreddit_name] = 1
    # sort dict by values - https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    # reverse order from above - https://stackoverflow.com/questions/5455606/how-to-reverse-order-of-keys-in-python-dict
    subreddit_dict = dict(reversed(sorted(subreddit_dict.items(), key=lambda item: item[1])))
    
    print(subreddit_dict)

    if (output_file != None):
        with open(output_file, 'w+') as subreddit_json:
            json.dump(subreddit_dict, subreddit_json)


def read_file(input_text_file):
    lines = []
    try:
        with open(input_text_file) as input:
            lines = input.readlines()
    except:
        lines = None
    
    return lines
    
def grab_subreddit_name(link_line):
    try:
        regex_match = re.match("https://www.reddit.com/r/([A-z0-9_]+)/comments/", link_line)
        return regex_match.group(1)
    except:
        return None

process_file("saved_post.txt","subreddits.json")
