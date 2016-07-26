def setup():
    print 'made it to setup'

    import csv
    import os
    import sqlite3

    # Open the classTrack database
    conn = sqlite3.connect('classTrack-DB')
    ct = conn.cursor()

    os.system('clear')
    print "made it to ctStudents";
    raw_input('Hit any key to continue')
    os.system('clear')

    conn.commit()
    ct.close()
    conn.close()
