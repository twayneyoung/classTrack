def students():

    import csv
    import os
    import sqlite3

    # Open the classTrack database
    conn = sqlite3.connect('classTrack-DB.sqlite')
    ct = conn.cursor()

    #os.system('clear')
    print "made it to ctStudents";

    while True:
        print 'STUDENTS:\n\n'
        print '1. Import New Class'
        print '2. Import Student Info Data'
        print '3. Add a Student to existing Class'
        print '4. Remove a Student from existing Class'
        choiceStudents = raw_input('\nEnter the number of your choice: ')

        if choiceStudents == '1':
            newClassFile = raw_input('''\nEnter the PowerTeacher roster csv
                filename to import: ''')
            if len(newClassFile)==0:
                newClassFile = \
                './classTrack-PowerSchoolData/P1 Student Roster.csv'
            semesterNew = raw_input('\nEnter the semester: ')
            yearNew = raw_input('\nEnter the semster year: ')
            yearNew = int(yearNew)
            dateFirst = raw_input('\nEnter the semester start date: ')
            dateLast = raw_input('\nEnter the semester end date: ')
            periodNew = raw_input('\nEnter the period number: ')
            periodNew = int(periodNew)
            periodStart = raw_input('\nEnter the period start time: ')
            periodEnd = raw_input('\nEnter the period end time: ')
            rrPasses = raw_input('''\nEnter the alotted bathroom passes for the
                entire semester: ''')
            rrPasses = int(rrPasses)

            print semesterNew, yearNew
            rowCount = 0  # Initialize the row count for the csv file
            seatNum = 0 # Initialize the seat number
            # Open and read the Power School csv roster file
            with open(newClassFile, 'rb') as csvfile:
                newClassData = \
                    csv.reader(csvfile, delimiter=',', quotechar='"')

                for row in newClassData:
                    rowCount = rowCount + 1
                    if rowCount == 1:
                        # Update the maths table
                        try:
                            ct.execute('''SELECT id FROM maths
                                          WHERE name = ? ''', (row[0], ));
                            maths_id = ct.fetchone()[0]
                            print row[0] + " record exists."
                        except:
                            ct.execute("""
                                INSERT OR IGNORE INTO maths(name)
                                VALUES ( ? )""", ( row[0], ) );
                            ct.execute('''SELECT id FROM maths
                                          WHERE name = ? ''', (row[0], ));
                            maths_id = ct.fetchone()[0]
                            print row[0] + " record added to maths."


                        # Update the semester table
                        try:
                            ct.execute('''
                                SELECT id
                                FROM semester
                                WHERE (name)= ? AND (year)=?''',
                                (semesterNew,yearNew));
                            semester_id = ct.fetchone()[0]
                            print semesterNew + " " + str(yearNew) +" exists."
                        except:
                            ct.execute('''
                            INSERT OR IGNORE INTO semester(name,year,dateStart,
                                                            dateEnd)
                                VALUES ( ?, ?, ?, ?)''',( semesterNew ,yearNew,
                                        dateFirst, dateLast) );
                            ct.execute('''
                                SELECT id
                                FROM semester
                                WHERE (name)= ? AND (year)=?''',
                                (semesterNew,yearNew));
                            semester_id = ct.fetchone()[0]
                            print semesterNew + " " + str(yearNew) +" added."

                        # Update the period table
                        try:
                            ct.execute('''
                                SELECT id FROM period
                                WHERE (name)= ? ''',(periodNew,));
                            period_id = ct.fetchone()[0]
                            print str(periodNew) + " record exists."
                        except:
                            ct.execute("""
                            INSERT OR IGNORE INTO period(name,starting,ending)
                                VALUES ( ?,?,? )""", ( periodNew, periodStart,\
                                                       periodEnd) );
                            ct.execute('''
                                SELECT id FROM period
                                WHERE (name)= ? ''',(periodNew,));
                            period_id = ct.fetchone()[0]
                            print 'Period ' + str(periodNew) + " record added."

                        # Update the course table
                        try:

                            ct.execute('''
                                SELECT id FROM course
                                WHERE
                                (semester_id)=? AND
                                (maths_id)=? AND
                                (period_id)=?''',
                                (semester_id,maths_id,period_id));
                            course_id = ct.fetchone()[0]
                            print 'Course already exists.'

                        except:

                            ct.execute("""
                            INSERT OR IGNORE INTO course(semester_id,maths_id,
                                period_id)
                                VALUES ( ?, ?, ? )""",
                                ( semester_id, maths_id, period_id ) );
                            ct.execute('''
                                SELECT id FROM course
                                WHERE
                                (semester_id)=? AND
                                (maths_id)=? AND
                                (period_id)=?''',
                                (semester_id,maths_id,period_id));
                            course_id = ct.fetchone()[0]
                            print "Course created."

                        conn.commit()
                        continue

                    elif rowCount == 2:
                        # Skip the row headers
                        # Later, modify this section to sort and determine
                        # the fields and position numbers for each so that
                        # there is no restriction on the order that they
                        # must be placed in when exporting from PowerTeacher
                        continue

                    elif rowCount>2 and row[0] != '':
                        # Pull student data from the current row in csv file
                        print row
                        nameFull        =   row[0]
                        nameSplit       =   nameFull.split(',')
                        nameLast        =   nameSplit[0].strip()
                        nameFirst       =   nameSplit[1].strip()
                        schoolID        =   row[1]
                        birthday        =   row[2]
                        gender          =   row[3]
                        gradeLevel      =   row[4]
                        nameMother      =   row[5]
                        nameFather      =   row[6]
                        phoneHome       =   row[7]
                        emailGuardian   =   row[8]
                        emergencyCon    =   row[9]

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
                        seatNum = seatNum + 1
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
                        continue
                    else:
                        conn.commit()
                        return
            newClassData.close()
        elif choiceStudents == '2':
            continue
        elif choiceStudents == '3':
            continue
        elif choiceStudents == '4':
            # REMOVE a student from a selected class
            os.system('clear')
            print '\nTo remove a student from a class...\n\n'
            print 'Select the class to edit. \n'
            ct.excecute('''
                SELECT course.id,semester.name,semester.year,maths.name,
                       period.name
                FROM course
                INNER JOIN semester ON course.semester_id=semester.id
                INNER JOIN maths ON course.maths_id=maths.id
                INNER JOIN period ON course.period_id=period.id;
            ''')
            choiceClass = raw_input('\nFrom which class do you wish to remove \
                                        the student?')
            os.system('clear')
            print('Class Roster for your selection:\n')
            ct.execute('''
                SELECT enroll.id,student.schoolID,student.nameLast,
                       student.nameFirst
                FROM enroll_id
                INNER JOIN student ON enroll.student_id=student.id;
            ''')
            choiceStudent = raw_input("\nSelect the student's enroll ID to \
                                            remove from this class: ")
            ct.execute('''
                DELETE FROM enroll WHERE id=choiceStudent
            ''');
            continue
        else:
            break

        raw_input('Hit any key to continue')
        os.system('clear')

        conn.commit()
        ct.close()
        conn.close()
        return
