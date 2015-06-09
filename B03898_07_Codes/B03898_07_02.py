"""
README
======
This file contains Python codes.
Save this file as mapper.py.
======
"""

#!/usr/bin/python
import sys
 
for line in sys.stdin:
    for word in line.strip().split():
        print "%s\t%d" % (word, 1)
