def discipline():
    print 'Made it to discipline'

    import csv
    import os
    import sqlite3
    import datetime

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

    # Now locate the current course that is in session at this time
    try:
        courses = ct.execute('''
                            SELECT * FROM course JOIN period
                            ON course.period_id=period.id
                            WHERE semester_id=?
                            ''',(semester_id,));

    except:
        print 'There is not currently a course in session.'
        raw_input( 'Press any key to continue...' )
        os.system('clear')
        conn.commit()
        ct.close()

    chkit = 'stay'
    course_id = -1

    courseID = list()
    try:
        for crs in courses:
            print crs
            courseID.append(crs[0])
            timeFirst = crs[6]
            timeLast = crs[7]
            timeFirst = datetime.datetime.strptime(timeFirst, '%H:%M:%S.%f').time()
            timeLast = datetime.datetime.strptime(timeLast, '%H:%M:%S.%f').time()
            print timeNow, timeFirst, timeLast
            if (timeNow >= timeFirst) and (timeNow <= timeLast):
                print 'Got it'
                course_id = crs[0]
                print 'the course currently in session is ',course_id
            else:
                print 'searching...'
    except:
        print 'Error occured locating course in session'
        chkit = 'end'

    while course_id == -1:
        print '\nNo course is currently in session.'
        course_id = raw_input('\nEnter the course id for which you would like to make a report: ')
        course_id = int(course_id)
        print 'You entered: ',course_id
        print 'Current courses: ',courseID
        if course_id not in courseID:
            print '\nYou have entered an invalid course id. Please try again.\n'
            course_id = -1

    while len(chkit)>3:
        os.system('clear')

        # Now grab the student roster for the current course_id
        students = ct.execute('''
            SELECT e.id, e.course_id, s.nameLast, s.nameFirst
            FROM enroll as e JOIN student as s
            ON e.student_id = s.id
            WHERE e.course_id=? ''',(course_id,));

        enrollees = {}
        for pupil in students:
            print pupil[0],': ',pupil[2],', ',pupil[3]

            enrollees[pupil[0]] = (pupil[2], pupil[3])
            print pupil[0], enrollees[pupil[0]]
        enroll_id = raw_input('\n\nDiscipline Report for which student? ')
        enroll_id = int(enroll_id)
        print enroll_id
        try:
            print 'You have selected student number: '
            print enroll_id, enrollees[enroll_id]
        except:
                'The student you entered is not in our records. Please try again.'
                chkit = 'stay'

        raw_input ('Press any key to continue.')
        os.system('clear')

        # Print the students information to date
        # Print incidentTotals

        incTotals = ct.execute('''
            SELECT * FROM incidentTotals
            JOIN typeIncident
            ON incidentTotals.typeIncident_id=typeIncident.id
            WHERE incidentTotals.enroll_id=?
            ''',(enroll_id,));


        for item in incTotals:
            if len(item) > 0 :
                print item
            else:
                print '\nThis student has no prior classroom incidents.\n\n'

        response = raw_input('\n\nWould you like to report a new incident for this student? (Y/N)')

        if response == 'Y' or response == 'y':
            os.system('clear')

            incidentList = ct.execute('''
            SELECT * FROM typeIncident
            ''');

            for item in incidentList:
                print item[0],item[1]

            incID = int(raw_input('\nPlease enter the incident ID you would like to report: '));

            incDate = raw_input('\nPlease enter the date of the incident: (mm/dd/yyyy)');
            if incDate == 'n': incDate = str(dateNow)

            incTime = raw_input('\nPlease enter the time of the incident: (hh:mm)');
            if incTime == 'n': incTime = str(timeNow)

            incComment = raw_input('\nPlease enter a short description or comment about the incident: ');

            # Write the incident to the database

            ct.execute("""
            INSERT OR IGNORE INTO classIncident(incDate,incTime,enroll_id,typeincident_id,comment)
            VALUES (?, ?, ?, ?, ?)""",(incDate,incTime,enroll_id,incID,incComment));

            # Now update the incident totals report
            try:
                newCount = 0
                incToUpdate = ct.execute("""
                            SELECT * FROM incidentTotals
                            WHERE (typeIncident_id = ? AND enroll_id = ?)
                            """,(incID,enroll_id));
                for item in incToUpdate:
                    newCount = item[3]+1
                ct.execute("""
                UPDATE incidentTotals
                SET counts = ?
                WHERE (typeIncident_id = ? AND enroll_id = ?)
                """,(newCount,incID,enroll_id));
            except:
                ct.execute("""
                INSERT OR IGNORE INTO incidentTotals(enroll_id,typeincident_id,counts)
                VALUES (?,?,?)
                """, (enroll_id,incID,1));
            chkit = 'end'



        else:
            chkit = 'end'
            print 'Returning to main menu.'
            continue


#----------------------END MODULE-----------------------------------------------
    os.system('clear')
    conn.commit()
    ct.close()
