def reports():
    # Output report of necessary parent contacts
    
    import csv
    import os
    import sqlite3
    import datetime

    os.system('clear')
    print 'Made it to Reports'

    # Open the classTrack database
    conn = sqlite3.connect('classTrack-DB.sqlite')
    ct = conn.cursor()



    # Determine the current date and time -- now
    dateNow = datetime.datetime.now().date()
    dateNow = str(dateNow)
    timeNow = datetime.datetime.now().time()
    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    attendanceDate_id = str(datestamp)

    print dateNow,' ',timeNow

    # Locate the current semester that is in session
    semester_id = -1
    semesters = ct.execute('''SELECT * FROM semester ''');

    for sem in semesters:
        dateFirst = sem[3]
        dateLast = sem[4]

        print sem
        #print dateNow, dateFirst, dateLast
        dateFirst = datetime.datetime.strptime(dateFirst, '%Y-%m-%d').date()
        dateLast = datetime.datetime.strptime(dateLast, '%Y-%m-%d').date()
        dateNow = datetime.datetime.strptime(dateNow, '%Y-%m-%d').date()
        print dateFirst, dateLast, dateNow
        if (dateNow >= dateFirst) and (dateNow <= dateLast):
            print "Got it"
            semester_id = sem[0]
            print "Current semester id = ",semester_id
            daysPast = dateNow - dateFirst
            daysPast = int(daysPast.days)
            daysTotal = dateLast-dateFirst
            daysTotal = int(daysTotal.days)
            daysLeft = daysTotal-daysPast
            print "days: ",dateNow,daysPast,daysLeft,daysTotal
            break
        else:
            print 'searching...'

    raw_input('Press any key to continue')









#----------------------END MODULE-----------------------------------------------
    os.system('clear')
    conn.commit()
    ct.close()
