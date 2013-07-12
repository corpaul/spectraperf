'''
Created on Jul 4, 2013

@author: corpaul
'''
import unittest
from PerformanceProfile import *
import DatabaseHelper

DATABASE = "/home/corpaul/workspace/spectraperf/performance_test.db"

class TestPerformanceFunctions(unittest.TestCase):



    def testAddToRange(self):
        s = MonitoredStacktrace("test", 10, 25)

        sess = MonitoredSession()
        sess.addStacktrace(s)

        p = Profile("24435a", "test_batch")
        p.addSession(sess)

        self.assertEqual(p.getRange("test").minValue, 10)
        self.assertEqual(p.getRange("test").maxValue, 10)

        p.addToRange("test", 20)
        self.assertEqual(p.getRange("test").minValue, 10)
        self.assertEqual(p.getRange("test").maxValue, 20)

        p.addToRange("test", 5)
        self.assertEqual(p.getRange("test").minValue, 5)
        self.assertEqual(p.getRange("test").maxValue, 20)

        p.addToRange("test", 15)
        self.assertEqual(p.getRange("test").minValue, 5)
        self.assertEqual(p.getRange("test").maxValue, 20)

    def testIsInRange(self):
        st1 = MonitoredStacktrace("test", 10, 25)
        st2 = MonitoredStacktrace("test", 20, 25)


        sess1 = MonitoredSession()
        sess1.addStacktrace(st1)
        sess2 = MonitoredSession()
        sess2.addStacktrace(st2)

        p = Profile("24435a", "test_batch")
        p.addSession(sess1)
        p.addSession(sess2)

        self.assertTrue(p.getRange(st1.stacktrace) == p.getRange(st2.stacktrace))

        self.assertTrue(p.getRange(st1.stacktrace).isInRange(15))
        self.assertTrue(p.getRange(st1.stacktrace).isInRange(10))
        self.assertFalse(p.getRange(st1.stacktrace).isInRange(9))
        self.assertFalse(p.getRange(st1.stacktrace).isInRange(21))

    def testFitsProfile(self):
        s1 = MonitoredStacktrace("test1", 10, 25)
        s2 = MonitoredStacktrace("test2", 25, 25)

        sess1 = MonitoredSession()
        sess1.addStacktrace(s1)



        p = Profile("24435a", "test_batch")
        p.addToRange("test1", 10)
        p.addToRange("test1", 20)


        #p.addToRange("test2", 10)
        #p.addToRange("test2", 20)


        fits = p.fitsProfile(sess1)
        self.assertEqual(fits["test1"], 1)

        sess1.addStacktrace(s2)
        # should raise AssertionError because we did not add a range for test2 yet
       # with self.assertRaises(AssertionError):
       #     fits = p.fitsProfile(sess1)

        p.addToRange("test2", 10)
        p.addToRange("test2", 20)
        fits = p.fitsProfile(sess1)


        self.assertEqual(fits["test1"], 1)
        self.assertEqual(fits["test2"], 0)

        p2 = Profile("24435a", "test_batch")
        p2.addToRange("test2", 10)
        p2.addToRange("test2", 20)
        sess2 = MonitoredSession()
        sess2.addStacktrace(s2)
        fits = p2.fitsProfile(sess2)
        self.assertEqual(fits["test2"], 0)

    def testSimilarity(self):
        v1 = {"test1" : 1, "test2" : 1, "test3" : 1, "test4" : 1, "test5" : 0}
        v2 = {"test1" : 1, "test2" : 1, "test3" : 1, "test4" : 1, "test5" : 1}
        p = Profile("24435a", "test_batch")
        self.assertAlmostEqual(p.similarity(v2), 1)
        self.assertAlmostEqual(p.similarity(v1), 0.894427191)

    def testProfileHelper(self):
        # reset database before testing
        i = DatabaseHelper.InitDatabase(DATABASE)

        s1 = MonitoredStacktrace("test1", 10, 25)
        s2 = MonitoredStacktrace("test2", 25, 25)

        sess1 = MonitoredSession()
        sess1.addStacktrace(s1)
        sess1.addStacktrace(s2)

        p = Profile("24435a", "test_batch", DATABASE)

        h = ProfileHelper(DATABASE)

        # empty profile
        self.assertEqual(h.getDatabaseId(p), -1)
        h.storeInDatabase(p)

        self.assertNotEqual(h.getDatabaseId(p), -1)

        p.addSession(sess1)
        h.storeInDatabase(p)

        h.loadFromDatabase("24435a", "test_batch")





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()