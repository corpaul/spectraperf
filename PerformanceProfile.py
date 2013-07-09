'''
Created on Jul 4, 2013

@author: corpaul
'''
import csv
from decimal import Decimal
from scipy.stats import wilcoxon

class Profile(object):
    '''
    classdocs
    '''


    def __init__(self, rev=0, tc=""):
        '''
        Constructor
        '''
        self.revision = rev
        self.testCase = tc
        # contains MonitoredSession objects
        self.runs = []
        # contains MonitoredStackRange objects
        self.ranges = {}
        
    def addSession(self, s):
        self.runs.append(s)
        for st in s.stacktraces:
            self.addToRange(st.stacktrace, st.rawBytes)
            
            
    def addToRange(self, st, value):
        if st not in self.ranges:
            self.ranges[st] = MonitoredStacktraceRange(st)
        r = self.ranges.get(st)
        r.addToRange(value)
        
            
    def getRange(self, st):
        return self.ranges.get(st)
    
    def __str__(self):
        s = "[Profile: revision: " + str(self.revision) + ", test case: " + self.testCase \
            + ", # runs: " + str(len(self.runs))
        for r in self.ranges.itervalues():
            s += str(r) + "\n"
        return s + "]"
         
            
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
        return "[MonitoredStacktrace: " + str(self.stacktrace) + ", rawBytes: " + str(self.rawBytes) + \
            ", percentage:" + str(self.percentage) + "]"


class MonitoredStacktraceRange(object):
    '''
    classdocs
    '''

    def __init__(self, st):
        '''
        Constructor
        '''
        self.stacktrace = st
        self.minValue = None
        self.maxValue = None
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
        return "[MonitoredStacktraceRange: (min: " + str(self.minValue) + ", max: " + str(self.maxValue) + ") " \
            + str(self.stacktrace) + "]"

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
        result = "[MonitoredSession: " + self.name + ": "
        for st in self.stacktraces:
            result += str(st) + "\n"
        result += "]"
        return result

    def loadSession(self):
        assert self.filename != ""
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
            
            
# session1 = MonitoredSession("Csv1", "csv/SummaryPerStacktrace_1.csv")
# session2 = MonitoredSession("Csv2", "csv/SummaryPerStacktrace_2.csv")
# session1.loadSession()
# session2.loadSession()

# session1.compareSessions(session2)
         
