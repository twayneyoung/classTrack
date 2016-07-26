def enrollment():
    print 'made it to enrollment'

    import csv
    import os
    import sqlite3

    # Open the classTrack database
    conn = sqlite3.connect('classTrack-DB.sqlite')
    ct = conn.cursor()

    os.system('clear')
    print "made it to ctStudents"

#------------------------------------------------------------------------------

    print 'Please choose how you wish to update your enrollment: \n\n'

    print 'A: Remove a student from enrollment'
    print 'B: Add a student to enrollment'
    print 'C: Move a student to a new class period'
    print 'D: Import Student Info Forms \n\n'

    choice = raw_input('Selection? ')
    if choice == '':  # Cancel
        print''
    elif choice.upper() == 'A': # Remove a student from enrollment
        studentSchoolID=raw_input("\nEnter student's school issued ID number: ")
        try:
            ct.execute('''SELECT * FROM enroll as e JOIN student as s
                ON e.student_id=s.id
                WHERE schoolID=?''',(studentSchoolID,));
            studentFound = ct.fetchone()
            verifyRemove = raw_input('Remove '+studentFound[21]+' '+studentFound[22]+' from enrollment? (Y/N)')
            if verifyRemove.upper() == 'Y':
                print 'Removing student...'
                ct.execute('''UPDATE enroll SET course_id=-1
                    WHERE id=?''', (studentFound[0],));
            elif verifyRemove.upper() == 'N':
                print 'This student has not been removed.'
                raw_input('Hit any key to continue.')
                os.system('clear')
            else:
                print 'Please enter Y or N to verify.'
                raw_input('Press any key to continue.')
                os.system('clear')
                enrollment()
        except:
            print '\nStudent '+studentSchoolID+' not found in database.'
            raw_input('Please verify the school ID number and try again.')
            os.system('clear')
            enrollment()


    elif choice.upper() == 'B': # Add a student to enrollment
        os.system('clear')
        print 'Please enter the following information to enroll a student:\n\n'

        nameFull = raw_input('\nStudent [Last Name],[First Name]: ')
        nameSplit       = nameFull.split(',')
        nameLast        = nameSplit[0].strip()
        nameFirst       = nameSplit[1].strip()
        schoolID        = int(raw_input('School issued student ID number: '))
        birthday        = raw_input('Student birthday: ')
        gender          = raw_input('Gender: (M/F): ').upper()
        gradeLevel      = int(raw_input('GradeLevel [9-12]: '))
        nameMother      = raw_input('Name of Mother: ')
        nameFather      = raw_input('Name of Father: ')
        phoneHome       = raw_input('Home phone xxx-xxx-xxxx : ')
        emailGuardian   = raw_input('Guardian email: ')
        emergencyCon    = raw_input('Emergency Contact: ')

        print '\n\nAdd this student to which course: '
        coursesAvailable = ct.execute('''
            SELECT c.id,c.period_id,m.name FROM course as c JOIN maths as m
            ON c.maths_id=m.id ''');
        courseList = []
        for item in coursesAvailable:
            print item[0],': Period ',item[1],' | ',item[2]
            courseList.append(item[0])
        courseID = int(raw_input('\n\nAdd student to course ID? '))
        course_id = courseID

