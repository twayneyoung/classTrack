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
import ctParentContact
import ctGrades
import ctSetup
import ctReports
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
    print '6. PARENT CONTACT'
    print '7. GRADES'
    print '8. SETUP'
    print '9. REPORT'

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
        ctParentContact.parentContact()
    elif choiceMain == '7':
        ctGrades.grades()
    elif choiceMain == '8':
        ctSetup.setup()
    elif choiceMain == '9':
        ctReports.reports()
    else:
        break
    continue












#-------------------------------------------------------------------------------
