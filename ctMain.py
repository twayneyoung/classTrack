#-------------------------------------------------------------------------------
# PROGRAM   ctMain.py
# AUTHOR    T. Wayne Young
# DATE      June 6, 2016
#
# This is the main program for classTrack.  All other modules will be run from
# this program.
#
# FILES:
# classTrack-DB.sqlite --> main SQL database where all data is stored
# classTrackModel_create_proto.sql --> SQL script to create the DB structure
#
#-------------------------------------------------------------------------------
#
# Import modules
#
import ctStudents
import ctAttendance
import ctEnrollment
import ctRestroom
import ctDiscipline
import ctGrades
import ctSetup
import os
#
# Clear the screen before beginning
os.system('clear')
#
# Setup main menu
#
while True:
    print 'classTrack MAIN \n\n'
    print 'Please choose from the following modules:\n'
    print '1. STUDENTS'
    print '2. ATTENDANCE'
    print '3. ENROLLMENT'
    print '4. RESTROOM'
    print '5. DISCIPLINE'
    print '6. GRADES'
    print '7. SETUP'
    choiceMain = raw_input ('\nEnter number of choice: ');

    if choiceMain   == '1':
        ctStudents.students()
    elif choiceMain == '2':
        ctAttendance.attendance()
    elif choiceMain == '3':
        ctEnrollment.enrollment()
    elif choiceMain == '4':
        ctRestroom.restroom()
    elif choiceMain == '5':
        ctDiscipline.discipline()
    elif choiceMain == '6':
        ctGrades.grades()
    elif choiceMain == '7':
        ctSetup.setup()
    else:
        break
    continue












#-------------------------------------------------------------------------------
