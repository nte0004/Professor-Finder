import requests
import json
from bs4 import BeautifulSoup
import csv

collegeList = []

def findSchool(collegeNum):
    url = f'https://www.ratemyprofessors.com/school?sid={collegeNum}'
    r = requests.get(url)
    if r.status_code == 404:
        return
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

def toCSV(fileName):
    fields = ['School','Legacy ID', 'sid']
    with open(fileName, 'w', newline='') as f:
        dataWrite = csv.DictWriter(f, fieldnames=fields) 
        dataWrite.writeheader()
        dataWrite.writerows(collegeList)

def requestYN(fileName):
    request = input(f'The data has been found, put data in {fileName}? (yes/no): ')
    if request.lower() == 'yes':
        toCSV(fileName)
    elif request.lower() == 'no':
        print('Exiting program')
        return
    else:
        requestYN(fileName)

def main():
    fileName = '' #Name of file to write to
    collegeNum = 1
    maxCount = 6049 #6049 is believed to be the true max count. 
    for collegeNum in range(maxCount):
        findSchool(collegeNum)
    requestYN(fileName)
    exit(0)
    

if __name__ == '__main__' :
    main()
