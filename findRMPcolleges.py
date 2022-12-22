import requests
import json
from bs4 import BeautifulSoup

collegeList = []

collegeNum = 1
def findSchool(number):
    url = f'https://www.ratemyprofessors.com/school?sid={number}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.find_all('script')[11].text.strip()[25:-1061]
    data = json.loads(script)
    school = data['client:root'][2]['__ref']
    print(school)
while int(collegeNum) < 2 :
    findSchool(collegeNum)
    collegeNum = int(collegeNum) + 1
print(collegeList)