import requests
import json
from bs4 import BeautifulSoup
 
def getScript(link:str):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser') # Pull html content from professor webpage
    #allscript = soup.find_all('script')
    #print(allscript)

    for script in soup.find_all('script'):
        if len(script) == 1:
            if script.text.strip()[0:8] == 'window._':
                return cleanScript(script.text.strip())

    # cleanScript finds the beginning and end points of the JSON string so that it can return the valid JSON string that contains
    # all of the professor information.
def cleanScript(soupScript):
    key = -860
    while soupScript[key] != ';':   #Check each character until it finds the end of the JSON string
        key -= 1
    JSONstring = str(soupScript[25:key])
    return JSONstring


def getComments(content:str):
    reviewList = [] #List of keys referencing each review in content
    commentList = [] #List of dicts for each comment
    data = json.loads(content)
    prof = data['client:root']
    profID = data['client:root'][list(prof)[2]]['__ref']
    reviewIDList = data[f'client:{profID}:ratings(first:20)']['edges']['__refs']
    for reviewID in reviewIDList[:5]: #First 5 of up to 20 reviews are fetched
        reviewList.append(data[reviewID]['node']['__ref'])
    for review in reviewList:
        comment = {
            'Class' : str(data[review]['class']),
            'Comment' : str(data[review]['comment'])
        }
        commentList.append(comment)
    return commentList

def main(link:str):
    content = getScript(link)
    comments = getComments(content)
    return comments


