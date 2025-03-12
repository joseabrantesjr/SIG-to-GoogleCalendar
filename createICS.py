from icalendar import Calendar, Event
import datetime

class ICS:
    def __init__(self, schedule, startDate, endDate, fileName):
        self.schedule = schedule
        self.startDate = self.createDate(startDate)
        self.endDate = self.createDate(endDate)
        self.fileName = fileName

    def createDate(self, date):
        day, month, year = map(int, date.split('/'))
        return datetime.date(year, month, day)

    def writeFile(self):
        print(f'Writing in {self.fileName}')
        cal = Calendar()
        actualDate = self.startDate

        for _ in range(abs((self.endDate - self.startDate).days) + 1):
            weekDay = actualDate.weekday()
            for classs in self.schedule[weekDay]:
                event = Event()
                event.add('summary', classs[0])
                start_time = datetime.datetime.strptime(classs[2], "%I:%M %p").time()
                end_time = datetime.datetime.strptime(classs[4], "%I:%M %p").time()
                event.add('dtstart', datetime.datetime.combine(actualDate, start_time))
                event.add('dtend', datetime.datetime.combine(actualDate, end_time))
                event.add('location', classs[5])
                event.add('description', 'Aula cadastrada automaticamente.')
                cal.add_component(event)

            actualDate += datetime.timedelta(days=1)

        with open(self.fileName, 'wb') as f:
            f.write(cal.to_ical())

        print('Done!')
