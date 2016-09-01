def parentContact():

    # Report a contact with a parent
    print 'Made it to Parent Contact'

    import csv
    import os
    import sqlite3
    import datetime

    # Open the classTrack database
    conn = sqlite3.connect('classTrack-DB.sqlite')
    ct = conn.cursor()

    os.system('clear')

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

    # Check which type of contact to records

    typeContactList = ct.execute('''
                        SELECT * FROM typecontact''');
    for item in typeContactList:
        print item[0], item[1]

    tcChoice = int(raw_input('Enter the type of contact ID you would like to record: '));
    print 'You have selected item number: ', tcChoice

    raw_input('Press any key to continue')

    # Now locate the student for which the record applies

    studentList = ct.execute('''
                    SELECT
                     enroll.id ,
                     student.nameLast ,
                     student.nameFirst ,
                     course.id
                    FROM
                     student
                     JOIN course ON enroll.course_id = course.id
                     JOIN enroll ON student.id = enroll.student_id
                    WHERE
                     semester_id = ?
                    ORDER BY
                     student.nameLast,
                     student.nameFirst
                ''', (semester_id,));

    students = []
    for pupil in studentList:
        students.append(pupil)

    col_width = max(len(str(word)) for row in students for word in row) + 2
#    print 'The column width is: ',col_width
    studentEnrollID={}
    itemNum = 0
    print '\n\nEnroll_ID---------Last--------------First-------------Course_ID--------------------'
    for row in students:
        print '--------------------------------------------------------------------------------'
        print "".join(str(word).ljust(col_width) for word in row)
        itemNum += 1
        studentEnrollID[row[0]]=(row[0], row[1], row[2], row[3])

    enrollID = int(raw_input('\n\nEnter the enrollment ID of the student:  '))

    print '\nYou selected: ', "".join(str(word).ljust(col_width) for word in studentEnrollID[enrollID])

    ans = raw_input('\nIs this the correct student? (Y/N) ' );
    if (ans=='y' or ans=='Y'):
        reDisciplineID = raw_input('\nRegarding which discipline ID? (0 for None) ');
        dateContact = raw_input('\nEnter the date of the contact: (mm/dd/yyyy)');
        if dateContact=='n' : dateContact = dateNow
        nameContact = raw_input('\nEnter the name of the contact: ');
        reasonContact = raw_input('\nReason: \n');
        actionNeeded = raw_input('\nAction needed: \n');

        # Write the contact record to the database

        ct.execute('''
                    INSERT INTO parentContacts
                    (enroll_id,typecontact_id,dateSubmitted,nameContacted,reason,actionNeeded,reDiscID)
                    VALUES (?,?,?,?,?,?,?)
                    ''', (enrollID, tcChoice, dateContact, nameContact, reasonContact, actionNeeded, reDisciplineID));

    raw_input('press any key to continue')

#----------------------END MODULE-----------------------------------------------
    os.system('clear')
    conn.commit()
    ct.close()
