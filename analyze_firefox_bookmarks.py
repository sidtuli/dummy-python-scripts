from html.parser import HTMLParser
import requests
import time

out_file_path = "bookmarks_filter.txt"

def process_links(links):
    results = list()
    
    for link in links:
        try:
            time.sleep(.5)
            response = requests.get(link)
            if response.status_code != 200:
                results.append([response.status_code,link])
        except:
            results.append(["XX",link])
    with open(out_file_path, 'w+') as out_file:
        for result in results:
            print(result)
            out_file.write(' '.join(map(str,result)) + "\n")
    

class MyHTMLParser(HTMLParser):
    links = list()

    def handle_starttag(self, tag, attrs):
        
        #print("Encountered a start tag:", tag)
        for attr in attrs:
            if attr[0] == "href" and tag == "a":
                #print(attr[1])
                self.links.append(attr[1])

    #def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)

    #def handle_data(self, data):
        #print("Encountered some data  :", data)
        

with open('bookmarks-03-13-2025.html', 'r') as file:
    data = file.read().rstrip()
    parser = MyHTMLParser()
    parser.feed(data)

    #print(parser.links)

    process_links(parser.links)





