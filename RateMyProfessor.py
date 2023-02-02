import requests
import json
from bs4 import BeautifulSoup
import schoolSearch

professorNames = []
professorInfo = []
scriptKey = -945

#requestNames ask the user for the names of the professors to search.
#   That input is put in the inputList, then it is further seperated to first and last names in the professorNames list.
def requestNames(profInput:str):
    inputList = profInput.strip().split(',')
    for name in inputList:
        professorNames.append(name.strip().split(' ', 1))

#lookupProfessor takes the first and last name of each inputted name from the user and searches for the results of
#   that name on the rate my professor webiste. The information needed is all in a script from the source code of
#   the professor page. The JSON aspect of that script is isolated and then the function calls getProfessorInfo to
#   further isolate the correct information.
def lookupProfessor(firstName: str, lastName: str, target_SID: str):
    pageUrl = f'https://www.ratemyprofessors.com/search/teachers?query={firstName}%20{lastName}&sid={target_SID}'
    r = requests.get(pageUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.find_all('script')[10].text.strip()
    contents = script[25:scriptKey]
    if contents[-3:-1] == 'l}':
        getProfessorInfo(contents, firstName, lastName, target_SID)
    else:
        key = -1061
        while script[key] != ';':
            key += 1
        print('\n****\n', f'New Key for Script: {str(key)}', '\n****\n')

#getProfessorInfo creates and navigates a data dictionary with the script found with lookupProfessor.
#   The script is converted to a JSON string then navigated in the usual dictionary methods. 
#   Once all the information needed is found, it creates a Professor object and adds it to the PrefessorInfo list.
def getProfessorInfo(JSON_String: str, first: str, last: str, target_SID: str):
    data = json.loads(JSON_String)
    bs, open, close = '\"', '{\"', '\"}' # formatting variables to use f string in the refString
    resultString = f'client:root:newSearch:teachers(after:{bs}{bs},first:8,query:{open}fallback{bs}:true,{bs}schoolID{bs}:{bs}{target_SID}{bs},{bs}text{bs}:{bs}{first} {last}{close})'
    resultCount = int(data[resultString]['resultCount'])
    if resultCount == 0:
        badResult(first, last, resultCount)
        return
    professorList = data[resultString]['edges']['__refs']

    for professor in professorList:
        prof_ID = data[professor]['node']['__ref']
        legacy_ID = data[prof_ID]['legacyId']
        school_ID = data[prof_ID]['school']['__ref']
        school_Name = data[school_ID]['name']

        if school_ID != target_SID:
            badResult(first, last, resultCount)
            return

        else:
            professor = {
                'First Name' : data[prof_ID]['firstName'],
                'Last Name' : data[prof_ID]['lastName'],
                'School' : school_Name,
                'Department' : data[prof_ID]['department'],
                'Rating' : str(data[prof_ID]['avgRating']) + '/5',
                'Difficulty' : str(data[prof_ID]['avgDifficulty']) + '/5',
                'Would Take Again' : str(data[prof_ID]['wouldTakeAgainPercent']).replace('-1', 'NA') + '%',
                'Reviews' : data[prof_ID]['numRatings'],
                'Professor Page' : f'https://www.ratemyprofessors.com/professor?tid={legacy_ID}'
            }
            professorInfo.append(professor)

#This function deals with instances where there are no results, or results not matching the correct school
def badResult(first: str, last: str, resultCount: int):
    if resultCount == 0:
        professor = {
            'First Name' : first,
            'Last Name' : last,
            'Error' : 'No professor(s) found with this name.'
        }
        professorInfo.append(professor)
    else:
        professor = {
        'First Name' : first,
        'Last Name' : last,
        'Error' : f'{resultCount} professor(s) found. None at this school.'
        }
        professorInfo.append(professor)

def main(professorsString, target_SchoolID):
    if len(professorsString) == 0:
        raise ValueError
    requestNames(professorsString)
    for name in professorNames:
        lookupProfessor(name[0], name[1], target_SchoolID)
    return professorInfo
