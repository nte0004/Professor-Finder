import requests
import json
from bs4 import BeautifulSoup

collegeList = []
collegeNum = 1
def findSchool(number):
    url = f'https://www.ratemyprofessors.com/school?sid={number}'
    r = requests.get(url)
    if r.status_code == 404:
        errorMSG(r.status_code,number)
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        script = soup.find_all('script')[11].text.strip()[25:-1061]
        soup = BeautifulSoup(r.content, 'html.parser')
        data = json.loads(script)
        school = data['client:root']
        id = list(school)[2][9:-2]
        college = {
            'School' : data[id]['name'],
            'Legacy ID' : data[id]['legacyId'],
            'sid' : data[id]['id']

        }
        collegeList.append(college)
def errorMSG(status, num):
    print(f'HTTPError: {status}, School {num} Does not exist.')

while int(collegeNum) < 6050 :
    findSchool(collegeNum)
    collegeNum = int(collegeNum) + 1
print(json.dumps(collegeList, indent=4, sort_keys=False))