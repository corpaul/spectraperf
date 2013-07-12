'''
Created on Jul 4, 2013

@author: corpaul
'''
import csv
from decimal import Decimal
from math import sqrt
import sqlite3




class Profile(object):
    '''
    classdocs
    '''

    def __init__(self, rev, tc, DATABASE = "/home/corpaul/workspace/spectraperf/performance.db"):
        '''
        Constructor
        '''
        self.revision = rev
        self.testCase = tc
        # contains MonitoredSession objects
        # sink? we will only use the ranges
        self.runs = []
        # contains MonitoredStackRange objects
        self.ranges = {}
        self.databaseId = -1
        self.DATABASE = DATABASE
#        self.helper = ProfileHelper(DATABASE)

    def addSession(self, s):
        '''
        Add session s to the profile. Update ranges for all
        stacktraces in s.
        '''
        self.runs.append(s)
        for st in s.stacktraces:
            self.addToRange(st.stacktrace, st.rawBytes)

    def addToRange(self, st, value):
        '''
        Find the range for stacktrace st and add value to it,
        i.e. extend the range if necessary.
        '''
        if st not in self.ranges:
            self.ranges[st] = MonitoredStacktraceRange(st, self.DATABASE)
        r = self.ranges.get(st)
        r.addToRange(value)

    def isInRange(self, st, value):
        '''
        Returns true iff value is in the range of stacktrace st.
        '''
        assert self.getRange(st) != None, "No range set for %s" % st
        return self.getRange(st).isInRange(value)

    def getRange(self, st):
        return self.ranges.get(st)

    def fitsProfile(self, s):
        '''
        Returns a dict containing 1's and 0's representing whether
        the value for that stacktrace is in the range of the stacktrace
        in this profile.
        '''
        fits = {}
        for st in s.stacktraces:
            f = 1 if self.getRange(st.stacktrace) != None and self.isInRange(st.stacktrace, st.rawBytes) else 0
            fits[st.stacktrace] = f
        return fits


    def similarity(self, v):
        '''
        Returns the (simplified) cosine similarity for fit vector v
        and a vector with the same total number of items, all initialized to 1's.

        The rationale behind this is that we want to see how different the fit vector
        is compared to the profile (which is the fit vector with all 1's).

        A similarity of 1 means all elements are equal, hence all elements of the new vector
        fit in the ranges defined in the profile.

        A similarity of 0 means all elements are different, hence no elements fit in the defined
        ranges.

        A value between 0 and 1 means the vectors are partly different.
        '''
        d1 = sqrt(len(v))
        ones = 0
        for i in v.itervalues():
            ones += i
        d2 = sqrt(ones)
        sim = ones / (d1*d2)
        return sim

    def __str__(self):
        s = "[Profile: revision: %s, test case: %s, # runs: %d" \
            %(self.revision, self.testCase, len(self.runs))

        for r in self.ranges.itervalues():
            s += "%s\n" % r
        return "%s]" % s

class ProfileHelper(object):

    def __init__(self, DATABASE = "/home/corpaul/workspace/spectraperf/performance.db"):
        self.DATABASE = DATABASE
        self.con = sqlite3.connect(self.DATABASE)
        self.con.row_factory = sqlite3.Row


    def getDatabaseId(self, p):
        if p.databaseId != -1:
            return p.databaseId

        with self.con:
            cur = self.con.cursor()
            sqlCheck = "SELECT id FROM profile WHERE revision = '%s' AND testcase = '%s'" \
                % (p.revision, p.testCase)
            cur.execute(sqlCheck)
            rows = cur.fetchall()
            if len(rows) == 1:
                self.databaseId = rows[0][0]
                return rows[0][0]
            else:
                return -1

    def storeInDatabase(self, p):
        with self.con:
            cur = self.con.cursor()

            if p.databaseId == -1:
                # insert profile
                sqlProfile = "INSERT INTO profile (revision, testcase) VALUES ('%s', '%s')" \
                    % (p.revision, p.testCase)
                cur.execute(sqlProfile)
                p.databaseId = cur.lastrowid

            # insert ranges
            for st in p.ranges.itervalues():
                if st.getDatabaseId() == -1:
                    sqlStacktrace = "INSERT INTO stacktrace (stacktrace) VALUES ('%s')" \
                        % (st.stacktrace)
                    cur.execute(sqlStacktrace)
                    st.databaseId = cur.lastrowid

                sqlRange = "INSERT INTO range (stacktrace_id, min_value, max_value, profile_id, type_id) VALUES \
                    (%d, %d, %d, %d, %d) " \
                    % (st.databaseId, st.minValue, st.maxValue, p.databaseId, 1)
                cur.execute(sqlRange)

            self.con.commit()

    def loadFromDatabase(self, rev, tc):
        with self.con:
            cur = self.con.cursor()
            sql = "SELECT id FROM profile WHERE revision = '%s' AND testcase = '%s'" \
                % ( rev, tc )
            cur.execute(sql)
            rows = cur.fetchall()
            assert len(rows) > 0, "profile does not exist"

            p = Profile(rev, tc)
            p.databaseId = rows[0]['id']
            print p

            # TODO: read ranges

            # TODO: add ID to stackranges etc?







