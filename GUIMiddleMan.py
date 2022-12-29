import RateMyProfessor
import schoolSearch
import rmpGUI

def schoolSearchInput(input):
    #findMatch will return the school and sid, a school List and sid List, or an empty list
    school, sid = schoolSearch.findMatch(str(input))
    if len(school) == 0:
        status = 'Search did not match any schools'
        return None, None, status
    rmpGUI.schoolListBox(school)
    if type(school) is list:
        status = 'Select your school'
        return school, sid, status
    elif type(school) is str:
        status = 'School found'
        return school, sid, status