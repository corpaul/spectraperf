'''
Created on Jul 4, 2013

@author: corpaul
'''
import unittest
from PerformanceProfile import * 


class Test(unittest.TestCase):


    def testName(self):
        pass

    def testAddToRange(self):
        s = MonitoredStacktrace("test", 10, 25)
        
        sess = MonitoredSession()
        sess.addStacktrace(s)
        
        p = Profile()
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
        
        p = Profile()
        p.addSession(sess1)
        p.addSession(sess2)
        
        self.assertTrue(p.getRange(st1.stacktrace) == p.getRange(st2.stacktrace))
        
        self.assertTrue(p.getRange(st1.stacktrace).isInRange(15))
        self.assertTrue(p.getRange(st1.stacktrace).isInRange(10))
        self.assertFalse(p.getRange(st1.stacktrace).isInRange(9))
        self.assertFalse(p.getRange(st1.stacktrace).isInRange(21))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()