#*****************************************************
        # Update the student table
        try:
            ct.execute('''
                SELECT id FROM student
                WHERE (schoolID)= ? ''', (schoolID,) );
            student_id = ct.fetchone()[0]
            oldGradeLevel = ct.fetchone()[6]
            if gradeLevel > oldGradeLevel:
                ct.execute('''
                UPDATE student SET gradelevel=gradeLevel
                WHERE (schoolID)= ? ''', (schoolID,) );
            print nameLast + ", " + nameFirst +" record exists."
        except:
            ct.execute("""
            INSERT OR IGNORE INTO student(schoolID, nameLast,
            nameFirst, gradelevel, birthday, gender)
            VALUES (?, ?, ?, ?, ?, ?)""",\
            (schoolID,nameLast,nameFirst,gradeLevel,birthday,\
            gender));
            ct.execute('''
                SELECT id FROM student
                WHERE (schoolID)= ? ''', (schoolID,) );
            student_id = ct.fetchone()[0]
            print nameLast + ", " + nameFirst +" record added."

        # Update the mother table
        ct.execute("""
            INSERT OR REPLACE INTO mother(student_id,nameLast,
            nameFirst,phoneHome)
            VALUES (?,?,?,?)""",
            (student_id, nameLast, nameMother, phoneHome) );
        ct.execute('''
            SELECT id FROM mother
            WHERE
            (student_id)=? AND
            (nameFirst)=? AND
            (phoneHome)=?''',
            (student_id,nameMother,phoneHome) );
        mother_id = ct.fetchone()[0]

        # Update the father table
        ct.execute("""
            INSERT OR REPLACE INTO father(student_id,nameLast,
            nameFirst,phoneHome)
            VALUES (?,?,?,?)""", (student_id, nameLast,
                nameFather, phoneHome) );
        ct.execute('''
            SELECT id FROM father
            WHERE
            (student_id)=? AND
            (nameFirst)=? AND
            (phoneHome)=?''',
            (student_id,nameFather,phoneHome) );
        father_id = ct.fetchone()[0]

        # Update the enroll table
        ct.execute('''SELECT MAX(seatNumber) FROM enroll
            WHERE course_id=? ''', (courseID,));
        seatMax = int(ct.fetchone()[0])
        print seatMax
        seatNum = seatMax + 1
        print seatNum
        calcNum = seatNum
        bookNum = seatNum
        absent = 0
        tardy = 0
        gradeQ1 = 50
        gradeQ2 = 50
        gradeEx = 50
        gradeFinal = 50
        incidents = 0
        contacts = 0
        initNo = 'N'

        try:
            ct.execute('''SELECT id FROM enroll
            WHERE
            (course_id)=? AND
            (student_id)=? AND
            (seatNumber)=?''',
            (course_id,student_id,seatNum) );
            enroll_id = ct.fetchone()[0]
            print "Student already enrolled in this course."
        except:
            ct.execute("""
            INSERT OR IGNORE INTO enroll(course_id,student_id,
            seatNumber,calcNumber,bookNumber,rrPasses,
            absentTotal,tardyTotal,gradeQ1,gradeQ2,gradeExam,
            gradeFinal,incidentsTotal,contactsTotal,
            absentContact,tardyStudentConference,
            tardyParentContact,tardyParentConference)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (course_id,student_id,seatNum,\
            calcNum,bookNum,rrPasses,absent,tardy,gradeQ1,\
            gradeQ2,gradeEx,gradeFinal,incidents,contacts,\
            initNo,initNo,initNo,initNo) );
            ct.execute('''SELECT id FROM enroll
            WHERE
            (course_id)=? AND
            (student_id)=? AND
            (seatNumber)=?''',
            (course_id,student_id,seatNum) );
            enroll_id = ct.fetchone()[0]
            print 'New student enrolled in this course.'
            conn.commit()

#*******************************************************

    elif choice.upper() == 'C': # Move a student to a new class period_id

        studentSchoolID=raw_input("\nEnter student's school issued ID number: ")
        try:
            ct.execute('''SELECT * FROM enroll as e JOIN student as s
                ON e.student_id=s.id
                WHERE schoolID=?''',(studentSchoolID,));
            studentFound = ct.fetchone()
            #print studentFound
            courseID = studentFound[1]
            #print courseID
            if courseID =='-1':
                print '\nStudent not currently enrolled.'
                raw_input('Press any key to continue.')
            else:
                ct.execute('''SELECT c.id,c.period_id,m.name FROM course as c JOIN maths as m
                ON c.maths_id=m.id WHERE c.id=?''',(courseID,));
            courseInfo = ct.fetchone()
            #print courseInfo
            verifyMove = raw_input('\nMove '+studentFound[21]+' '+studentFound[22]\
                +' from: '+str(courseInfo[0])+': Period '+str(courseInfo[1])+' '\
                +courseInfo[2]+'? (Y/N)')

            if verifyMove.upper() == 'Y':
                coursesAvailable = ct.execute('''SELECT c.id,c.period_id,m.name
                    FROM course as c JOIN maths as m
                    ON c.maths_id=m.id WHERE c.id != ? ''',(courseID,));
                courseList = []
                for item in coursesAvailable:
                    print item[0],': Period ',item[1],' | ',item[2]
                    courseList.append(item[0])
                moveTo = int(raw_input('\n\nMove student to course ID? '))

                if moveTo in courseList:
                    print 'Moving student...'
                    ct.execute('''UPDATE enroll SET course_id=?
                        WHERE id=?''', (moveTo,studentFound[0]));
                else:
                    print 'No such course exists.  Please try again.'
                    raw_input('Hit any key to continue.')
                    os.system('clear')
                    enrollment()

            elif verifyMove.upper() == 'N':
                print 'This student has not been moved.'
                raw_input('Hit any key to continue.')
                os.system('clear')
            else:
                print 'Please enter Y or N to verify.'
                raw_input('Press any key to continue.')
                os.system('clear')
                enrollment()
        except:
            print '\nStudent '+studentSchoolID+' not found in database.'
            raw_input('Please verify the school ID number and try again.')
            os.system('clear')
            enrollment()




    elif choice.upper() == 'D': # Import student info Forms
        print 'This option not yet available.'

    elif choice.upper() == '': # Return to main menu
        os.system('clear')
        print '\n'
    else:
        raw_input('Choice invalid. Please try again...Hit any key to continue.')
        os.system('clear')
        enrollment()


#------------------------------------------------------------------------------
    raw_input('Hit any key to continue')
    os.system('clear')

    conn.commit()
    ct.close()
    conn.close()
