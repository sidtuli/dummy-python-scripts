import re

def process_file(input_text_file):
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
    
    print(subreddit_dict)

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

process_file("saved_post.txt")
