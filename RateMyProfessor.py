import requests
import json
from bs4 import BeautifulSoup

inputPrompt = input('Please input the first and last names of the professor you would like to search, seperate each name with a comma: ')
inputList = inputPrompt.split(', ') # Input List now in format [First Last, First Last, ...]

sid = 'U2Nob29sLTYw' #This is auburn's school id, the ratemyprofessor api converts this value to a number 1-6049 for each college, Auburn's is 60, so U2Nob29sLTYw = 60.
professorNames = []
professorInfo = []
for name in inputList:
    professorNames.append(name.split(' ')) # Professors List now in format [[First, Last], [First, Last], ...]

def lookupProfessor(firstName, lastName):
    pageUrl = f'https://www.ratemyprofessors.com/search/teachers?query={firstName}%20{lastName}&sid={sid}'
    r = requests.get(pageUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.find_all('script')[10].text.strip()[25:-1061] # This part finds the script containing the information, and isolates the json string
    getProfessorInfo(script, firstName, lastName)

def getProfessorInfo(JSON_String, first, last):
    data = json.loads(JSON_String)
    bs, open, close = '\"', '{\"', '\"}' # formatting variables to use f string in the refString
    resultString = f'client:root:newSearch:teachers(after:{bs}{bs},first:8,query:{open}fallback{bs}:true,{bs}schoolID{bs}:{bs}U2Nob29sLTYw{bs},{bs}text{bs}:{bs}{first} {last}{close})'
    resultCount = int(data[resultString]['resultCount']) #Results = number of edges = number of professors
    if resultCount == 0 :
        profDNE(first, last, resultCount)
        return
    resultEdges = data[resultString]['edges']['__refs'] #List of edges, where each edge represents a different professor that matched the search
    for edge in resultEdges : #each edge contains a node that references the professor's ID, which is saved as the profRef
        profRef = data[edge]['node']['__ref']
        tid = data[profRef]['legacyId'] #In the profRef the tid is found to complete the url to the professor's webpage
        schoolID = data[profRef]['school']['__ref'] #The schoolID that they are at is found, this will also be used to make sure it shows professors for the right school
        schoolName = data[schoolID]['name']

        if schoolID != sid :
            profDNE(first, last, resultCount)
            return

        else :
            professor = {
                'First Name' : data[profRef]['firstName'],
                'Last Name' : data[profRef]['lastName'],
                'School' : schoolName,
                'Department' : data[profRef]['department'],
                'Rating' : data[profRef]['avgRating'],
                'Difficulty' : data[profRef]['avgDifficulty'],
                'Taken Again %' : str(data[profRef]['wouldTakeAgainPercent']).replace('-1', 'NA'),
                'Reviews' : data[profRef]['numRatings'],
                'Professor Page' : f'https://www.ratemyprofessors.com/professor?tid={tid}'
            }
            professorInfo.append(professor)

def profDNE(first, last, resultCount) : #This function catches instances where there are no results, or results not matching the correct school
    if resultCount == 0 :
        professor = {
            'First Name' : first,
            'Last Name' : last,
            'Error' : 'No professor by this name found, make sure the name is correct.'
        }
        professorInfo.append(professor)
    else :
        professor = {
        'First Name' : first,
        'Last Name' : last,
        'Error' : f'{resultCount} professor(s) matched the search for this name, but they are not at your school.'
        }
        professorInfo.append(professor)

for name in professorNames:
    lookupProfessor(name[0], name[1]) #name[0] is the first name of a professor, name[1] is the last name of a professor

print(json.dumps(professorInfo, indent=4, sort_keys=False))

