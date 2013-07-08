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
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()