import requests
from bs4 import BeautifulSoup
from operator import itemgetter

url2 = "http://dktes.com/autonomous/result.php"

'''
# Optional headers if required!!

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
}'''

# You can change these as per your result
gradePoints = {
'O':10,'A+':9,'A':8,'B+':7,'B':6,'C':5,'P':4,'F':0,'D':0,'AB':0
}

# These credits correspond to subjects shown in result respectively can change them based on your result
credits = [4,3,3,3,4,5,1,2]

# total credits available change according to your branch
total_credits = 25

# your seatno file ensure each seatno is on newline
student_seats = open("list.txt", 'r')

# list containing list of students with seatno, name and sgpa of student
sgpa_list = []
for i in student_seats:

    # tempory list to hold seatno, name and sgpa of student
    temp = []
    temp.append(i.strip()) # remove whitespaces or escape sequences if any

    # data to be sent as POST request
    data = {
        'seatno' : str(i),
        'submitme':''
    }

    SGPA = 0
    j =0    # counter to iterate th' credits one by one

    #page = requests.post(url2, data=data, headers=headers)
    page = requests.post(url2, data=data)
    doc = BeautifulSoup(page.text, 'lxml')

    # Grab all of the rows
    table_rows = doc.find_all('tr')
    name_td = table_rows[0].find_all('td')
    name_row = [i.text.strip() for i in name_td]
    temp.append(name_row[1])

    #for tr in table_rows[6:14]:
    for tr in table_rows[6:len(table_rows)-3]:
        td = tr.find_all('td')
        row = [i.text.strip() for i in td]
        #print(row)


        # based on observation 4th row contains our grade
        if row[0] == '4':
            SGPA = SGPA + gradePoints[row[3].lstrip("*")]*credits[j] # to stip out * in condolance
            j+=1
            #print(SGPA)

    temp.append(float("{0:.2f}".format(SGPA/total_credits)))
    sgpa_list.append(temp)

# print(sgpa_list)
sgpa_list.sort(key=itemgetter(2), reverse=True)
#print(sgpa_list)

student_seats.close()

# writing sorted list to file
choice = input("Store result as txt file or csv file (Enter 1 or 2): ")

if choice == '1':
    with open("result.txt",'w') as fp:
        for index, item in enumerate(sgpa_list):
            print(index+1,"->"," ".join(str(i) for i in item), file=fp)
    fp.close()

elif choice == '2':
    with open("result.csv",'w') as fp:
        print("Rank,Seat No,Name, SGPA,",file=fp)
        for index, item in enumerate(sgpa_list):
            print(index+1,",",",".join(str(i) for i in item), file=fp)
    fp.close()

else:
    print("Invalid choice")
