import sys
import time

if __name__ == '__main__':
    s = "hello, world"
    print len(s)
    if len(s) > 100:
        print "long"
    else:
        print "short"

    print s[0:4]