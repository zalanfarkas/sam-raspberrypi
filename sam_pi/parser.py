#-------------------------------------------------------------------------------
# Name:        Parser Class
# Purpose:
#
# Author:      Vladimir
#
# Created:     24/01/2018
# Copyright:   (c) V.Yesipov 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests

class Parser:

    def __init__(self,uid):
        self.uid = uid

    def parse(self):
        #parse the file on the post

        # defining the api-endpoint
        API_ENDPOINT = "http://aberdeen-sam.herokuapp.com/"
        # your API key here
        API_KEY = "XXXXXXXXXXXXXXXXX"

        # data to be sent to api        
        data={'uid':str(self.uid), 'type':'nfc', 'data':'id'}
        
        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT, data = data)

        # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is:%s"%pastebin_url)

'''
    def validate(self,uid):
        for vlue in uid:
            if value == valid:
            #add this value into the file
'''



#Parsing json
'''
import requests
import simplejson

r = requests.get('https://github.com/timeline.json')
c = r.content
j = simplejson.loads(c)

for item in j:
    print item['repository']['name']
'''

#writing json
'''
import json

data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
'''

#Reading json
'''
import json

with open('data.txt') as json_file:
    data = json.load(json_file)
    for p in data['people']:
        print('Name: ' + p['name'])
        print('Website: ' + p['website'])
        print('From: ' + p['from'])
        print('')
'''

