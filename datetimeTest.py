import datetime
import csv
import os
import sqlite3

dateNow = datetime.datetime.now().date()
timeNow = datetime.datetime.now().time()

dateBegin = (2016,6,1)
#dateStart = datetime.date(dateBegin[0],dateBegin[1],dateBegin[2])
dateStart = '2016-06-01'
dateStrt = datetime.datetime.strptime(dateStart, '%Y-%m-%d').date()
print 'dateStrt = ', dateStrt
yearStart = int(dateStart[0:4])
monthStart = int(dateStart[5:7])
dayStart = int(dateStart[8:10])
print dateStart,yearStart,monthStart,dayStart
dateStart = datetime.date(yearStart,monthStart,dayStart)
dateEnd = datetime.date(2016,6,30)

print dateNow,' ',timeNow

if (dateNow >= dateStrt) and (dateNow <= dateEnd):
    print "Course in session"
else:
    print "Course not in session"
