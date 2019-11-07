import requests

url = {
    'armor': 'https://mhw-db.com/armor',
    'items': 'https://mhw-db.com/items',
    'skills': 'https://mhw-db.com/skills',
    'weapons': 'https://mhw-db.com/armor'
}
api = {}

for key in url.keys():
    data = requests.get(url[key])
    api[key] = data.json()
