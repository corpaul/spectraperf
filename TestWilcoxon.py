'''
Created on Jul 2, 2013

@author: corpaul
'''
from scipy.stats import wilcoxon

a = list(xrange(5))
b = list(xrange(5))
c = list(a)
b.reverse()
c[0] = c[0]+.1
#c[1] = c[1]-.1
#c[2] = c[2]-.1
#c[3] = c[3]-.1

print "a: "  + str(a)
print "b: "  + str(b)
print "c: "  + str(c)

res = wilcoxon(a,c, "wilcox")
print str(res)
res = wilcoxon(a,b)
print str(res)


        

def cliffsDelta(a, b):
    larger = 0
    smaller = 0
    for i in range(0, len(a)):
        if(a[i] > b[i]):
            larger = larger + 1
        if(a[i] < b[i]):
            smaller = smaller + 1
    
    print "larger: " + str(larger)
    print "smaller: " + str(smaller)
    
    return (larger-smaller)/(len(a)*len(b))
    
    
print cliffsDelta(a, b)
