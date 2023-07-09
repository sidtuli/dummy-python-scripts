# Dummy Python Scripts
Collection of dumb little python scripts I play around with

## reddit_reqs.py

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
response = requests.get(redditJsonRequestUrl, headers = {'User-agent': 'Telexon Bot Requests ' + datetime.now().strftime('%Y%m%d%H%M%S')})
```
[Basic tutorial on request.get() method](https://www.w3schools.com/PYTHON/ref_requests_get.asp)
Used here:
```python
response = requests.get(redditJsonRequestUrl, headers = {'User-agent': 'Telexon Bot Requests ' + datetime.now().strftime('%Y%m%d%H%M%S')})
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