-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2016-06-02 15:46:43.196

-- tables
-- Table: assignType
CREATE TABLE assignType (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    weight text NOT NULL
);

-- Table: assignment
CREATE TABLE assignment (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    quarter_id integer NOT NULL,
    course_id integer NOT NULL,
    assignType_id integer NOT NULL,
    name text NOT NULL,
    CONSTRAINT assignment_assignType FOREIGN KEY (assignType_id)
    REFERENCES assignType (id),
    CONSTRAINT assignment_quarter FOREIGN KEY (quarter_id)
    REFERENCES quarter (id),
    CONSTRAINT assignment_course FOREIGN KEY (course_id)
    REFERENCES course (id)
);

-- Table: attendanceCode
CREATE TABLE attendanceCode (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    nameShort text NOT NULL,
    CONSTRAINT AK_9 UNIQUE (id)
);

-- Table: attendanceDate
CREATE TABLE attendanceDate (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    day text,
    daysPast integer,
    daysRemain integer,
    CONSTRAINT AK_8 UNIQUE (id)
);

-- Table: classIncident
CREATE TABLE classIncident (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    attendanceDate_id integer NOT NULL,
    enroll_id integer NOT NULL,
    typeIncident_id integer NOT NULL,
    comment text NOT NULL,
    CONSTRAINT classIncident_attendanceDate FOREIGN KEY (attendanceDate_id)
    REFERENCES attendanceDate (id),
    CONSTRAINT classIncident_enroll FOREIGN KEY (enroll_id)
    REFERENCES enroll (id),
    CONSTRAINT classIncident_typeIncident FOREIGN KEY (typeIncident_id)
    REFERENCES typeIncident (id)
);

-- Table: clubs
CREATE TABLE clubs (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    sponsor text NOT NULL
);

-- Table: course
CREATE TABLE course (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    semester_id integer NOT NULL,
    maths_id integer NOT NULL,
    period_id integer NOT NULL,
    CONSTRAINT course_semester FOREIGN KEY (semester_id)
    REFERENCES semester (id),
    CONSTRAINT course_maths FOREIGN KEY (maths_id)
    REFERENCES maths (id),
    CONSTRAINT course_period FOREIGN KEY (period_id)
    REFERENCES period (id)
);

-- Table: enroll
CREATE TABLE enroll (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    course_id integer NOT NULL,
    student_id integer NOT NULL,
    seatNumber integer NOT NULL,
    calcNumber integer NOT NULL,
    bookNumber integer NOT NULL,
    rrPasses integer NOT NULL,
    absentTotal integer NOT NULL,
    tardyTotal integer NOT NULL,
    gradeQ1 integer NOT NULL,
    gradeQ2 integer NOT NULL,
    gradeExam integer NOT NULL,
    gradeFinal integer NOT NULL,
    incidentsTotal integer NOT NULL,
    contactsTotal integer NOT NULL,
    absentContact text NOT NULL,
    tardyStudentConference text NOT NULL,
    tardyParentContact text NOT NULL,
    tardyParentConference text NOT NULL,
    CONSTRAINT enroll_course FOREIGN KEY (course_id)
    REFERENCES course (id),
    CONSTRAINT enroll_student FOREIGN KEY (student_id)
    REFERENCES student (id)
);

-- Table: father
CREATE TABLE father (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    student_id integer NOT NULL,
    nameLast text,
    nameFirst text,
    emailWork text,
    emailHome text,
    phoneHome text,
    phoneMobile text,
    phoneWork text,
    CONSTRAINT AK_5 UNIQUE (id),
    CONSTRAINT father_student FOREIGN KEY (student_id)
    REFERENCES student (id)
);

-- Table: grades
CREATE TABLE grades (
    assignment_id integer NOT NULL,
    attendanceDate_id integer NOT NULL,
    enroll_id integer NOT NULL,
    grade integer NOT NULL,
    PRIMARY KEY (assignment_id,attendanceDate_id,enroll_id),
    CONSTRAINT grades_assignment FOREIGN KEY (assignment_id)
    REFERENCES assignment (id),
    CONSTRAINT grades_attendanceDate FOREIGN KEY (attendanceDate_id)
    REFERENCES attendanceDate (id),
    CONSTRAINT grades_enroll FOREIGN KEY (enroll_id)
    REFERENCES enroll (id)
);

-- Table: incidentTotals
CREATE TABLE incidentTotals (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    enroll_id integer NOT NULL,
    typeIncident_id integer NOT NULL,
    counts integer NOT NULL,
    CONSTRAINT incidentTotals_typeIncident FOREIGN KEY (typeIncident_id)
    REFERENCES typeIncident (id),
    CONSTRAINT incidentTotals_enroll FOREIGN KEY (enroll_id)
    REFERENCES enroll (id)
);

