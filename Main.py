'''
Created on Jul 8, 2013

@author: corpaul
'''
from PerformanceProfile import *

s1 = MonitoredSession("nt_magnetlink1", "csv/nosetests_test_magnetlink1.csv")
s2 = MonitoredSession("nt_magnetlink2", "csv/nosetests_test_magnetlink2.csv")
s3 = MonitoredSession("nt_magnetlink3", "csv/nosetests_test_magnetlink3.csv")
s4 = MonitoredSession("nt_magnetlink4", "csv/nosetests_test_magnetlink4.csv")
s5 = MonitoredSession("nt_magnetlink5", "csv/nosetests_test_magnetlink5.csv")

s6 = MonitoredSession("nt_magnetlink6", "csv/nosetests_test_magnetlink6.csv")


profile = Profile(1, "nosetests_test_magnetlink")
profile.addSession(s1)
profile.addSession(s2)
profile.addSession(s3)
profile.addSession(s4)
profile.addSession(s5)



print str(profile)

fits = profile.fitsProfile(s6)
print fits


profile.similarity(fits)

