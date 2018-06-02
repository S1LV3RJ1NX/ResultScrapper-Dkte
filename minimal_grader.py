'''This program is used to check if grader works for a single person and test any minute changes'''

import requests
from bs4 import BeautifulSoup

url1 = "http://dktes.com/autonomous/index.php"
url2 = "http://dktes.com/autonomous/result.php"

'''
##Optional headers if required

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '21',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'dktes.com',
    'Origin':'http://dktes.com',
    'Referer':'http://dktes.com/autonomous/index.php',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
}

'''

data = {
'seatno' : '2052',
'submitme':''
}



page = requests.post(url2, data=data)
doc = BeautifulSoup(page.text, 'html.parser')

# Grab all of the rows
row_tags = doc.find_all('tr')

for row in row_tags:
    print(row.text.strip())
