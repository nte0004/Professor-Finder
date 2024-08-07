import json
from bs4 import BeautifulSoup

#lookupProfessor takes the first and last name of each inputted name from the user and searches for the results of
#   that name on the rate my professor webiste. The information needed is all in a script from the source code of
#   the professor page. The JSON aspect of that script is isolated and then the function calls cleanScript to
#   further isolate the correct information.
def lookupProfessor(firstName: str, lastName: str, target_SID: str, session):
    pageUrl = f'https://www.ratemyprofessors.com/search/professors/{target_SID}?q={firstName}%20{lastName}'
    r = session.get(pageUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
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

#getProfessorList creates and navigates a data dictionary from the JSON string found with lookupProfessor.
#   The resultString (name of the object holding the needed information) is really hacked together but it works! 
#   Once all the information needed is found, it creates a Professor object and adds it to the PrefessorInfo list.
def getProfessorList(JSON_String: str):
    data = json.loads(JSON_String)
    resultString = 'client:root:newSearch:' + str(list(data['client:root:newSearch'])[2])
    resultCount = int(data[resultString]['resultCount'])
    professorList = data[resultString]['edges']['__refs']
    return professorList, resultCount, data

def getProfessorInfo(professor:str, data:dict, target_SID:str, resultCount:int, targetProf:str):
    prof_ID = data[professor]['node']['__ref']
    legacy_ID = data[prof_ID]['legacyId']
    school_ID = data[prof_ID]['school']['__ref']
    school_Name = data[school_ID]['name']
    first_Name = data[prof_ID]['firstName']
    last_Name = data[prof_ID]['lastName']
    firstLast = first_Name + last_Name
   
    profStat = {'isFound': False, 'details': None}

    if (firstLast.lower() == targetProf.lower()):
        profStat['isFound'] = True    

    if (school_ID != target_SID):
        profStat['details'] = None
    else:
        professor = {
            'First Name' : first_Name,
            'Last Name' : last_Name,
            'School' : school_Name,
            'Department' : data[prof_ID]['department'],
            'Rating' : str(data[prof_ID]['avgRating']) + '/5',
            'Difficulty' : str(data[prof_ID]['avgDifficulty']) + '/5',
            'Would Take Again' : str(data[prof_ID]['wouldTakeAgainPercent']).replace('-1', 'NA') + '%',
            'Reviews' : data[prof_ID]['numRatings'],
            'Professor Page' : f'https://www.ratemyprofessors.com/professor?tid={legacy_ID}'
        }
        profStat['details'] = professor

    return profStat

#This function deals with instances where there are no results, or results not matching the correct school
def badResult(first: str, last: str, resultCount: int):
    if resultCount == 0:
        professor = {
            'First Name' : first,
            'Last Name' : last,
            'Error' : 'No professor(s) found with this name.'
        }
        return professor
    else:
        professor = {
        'First Name' : first,
        'Last Name' : last,
        'Error' : f'{resultCount} professor(s) found. None at this school.'
        }
        return professor

# main is receiving a list of professor names along with the sid to search for from rmp-gui,
#   - For each professor name received it will call lookupProfessor to get a JSON string containing professor info.
#   - Then it will call getProfessorList to create list of all the professors found on 
#       ratemyprofessor's search of the user-input name. 
#   - Then for each of those professors from the website, it will call getProfessorInfo to create the professor object
#       which is then stored in professorInfo.
#   - Finall the list of professor objects is returned to rmp-gui where they will be display in the results window.
#
def main(professorNames:list, target_SchoolID:str, session):
    professorInfo = []
    
    if len(professorNames) == 0:
        raise ValueError
    
    for name in professorNames:
        firstName = name[0]
        lastName = name[1]
    
        contents = lookupProfessor(firstName, lastName, target_SchoolID, session)
        professorList, professorCount, data = getProfessorList(contents)
        
        if professorCount == 0:
            NoProfessor = badResult(firstName, lastName, professorCount)
            professorInfo.append(NoProfessor)
        else:
            targetProf = firstName + lastName
            oneOrMoreMatches = False
            localResults = []

            for professorAddr in professorList:
                profStat = getProfessorInfo(str(professorAddr), data, target_SchoolID, professorCount, targetProf)
                profFound = profStat['isFound']
                professor = profStat['details']
                
                if profFound:
                    oneOrMoreMatches = True
                    professorInfo.append(professor)
                elif professor is not None:
                    localResults.append(professor)
                
            if not oneOrMoreMatches:
                # Return up to first three search results
                for prof in localResults[:3]:
                    professorInfo.append(prof)

    return professorInfo

