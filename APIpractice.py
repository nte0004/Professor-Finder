#uses PunkAPI, for practice, punkapi.com
import json
import requests
from random import randint

food_choice = input('Please enter your dinner choice!: ')

url = f'https://api.punkapi.com/v2/beers?food={food_choice}'    #f string used to input directly into link
r = requests.get(url)
data = json.loads(r.text)

beerList = []

for beer in data:
    name = beer['name']
    tagline = beer['tagline']
    abv = beer ['abv']

    beer_item = {
        'name': name,
        'tagline' : tagline,
        'abv' : abv
    }
    beerList.append(beer_item)

val = randint(0,len(beerList))
recommendation = beerList[val]
recName = recommendation['name']
recTagline = recommendation['tagline']
recAbv = recommendation['abv']
print(f'We recommend {recName}, {recTagline} {recAbv}%')