#
           #         JOIN range ON range.profile_id = profile.id \
          #          JOIN stacktrace ON stacktrace.id = range.stacktrace_id \
          #          JOIN type ON type_id = range.type_id"



class MonitoredStacktrace(object):
    '''
    classdocs
    '''

    def __init__(self, st, raw, perc):
        '''
        Constructor
        '''
        self.stacktrace = st
        self.rawBytes = raw
        self.percentage = perc

    def __str__(self):
        return "[MonitoredStacktrace: %s, rawBytes: %d, percentage: %d]" \
            %(self.stacktrace, self.rawBytes, self.percentage)


class MonitoredStacktraceRange(object):
    '''
    classdocs
    '''

    def __init__(self, st, DATABASE = "/home/corpaul/workspace/spectraperf/performance.db"):
        '''
        Constructor
        '''
        self.stacktrace = st
        self.minValue = None
        self.maxValue = None
        self.databaseId = -1
        self.DATABASE = DATABASE
       # self.mean = None
       # self.stdev = None

    def addToRange(self, i):
        '''
        Add i to the range, extend the range if necessary.
        '''
        if (self.minValue == None) or (i < self.minValue):
            self.minValue = i
        if (self.maxValue == None) or (i > self.maxValue):
            self.maxValue = i

    def isInRange(self, value):
        return value >= self.minValue and value <= self.maxValue

    def __str__(self):
        return "[MonitoredStacktraceRange: (min: %d, max: %d) %s]" \
            %(self.minValue, self.maxValue, self.stacktrace)

    def getDatabaseId(self):
        if self.databaseId != -1:
            return self.databaseId

        self.con = sqlite3.connect(self.DATABASE)
        with self.con:
            cur = self.con.cursor()
            sqlCheck = "SELECT id FROM stacktrace WHERE stacktrace = '%s'" \
                % self.stacktrace
            cur.execute(sqlCheck)
            rows = cur.fetchall()
            if len(rows) == 1:
                return rows[0][0]
            else:
                return -1

class MonitoredSession(object):
    '''
    classdocs
    '''
    def __init__(self, name="", filename=""):
        '''
        Constructor
        '''
        self.name = name
        self.filename = filename
        self.stacktraces = []
        self.lookupDict = {}
        if filename != "":
            self.loadSession()

    def __str__(self):
        result = "[MonitoredSession: %s: " % self.name
        for st in self.stacktraces:
            result += "%s\n" % st
        return "%s]" % result

    def loadSession(self):
        assert self.filename != "", "Filename not set for session"
        # read CSV
        with open(self.filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for line in reader:
                st = line['TRACE']
                b = Decimal(line['BYTES'])
                # perc = Decimal(line['PERC'])
                # note: perc is unused at the moment
                record = MonitoredStacktrace(st, b, 0)
                self.stacktraces.append(record)
                self.lookupDict[st] = record

    def addStacktrace(self, st):
        self.stacktraces.append(st)


'''
    unused, didn't make sense :)
    def compareSessions(self, s2):
        # get union of session entries and initialize to 0
        # note: we do not take thread id into account at the moment!!
        compared = {}
        print "size self: " + str(len(self.stacktraces))
        for st in self.stacktraces:
            compared[st.stacktrace] = {}
            compared[st.stacktrace]['s1'] = st.rawBytes

        print "size compared after s1: " + str(len(compared))

        for st in s2.stacktraces:
            if not st.stacktrace in compared:
                compared[st.stacktrace] = {}
            compared[st.stacktrace]['s2'] = st.rawBytes

        for st in compared:
            if not 's1' in  compared[st]:
                compared[st]['s1'] = 0
            if not 's2' in  compared[st]:
                compared[st]['s2'] = 0

        print "size compared after s2: " + str(len(compared))
        # print str(compared)
        # calculate difference
        for st in compared:
            diff = compared[st]['s2'] - compared[st]['s1']
            print str(diff) + " (" + st + ")"
'''

# session1 = MonitoredSession("Csv1", "csv/SummaryPerStacktrace_1.csv")
# session2 = MonitoredSession("Csv2", "csv/SummaryPerStacktrace_2.csv")
# session1.loadSession()
# session2.loadSession()

# session1.compareSessions(session2)

