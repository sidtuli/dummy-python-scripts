import re

def read_file(input_text_file):
    lines = []
    subreddit_dict = {}
    with open(input_text_file) as input:
        lines = input.readlines()
    
    for line in lines:
        regex_match = re.match("https://www.reddit.com/r/([A-z0-9_]+)/comments/",line)

        if regex_match == None:
            continue
        
        subreddit_name = regex_match.group(1)

        if subreddit_name in subreddit_dict:
            subreddit_dict[subreddit_name] = subreddit_dict[subreddit_name] + 1
        else :
            subreddit_dict[subreddit_name] = 1
    
    print(subreddit_dict)

read_file("saved_post.txt")
