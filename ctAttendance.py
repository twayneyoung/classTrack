def attendance():

# Create a report of actual absences based on the Sign In and Sign out times

    import csv
    import os
    import sqlite3
    import datetime


    # Open the classTrack database
    conn = sqlite3.connect('classTrack-DB.sqlite')
    ct = conn.cursor()

    os.system('clear')
    print "made it to ctStudents";


    # Determine the current date and time -- now

    dateNow = datetime.datetime.now().date()
    #dateNow = datetime.date(2016,4,8)
    timeNow = datetime.datetime.now().time()
    dateNow = str(dateNow)

    print dateNow,' ',timeNow

    attTime = raw_input('\nAre you taking attendance in class (Y/N/U)? ')
    if attTime.upper()=='Y':
        print "yes you are taking attendance in class period"

        # Locate the current semester that is in session
        semesters = ct.execute('''
            SELECT * FROM semester
                    ''');
        for sem in semesters:
            dateFirst = sem[3]
            dateLast = sem[4]

            print dateNow, dateFirst, dateLast
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

        # Update the attendanceDate table
        datestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        strDateStamp = str(datestamp)
        ct.execute('''INSERT OR IGNORE INTO attendanceDate(day,daysPast,daysRemain)
                        VALUES (?,?,?)''', (strDateStamp,daysPast,daysLeft));
        ct.execute(''' SELECT * FROM attendanceDate
                       WHERE attendanceDate.day = ? ''', (strDateStamp,));
        attendanceDate_id = ct.fetchone()[0]
        conn.commit()

        # Now locate the current course that is in session at this time
        courses = ct.execute('''
                                SELECT * FROM course JOIN period
                                ON course.period_id=period.id
                                WHERE semester_id=?
                                ''',(semester_id,));
        try:
            for crs in courses:
                print crs
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
        #
        # Prepare the attendance codesbreak

            aCode = ct.execute('SELECT * FROM attendanceCode ');
            codes={}
            for row in aCode:
                codes[row[2].upper()] = row[0]


        # Now go through the enrolled students and enter attendance data

            enrolled = ct.execute('''
                SELECT *breakoll.student_id=student.id
                    WHERE (enroll.course_id=?)
                    ''',(course_id,));
            attData = []
            for pupil in enrolled:
                print '\n'
                attCode = raw_input('\n'+pupil[21]+' '+pupil[22]+' attendance code: ').upper()
                if attCode == '':
                    attCode = 'PR'
                attendanceCode_id = codes[attCode]
                attData.append((pupil[0],attendanceCode_id))
                print attData
            for item in attData:
                ct.execute('''
                    INSERT OR REPLACE INTO rollcall(attendanceDate_id,enroll_id,attendanceCode_id)
                    VALUES (?,?,?)''', (attendanceDate_id,item[0],item[1]) );
                conn.commit()
        except:
            print "You are not in a current class period."
            raw_input('Enter any key to continue')
            os.system('clear')
            return

    elif attTime.upper()=='N':
        print "you are taking attendance outside the class period."

        # Determine the current date  -- now

        dateNow = datetime.datetime.now().date()
        dateNow = str(dateNow)

        # Locate the current semester that is in session
        semesters = ct.execute('''
            SELECT * FROM semester
                    ''');
        for sem in semesters:
            dateFirst = sem[3]
            dateLast = sem[4]

            print dateNow, dateFirst, dateLast
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

        # Update the attendanceDate table
        datestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        strDateStamp = str(datestamp)
        ct.execute('''INSERT OR IGNORE INTO attendanceDate(day,daysPast,daysRemain)
                        VALUES (?,?,?)''', (strDateStamp,daysPast,daysLeft));
        ct.execute(''' SELECT * FROM attendanceDate
                       WHERE attendanceDate.day = ? ''', (strDateStamp,));
        attendanceDate_id = ct.fetchone()[0]
        conn.commit()

        # List the current courses and ask for selection
        courses = ct.execute('''SELECT * FROM course
                                JOIN period ON course.period_id=period.id
                                WHERE course.semester_id=?''',(semester_id,))
        for crs in courses:
            print crs[0],': Period ',crs[5]

        print '\nPlease select which course to take attendance.'
        course_id = int(raw_input('Course ID: '))
        print '\n'

        # Prepare the attendance codes

        aCode = ct.execute('SELECT * FROM attendanceCode ');
        codes={}
        for row in aCode:
            codes[row[2].upper()] = row[0]

        # Now go through the enrolled students and enter attendance data

        enrolled = ct.execute('''
            SELECT *
            FROM enroll
                JOIN student ON enroll.student_id=student.id
                WHERE (enroll.course_id=?)
                ''',(course_id,));
        attData = []
        for pupil in enrolled:
            print '\n'
            attCode = raw_input('\n'+pupil[21]+' '+pupil[22]+' attendance code: ').upper()
            if attCode == '':
                attCode = 'PR'
            attendanceCode_id = codes[attCode]
            attData.append((pupil[0],attendanceCode_id))
        print attData
        for item in attData:
            ct.execute('''
                INSERT OR IGNORE INTO rollcall(attendanceDate_id,enroll_id,attendanceCode_id)
                VALUES (?,?,?)''', (attendanceDate_id,item[0],item[1]) );
            conn.commit()

