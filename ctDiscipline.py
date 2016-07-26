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

    courses = list()
    try:
        for crs in courses:
            print crs
            courses.append(crs[0])
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
        if course_id not in courses:
            print '\nYou have entered an invalid course id. Please try again.\n'
            course_id = -1

    while len(chkit)>3:
        os.system('clear')

        # Now grab the student roster for the current course_id
        students = ct.execute('''
            SELECT e.id, s.nameLast, s.nameFirst
            FROM enroll as e AND student as s
            ON e.student_id = s.id
            WHERE e.course_id=? ''',(course_id,));
        passes = {}
        enrollees = []
        for pupil in students:
            print pupil[0],': ',pupil[1],', ',pupil[2]
            passes[pupil[0]] = pupil[3]
            enrollees.append(pupil[0])

        enroll_id = raw_input('\n\nDiscipline Report for which student? ')

        try:
            print 'You have selected student number: ',enrollees[enroll_id]
        except:
                'The student you entered is not in our records. Please try again.'
                chkit = 'stay'

        raw_input ('Press any key to continue.')
        os.system('clear')

        # Print the students information to date




#----------------------END MODULE-----------------------------------------------
    os.system('clear')
    conn.commit()
    ct.close()
