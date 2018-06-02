import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import os

url2 = "http://dktes.com/autonomous/result.php"
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

marks = {
'O':10,'A+':9,'A':8,'B+':7,'B':6,'C':5,'P':4,'F':0,
}

credits = [4,3,3,3,4,5,1,2]

f = open("list.txt", 'r')
g = open("result.txt", 'w')


for i in f:
    print(i.strip(), end=" ", file=g)
    data = {
    'seatno' : str(i),
    'submitme':''
    }


    CGPA = 0
    j =0
    page = requests.post(url2, data=data, headers=headers)
    doc = BeautifulSoup(page.text, 'lxml')

    # Grab all of the rows
    table_rows = doc.find_all('tr')
    name_td = table_rows[0].find_all('td')
    name_row = [i.text.strip() for i in name_td]
    print(name_row[1], end=" ",file=g)

    for tr in table_rows[6:14]:
        td = tr.find_all('td')
        row = [i.text.strip() for i in td]
        CGPA = CGPA + marks[row[3].lstrip("*")]*credits[j]
        j+=1

    print("CGPA:- ",CGPA/25,file=g)

f.close()
g.close()
g = open("result.txt", 'r')
cg = []

for line in g:
    s = line.strip().split()
    s[-1] = float(s[-1])
    cg.append(s)
y = sorted(cg, key=itemgetter(5), reverse=True)

with open("result_final.txt",'w') as fp:
    for item in y:
        fp.write(" ".join(str(i) for i in item))
        fp.write('\n')

g.close()
os.remove('result.txt')