#   Now, allow user to update attendance records when a student signs out or
#   arrives late after roll call.

    elif attTime.upper()=='U':
        print 'You have chosen to update your attendance records.'

        # Determine the current date  -- now
        dateChoice = raw_input("Would you like to update today's attendance? (Y/N)")
        if dateChoice.upper()=='Y':
            dateNow = datetime.datetime.now().date()
            dateNow = str(dateNow)
        else:
            print '\nEnter the year, month and date of the attendance records as integers:\n'
            dateYear = int(raw_input('Year: '))
            if dateYear=='': return
            dateMonth = int(raw_input('Month: '))
            dateDay = int(raw_input('Day: '))
            dateNow = datetime.date(dateYear,dateMonth,dateDay)
            dateNow = str(dateNow)

        # Locate the current semester that is in session
        semesters = ct.execute('''
            SELECT * FROM semester
                    ''');
        for sem in semesters:
            dateFirst = sem[3]
            dateLast = sem[4]

            print dateNow, dateFirst, dateLast
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

        # Update the attendanceDate table
        datestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        strDateStamp = str(datestamp)
        ct.execute('''INSERT OR IGNORE INTO attendanceDate(day,daysPast,daysRemain)
                        VALUES (?,?,?)''', (strDateStamp,daysPast,daysLeft));
        ct.execute(''' SELECT * FROM attendanceDate
                       WHERE attendanceDate.day = ? ''', (strDateStamp,));
        attendanceDate_id = ct.fetchone()[0]
        conn.commit()

        # List the current courses and ask for selection
        courses = ct.execute('''SELECT * FROM course
                                JOIN period ON course.period_id=period.id
                                WHERE course.semester_id=?''',(semester_id,))
        for crs in courses:
            print crs[0],': Period ',crs[5]

        print '\nPlease select which course to take attendance.'
        course_id = int(raw_input('Course ID: '))
        print '\n'

        # Prepare the attendance codes

        aCode = ct.execute('SELECT * FROM attendanceCode ');
        codes={}
        for row in aCode:
            codes[row[2].upper()] = row[0]

        # Now, list the students and allow user to choose record to update

        classList = ct.execute('''
            SELECT * FROM enroll as e
                JOIN student as s ON e.student_id=s.id
                WHERE e.course_id=? ''',(course_id,));

        os.system('clear')  # Clear the screen before listing students
        print '\n\nPlease select the student you wish to update:\n'
        pupilList={}
        for pupil in classList:
            print pupil[0],': ',pupil[21],' ',pupil[22]
            pupilList[pupil[0]]=(pupil[21],pupil[22])

        # Choose student record to update
        pupilSelect = int(raw_input('\nStudent ID selection? (Enter to cancel): '))
        print pupilSelect,pupilList.keys()
        if pupilSelect=='':
            return  # Cancel the update if no entry
        elif pupilSelect not in  pupilList.keys():  # reset if no student on list
            raw_input('\n\nNo such student exists in this class.')
            os.system('clear')
            attendance()
        else:
            enroll_id = pupilSelect  # Found student record to update

            print '\nPlease enter the new attandance code for: '
            print pupilList[pupilSelect],' on ',dateNow
            updateCode = raw_input('\nCode? ')
            updateCode = updateCode.upper()

            timeSignedIn = ''
            timeSignedOut = ''

            if updateCode=='UT':
                timeSignedIn = raw_input('\nTime in (24hr HH:MM): ')
            elif updateCode=='SO':
                timeSignedOut = raw_input('\nTime out (24hr HH:MM): ')
            else:
                print '\n'

            ct.execute('''
                INSERT OR REPLACE INTO rollCall(attendanceDate_id,enroll_id,attendanceCode_id,timeIn,timeOut)
                VALUES (?,?,?,?,?)
                ''',(attendanceDate_id, enroll_id, codes[updateCode],timeSignedIn,timeSignedOut));
            conn.commit()

    else:
        "Bad input"
        raw_input('Please enter Y, N or U.  Press any key to continue')
        os.system('clear')
        attendance()
    raw_input('Hit any key to continue')
    os.system('clear')

# Now, update the tardy and absent choiceStudents
# Need to iterate through currently enrolled students and store their enroll_ids
#Then run the following for each of the attendance codes
#Then total up the UA and EA, and UT and write to the enroll table
    print 'Updating absent and tardy totals...'
    # Grab the enroll_id of current enrollment
    currentEnroll = ct.execute("""
        SELECT * FROM enroll as e JOIN course as c ON e.course_id=c.id
        WHERE semester_id = (?)""", (semester_id,) );
    enrollID=[]
    for row in currentEnroll:
        enrollID.append(row[0])

    for item in enrollID:
        print 'I am about to calculate the totals.'
        ct.execute('''
            SELECT count(attendanceCode_id)
            FROM rollCall
            WHERE (attendanceCode_id=1 AND enroll_id=?)''', (item,));
        totalsEA=ct.fetchone()[0]
        ct.execute('''
            SELECT count(attendanceCode_id)
            FROM rollCall
            WHERE (attendanceCode_id=3 AND enroll_id=?)''', (item,));
        totalsUA=ct.fetchone()[0]
        ct.execute('''
            SELECT count(attendanceCode_id)
            FROM rollCall
            WHERE (attendanceCode_id=4 AND enroll_id=?)''', (item,));
        totalsUT=ct.fetchone()[0]
        ct.execute('''
            SELECT count(attendanceCode_id)
            FROM rollCall
            WHERE (attendanceCode_id=7 AND enroll_id=?)''', (item,));
        totalsSO=ct.fetchone()[0]

        totalAbsents = totalsEA + totalsUA + totalsSO
        totalTardies = totalsUT

        # Now update the enroll table with student totalsSO
        ct.execute('''
            UPDATE enroll
            SET absentTotal=?, tardyTotal=?
            WHERE id=?''', (totalAbsents,totalTardies,item));

    conn.commit()
    ct.close()
    conn.close()
