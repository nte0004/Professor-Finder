import requests
import json
from bs4 import BeautifulSoup
def getScript(link:str):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser') # Pull html content from professor webpage
    #allscript = soup.find_all('script')
    #print(allscript)
    script = soup.find_all('script')[11].text.strip() #Locate the <script></script> where useful info is
    key = -863
    while script[key] != ';':
        key -= 1
    content = script[25:key] #This is the JSON string that contains useful info on professor
    return content

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


