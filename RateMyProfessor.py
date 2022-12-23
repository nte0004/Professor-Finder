import requests
import json
from bs4 import BeautifulSoup


sid = 'U2Nob29sLTYw' #This is Auburn University's school id, to be used in the search.
professorNames = []
professorInfo = []

#requestNames ask the user for the names of the professors to search.
#   That input is put in the inputList, then it is further seperated to first and last names in the professorNames list.
def requestNames():
    inputPrompt = input('Please input the first and last names of the professor you would like to search, seperate each name with a comma: ')
    inputList = inputPrompt.split(', ')
    for name in inputList:
        professorNames.append(name.split(' '))

#lookupProfessor takes the first and last name of each inputted name from the user and searches for the results of
#   that name on the rate my professor webiste. The information needed is all in a script from the source code of
#   the professor page. The JSON aspect of that script is isolated and then the function calls getProfessorInfo to
#   further isolate the correct information.
def lookupProfessor(firstName, lastName):
    pageUrl = f'https://www.ratemyprofessors.com/search/teachers?query={firstName}%20{lastName}&sid={sid}'
    r = requests.get(pageUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.find_all('script')[10].text.strip()[25:-1061]
    getProfessorInfo(script, firstName, lastName)

#getProfessorInfo creates and navigates a data dictionary with the script found with lookupProfessor.
#   The script is converted to a JSON string then navigated in the usual dictionary methods. 
#   Once all the information needed is found, it creates a Professor object and adds it to the PrefessorInfo list.
def getProfessorInfo(JSON_String, first, last):
    data = json.loads(JSON_String)
    bs, open, close = '\"', '{\"', '\"}' # formatting variables to use f string in the refString
    resultString = f'client:root:newSearch:teachers(after:{bs}{bs},first:8,query:{open}fallback{bs}:true,{bs}schoolID{bs}:{bs}U2Nob29sLTYw{bs},{bs}text{bs}:{bs}{first} {last}{close})'
    resultCount = int(data[resultString]['resultCount'])
    if resultCount == 0:
        profDNE(first, last, resultCount)
        return
    resultEdges = data[resultString]['edges']['__refs']

    for edge in resultEdges: #Each edge is essentially a different professor found in the query
        profRef = data[edge]['node']['__ref']
        tid = data[profRef]['legacyId']
        profSchoolID = data[profRef]['school']['__ref']
        schoolName = data[profSchoolID]['name']

        if profSchoolID != sid: #When the professor being looked at is not the right school
            profDNE(first, last, resultCount)
            return

        else:
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

#This function deals with instances where there are no results, or results not matching the correct school
def profDNE(first, last, resultCount):
    if resultCount == 0:
        professor = {
            'First Name' : first,
            'Last Name' : last,
            'Error' : 'No professor by this name found, make sure the name is correct.'
        }
        professorInfo.append(professor)
    else:
        professor = {
        'First Name' : first,
        'Last Name' : last,
        'Error' : f'{resultCount} professor(s) matched the search for this name, but they are not at your school.'
        }
        professorInfo.append(professor)

def main():
    requestNames()
    for name in professorNames:
        lookupProfessor(name[0], name[1])
    print(json.dumps(professorInfo, indent=4, sort_keys=False))
    exit(0)
    

if __name__ == '__main__':
    main()
