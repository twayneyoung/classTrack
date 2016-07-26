def restroom():

    #print 'made it to restroom'
    import csv
    import os
    import sqlite3
    import datetime
    import time

    os.system('clear')

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

    # Now locate the current course that is in session at this time
    courses = ct.execute('''
                            SELECT * FROM course JOIN period
                            ON course.period_id=period.id
                            WHERE semester_id=?
                            ''',(semester_id,));

    chkit = 'stay'
    course_id = -1


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
    except:
        print 'Error occured locating course in session'
        chkit = 'end'

    if course_id == -1:
        chkit = 'end'
        print 'No course is currently in session.'

    while len(chkit)>3:
        os.system('clear')

        # Now grab the student roster for the current course_id

        students = ct.execute('''
            SELECT e.id, s.nameLast, s.nameFirst,e.rrPasses
            FROM enroll as e AND student as s
            ON e.student_id = s.id
            WHERE e.course_id=? ''',(course_id,));
        passes = {}
        enrollees = []
        for pupil in students:
            print pupil[0],': ',pupil[1],', ',pupil[2],' -- Passes Remaining -- ',pupil[3]
            passes[pupil[0]] = pupil[3]
            enrollees.append(pupil[0])

        enroll_id = raw_input('\n\nSend which student to the restroom? ')

        try:
            print '\nStudent selected: ',enrollees[enroll_id]
            print '\n'
            if (len(enroll_id)>0 and passes[enroll_id]>0):
                # Grab the time sent as timeOut
                timeOut = datetime.datetime.now()
                timeOut_ts = time.mktime(timeOut.timetuple())

                #**** Add code to check time and remind with a beep every minute
                print '\nSTUDENT LEFT CLASS at: ',timeOut
                raw_input('STUDENT RETURNED?  Hit any key to continue')

                # Grab the time returned as timeIn
                timeIn = datetime.datetime.now()
                timeIn_ts = time.mktime(timeIn.timetuple())

                deltaTime = timeIn_ts - timeOut_ts
                minutesTotal = int(deltaTime/60.)

                # Now update the rrTrips table

                ct.execute('''
                    INSERT INTO rrTrips(attendanceDate_id,enroll_id,timeOut,timeIn,rrBreakTotal)
                    VALUES (?,?,?,?,?) ''',(attendanceDate_id,enroll_id,timeOut,timeIn,minutesTotal));
                conn.commit()

                #  Now need to update the enroll.rrPasses total in enroll and grab a new
                # roster list

                passes[enroll_id] -= 1
                ct.execute('''
                    UPDATE enroll as e
                    SET e.rrPasses = ?
                    WHERE e.id = ? ''', ( passes[enroll_id], enroll_id ) );
                conn.commit()

            else:
                    print '\n*** This student has no bathroom passes remaining. ***'
                    chkit = 'end'
        except:
                'The student you entered is not in our records. Please try again.'
                chkit = 'stay'


    raw_input('Hit any key to Return to Main Menu.')
    os.system('clear')
    conn.commit()
    ct.close()
    conn.close()