-- Table: maths
CREATE TABLE maths (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    CONSTRAINT AK_6 UNIQUE (id),
    CONSTRAINT AK_7 UNIQUE (name)
);

-- Table: memberClubs
CREATE TABLE memberClubs (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    student_id integer NOT NULL,
    clubs_id integer NOT NULL,
    office text,
    CONSTRAINT member_student FOREIGN KEY (student_id)
    REFERENCES student (id),
    CONSTRAINT member_clubs FOREIGN KEY (clubs_id)
    REFERENCES clubs (id)
);

-- Table: memberSports
CREATE TABLE memberSports (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    student_id integer NOT NULL,
    sports_id integer NOT NULL,
    number integer,
    position text,
    CONSTRAINT memberSports_student FOREIGN KEY (student_id)
    REFERENCES student (id),
    CONSTRAINT memberSports_sports FOREIGN KEY (sports_id)
    REFERENCES sports (id)
);

-- Table: mother
CREATE TABLE mother (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    student_id integer NOT NULL,
    nameLast text,
    nameFirst text,
    emailWork text,
    emailHome text,
    phoneHome text,
    phoneMobile text,
    phoneWork text,
    CONSTRAINT AK_4 UNIQUE (id),
    CONSTRAINT mother_student FOREIGN KEY (student_id)
    REFERENCES student (id)
);

-- Table: parentContacts
CREATE TABLE parentContacts (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    enroll_id integer NOT NULL,
    typecontact_id integer NOT NULL,
    dateSubmitted text NOT NULL,
    nameContacted text NOT NULL,
    reason text NOT NULL,
    actionNeeded text NOT NULL,
    dateCompleted text,
    CONSTRAINT parentContacts_enroll FOREIGN KEY (enroll_id)
    REFERENCES enroll (id),
    CONSTRAINT parentContacts_typecontact FOREIGN KEY (typecontact_id)
    REFERENCES typecontact (id)
);

-- Table: period
CREATE TABLE period (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL
);

-- Table: quarter
CREATE TABLE quarter (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL
);

-- Table: referral
CREATE TABLE referral (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    enroll_id integer NOT NULL,
    dateOf text NOT NULL,
    reason text NOT NULL,
    dateSubmitted text NOT NULL,
    dateCompleted text NOT NULL,
    action text NOT NULL,
    CONSTRAINT AK_3 UNIQUE (id),
    CONSTRAINT referral_enroll FOREIGN KEY (enroll_id)
    REFERENCES enroll (id)
);

-- Table: rollCall
CREATE TABLE rollCall (
    id integer NOT NULL PRIMARY KEY,
    attendanceDate_id integer NOT NULL,
    enroll_id integer NOT NULL,
    attendanceCode_id integer NOT NULL,
    CONSTRAINT rollCall_attendanceDate FOREIGN KEY (attendanceDate_id)
    REFERENCES attendanceDate (id),
    CONSTRAINT rollCall_enroll FOREIGN KEY (enroll_id)
    REFERENCES enroll (id),
    CONSTRAINT rollCall_attendanceCode FOREIGN KEY (attendanceCode_id)
    REFERENCES attendanceCode (id)
);

-- Table: rrtrips
CREATE TABLE rrTrips (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    attendanceDate_id integer NOT NULL,
    enroll_id integer NOT NULL,
    timeOut text NOT NULL,
    timeIn text,
    CONSTRAINT rrtrips_attendanceDate FOREIGN KEY (attendanceDate_id)
    REFERENCES attendanceDate (id),
    CONSTRAINT rrtrips_enroll FOREIGN KEY (enroll_id)
    REFERENCES enroll (id)
);

-- Table: semester
CREATE TABLE semester (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    year integer NOT NULL,
    CONSTRAINT AK_2 UNIQUE (id)
);

-- Table: sports
CREATE TABLE sports (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    coach text
);

-- Table: student
CREATE TABLE student (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    schoolID integer NOT NULL,
    nameLast text NOT NULL,
    nameFirst text NOT NULL,
    nameMI text,
    email text,
    gradelevel integer NOT NULL,
    birthday text NOT NULL,
    gender text NOT NULL,
    ethnic text,
    goalCollegeCareer text,
    CONSTRAINT AK_1 UNIQUE (id)
);

-- Table: typeIncident
CREATE TABLE typeIncident (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL
);

-- Table: typecontact
CREATE TABLE typecontact (
    id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    CONSTRAINT AK_0 UNIQUE (id)
);

-- End of file.
