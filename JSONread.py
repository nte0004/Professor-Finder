import json
#import requests

personList = []

with open('generated.json') as json_file:
    data = json.load(json_file)
    for item in data:
        name = item['name']
        email = item['email']
        balance = item['balance']

        person =  {
            'name' : name,
            'email' : email,
            'balance' : balance
        }
        personList.append(person)
print(personList)