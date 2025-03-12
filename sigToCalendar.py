import requests
import sys
import getpass
import urllib3
import numpy as np
from pathlib import Path
from bs4 import BeautifulSoup
from createCSV import CSV
from createICS import ICS
from urllib.parse import urljoin

class Schedule:
    def __init__(self, info):
        self.info = info
        self.sigURL = 'https://sig.ufla.br/modulos/login/index.php'
        self.scheduleURL = 'https://sig.ufla.br/modulos/alunos/utilidades/horario.php'
        self.session = requests.Session()

    def getClassSchedule(self):
        pageData = self.connectToSIG()
        self.findFormAndLogin(pageData)
        print("Extracting data...")
        schedulePage = self.session.get(self.scheduleURL, verify=False)
        soup = BeautifulSoup(schedulePage.text, 'html.parser')
        scheduleBoard = soup.find('tbody')
        matrix = [[td.text for td in tr.findAll('td')] for tr in scheduleBoard.findAll('tr')]
        scheduleDict = {i: [] for i in range(7)}
        for index, row in enumerate(matrix):
            matrix[index][0] = self.correctTime(row[0])
        matrix = np.array(matrix)
        for row in matrix:
            for i in range(1, 8):
                if row[i] != '-':
                    classAndLocation = row[i].split(' - ')
                    classCode = classAndLocation[0].split(' ')[0]
                    className = classCode + ' - ' + soup.find('abbr', string=classCode)['title'].split(' / ')[0]
                    scheduleIndex = (i - 2) % 7
                    scheduleDict[scheduleIndex].append([className, '', row[0], '', self.endDate(row[0]), classAndLocation[1]])
        print("Data extracted!")
        return scheduleDict

    def endDate(self, time):
        hour = int(time.split(':')[0]) + 1
        period = "PM" if "PM" in time else "AM"
        return f"{hour}:00 {period}"

    def correctTime(self, time):
        hour = int(time.split(':')[0])
        return f"{hour % 12}:00 {'PM' if hour >= 12 else 'AM'}"

    def findFormAndLogin(self, formData):
        soup = BeautifulSoup(formData, 'html.parser')
        form = soup.find('form')
        fields = form.findAll('input')
        formdata = {field.get('name'): field.get('value') for field in fields}
        formdata['login'] = self.info['login']
        formdata['senha'] = self.info['password']
        posturl = urljoin(self.sigURL, form['action'])
        print('Trying to login...')
        response = self.session.post(posturl, data=formdata)
        if response.url != self.sigURL:
            print('Login successful')
        else:
            print('Unable to login. Verify your credentials')
            sys.exit()

    def connectToSIG(self):
        print(f'Connecting to {self.sigURL} ...')
        page = self.session.get(self.sigURL, verify=False)
        if page.status_code == 200:
            print('Connected!')
            return page.text
        else:
            print(f'Unable to connect to {self.sigURL}. Aborting...')
            sys.exit()


def getInfo():
    return {
        'login': input("Enter your SIG login: "),
        'password': getpass.getpass(prompt='Enter your SIG password: '),
        'startDate': input("Enter the start date (DD/MM/YYYY): "),
        'endDate': input("Enter the end date (DD/MM/YYYY): "),
        'fileName': 'calendar'
    }


def getInfoFromFile(fileData):
    data = fileData.read().splitlines()
    return {'login': data[0], 'password': data[1], 'startDate': data[2], 'endDate': data[3], 'fileName': data[4]}


if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    configFile = Path("data.config")
    info = getInfoFromFile(open('data.config', "r")) if configFile.exists() else getInfo()
    schedule = Schedule(info).getClassSchedule()
    CSV(schedule, info['startDate'], info['endDate'], f"{info['fileName']}.csv").writeFile()
    ICS(schedule, info['startDate'], info['endDate'], f"{info['fileName']}.ics").writeFile()