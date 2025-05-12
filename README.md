# Dummy Python Scripts
Collection of dumb little python scripts I play around with

## reddit_collect_post_data_reqs.py

A python script to collect data on a list of reddit posts and export it to json

### Citations

https://stackoverflow.com/questions/66178703/retrieving-all-comments-from-a-thread-on-reddit

[Removing last part of the url](https://stackoverflow.com/questions/54961679/python-removing-the-last-part-of-an-url)
Used here:
```python
# Create json request link from url above with removing last slash and adding json suffix
    redditJsonRequestLink = newLink[:newLink.rfind('/')]  + ".json"
```
[Initializing python dict](https://stackoverflow.com/questions/2853683/what-is-the-preferred-syntax-for-initializing-a-dict-curly-brace-literals-or)
Used here:
```python
#Dict that will serve to load in initial reddit data from file and also later write out results
resultRedditJsonData = {}
statuses = {}
```


[How to place a dict into a json file](https://stackoverflow.com/questions/17043860/how-to-dump-a-dict-to-a-json-file)
```python
# Open file and dump dict into resulting json file
    with open(filename, 'w') as fp:
        json.dump(resultRedditJsonData, fp)
```

[How to recombine url with url unparse](https://stackoverflow.com/questions/3798269/combining-a-url-with-urlunparse)
Used here:
```python
# Remove query parts from raw reddit
    newLink = urlunparse((urlParts.scheme, urlParts.netloc, urlParts.path, urlParts.params, '', urlParts.fragment))
```
[ALT+SHIFT+F to format json neatly in vscode](https://stackoverflow.com/questions/70728371/json-files-structure-format-in-visual-studio-code)

[str() converts ints to string in python](https://stackoverflow.com/questions/961632/convert-integer-to-string-in-python)
Used here:
```python
keysBefore = str(len(resultRedditJsonData.keys()))
```
and here:
```python
print("Keys After: " + str(len(resultRedditJsonData.keys())))
```

[Solving getting 429s for reddit requests by adding a user agent](https://www.reddit.com/r/redditdev/comments/3qbll8/429_too_many_requests/)
Used here:
```python
response = requests.get(redditJsonRequestUrl, headers = {'User-agent': 'Cool Bot Requests ' + datetime.now().strftime('%Y%m%d%H%M%S')})
```
[Basic tutorial on request.get() method](https://www.w3schools.com/PYTHON/ref_requests_get.asp)
Used here:
```python
response = requests.get(redditJsonRequestUrl, headers = {'User-agent': 'Cool Bot Requests ' + datetime.now().strftime('%Y%m%d%H%M%S')})
```
[Python docs on urllib.parse method](https://docs.python.org/3/library/urllib.parse.html)
Used here:
```python
# Parse url from raw line
urlParts = urlparse(rawRedditUrl)
```
[Python docs on urllib.unparse](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlunparse)
Used here:
```python
# Remove query parts from raw reddit
newLink = urlunparse((urlParts.scheme, urlParts.netloc, urlParts.path, urlParts.params, '', urlParts.fragment))
```
[Basic tutorial link on how to open file to read](https://www.pythontutorial.net/python-basics/python-read-text-file/)
```python
# start reading in reddit urls from source text file
    with open(sourceRedditTextFile) as f:
```
and here:
```python
# Open file and dump dict into resulting json file
with open(filename, 'w') as fp:
```
and here:
```python
with open(jsonResultFileName) as f :
```

[JSON python module documentation](https://docs.python.org/3/library/json.html)
Used here:
```python
resultRedditJsonData = json.load(f)
```
and here:
```python
json.dump(resultRedditJsonData, fp)
```

[json loads tutorial](https://www.geeksforgeeks.org/read-json-file-using-python/#)
Used here:
```python
resultRedditJsonData = json.load(f)
```

[Tutorial on used global vars](https://www.w3schools.com/python/gloss_python_global_variables.asp)
Used here (all over):
```python
global resultRedditJsonData
global statuses
```

[How to delete keys from dicts StackoverFlow link](https://stackoverflow.com/questions/64033039/how-to-delete-key-and-value-from-json)


#### Misc links
* [How to scrape data from Reddit using the Python Reddit API Wrapper(PRAW)](https://towardsdatascience.com/scraping-reddit-data-1c0af3040768)
* [Retrieving all comments from a thread on Reddit](https://stackoverflow.com/questions/66178703/retrieving-all-comments-from-a-thread-on-reddit)
* [Reddit API Docs](https://www.reddit.com/dev/api)
* [Simple OAuth2 for Reddit API](https://www.reddit.com/r/redditdev/comments/dx0hbo/ill_admit_it_im_stupid_how_do_i_do_the_oauth2/)
* [old oauth2 reddit api doc](https://github.com/reddit-archive/reddit/wiki/OAuth2)
* [How to get author, title, data, and body of a post (self or link) or comment? (newbie)](https://www.reddit.com/r/redditdev/comments/i0ufug/how_to_get_author_title_data_and_body_of_a_post/)
* [The Best Web Crawler for Scraping Reddit](https://medium.com/dataseries/the-best-web-crawler-for-scraping-reddit-c8db54c6b613)
* [Python sleep fot milliseconds](https://stackoverflow.com/questions/377454/how-do-i-get-my-program-to-sleep-for-50-milliseconds)

## reddit_unsave_reqs.py

A python script in order to unsave a list of reddit posts in bulk

### Citations

[Old OAuth2 Reddit GitHub wiki documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2)

[General Reddit API documentation](https://www.reddit.com/dev/api)

[Reddit unsave api endpoint documentation](https://www.reddit.com/dev/api/#POST_api_unsave)

[Example code on how to make an OAuth Token Request to Reddit](https://stackoverflow.com/questions/70884227/reddit-api-get-access-token)

[Example code function on to get current time in milliseconds](https://stackoverflow.com/questions/5998245/how-do-i-get-the-current-time-in-milliseconds-in-python)

[Manually raising (throwing) an exception in Python](https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python)

[Example on how to send POST requests for personal reddit user data](https://www.reddit.com/r/redditdev/comments/sti7i8/post_data_headers_auth_and_get_headers_params_etc/)

## extract_csv_column_to_text_list.py

### Citations

[Python CSV reader docs](https://docs.python.org/3/library/csv.html)

[Python CSV dict reader docs](https://docs.python.org/3/library/csv.html#csv.DictReader)

[StackOverflow article on write mode file open](https://stackoverflow.com/questions/2967194/open-in-python-does-not-create-a-file-if-it-doesnt-exist)

[StackOverflow article on adding new lines when writing to a file](https://stackoverflow.com/questions/2918362/writing-string-to-a-file-on-a-new-line-every-time)

[Useful article comparing string comparisons](https://note.nkmk.me/en/python-str-compare/)

## filter_text_file.py

### Citations

[Python regex example article](https://www.w3schools.com/python/python_regex.asp)

[Python regex testinmg site](https://pythex.org/)

[Python Regex Docs](https://docs.python.org/3/howto/regex.html)

[StackOverflow article on checking new lines in string](https://stackoverflow.com/questions/5193811/how-can-i-check-for-a-new-line-in-string-in-python-3-x)

[How to remove contents of a file](https://stackoverflow.com/questions/2769061/how-to-erase-the-file-contents-of-text-file-in-python)

[Reviewing file open modes in Python](https://stackoverflow.com/questions/16208206/confused-by-python-file-mode-w)

## reddit_filter_list.py

### Citations

[Checking time with arithmetic Python date time, under "Measuring Time Span with Timedelta Objects"](https://www.dataquest.io/blog/python-datetime-tutorial/)

[Python comparing times](https://stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da)

[Converting epoch ms to date time objects in Python](https://pythonguides.com/python-epoch-to-datetime/)

[convert struct time to date time object](https://stackoverflow.com/questions/1697815/how-do-you-convert-a-time-struct-time-object-into-a-datetime-object)

[date arithmetic in Python](https://stackoverflow.com/questions/38200581/subtract-a-month-from-a-date-in-python)


## processAndUnsaveRedditSaveds.js

Simple little JS script to run in browser to mass unsave stuff

### Citations

[How to do a for loop in JavaScript](https://stackoverflow.com/questions/9329446/loop-for-each-over-an-array-in-javascript)

[borrowed sleep function](https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep)

## analyze_firefox_bookmarks.py

[html.parser python documentation](https://docs.python.org/3/library/html.parser.html#html.parser.HTMLParser)
[Example of python HTMLParser code](https://www.pythoncentral.io/html-parser/)