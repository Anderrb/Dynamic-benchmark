# Copyright (C) 2009, Geir Kjetil Sandve, Sveinung Gundersen and Morten Johansen
# This file is part of The Genomic HyperBrowser.
#
#    The Genomic HyperBrowser is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    The Genomic HyperBrowser is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with The Genomic HyperBrowser.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os
import sys

from gold.util.CustomExceptions import ShouldNotOccurError
from gold.util.DiskMirroredDict import DiskMirroredDict, SafeDiskMirroredDict
#from test.util.Asserts import TestCaseWithImprovedAsserts
from test.util.FileUtils import removeFile

sys.stderr = open('/dev/null', 'w')

#class TestDiskMirroredDict(TestCaseWithImprovedAsserts):
class TestDiskMirroredDict(unittest.TestCase):
    def setUp(self):
        self._fn = os.tempnam()
    
    def testMirror(self):
        myDict = DiskMirroredDict(self._fn)
        myDict.update({1:1, 2:3})
        myDict[4] = 5
        self.assertEqual([1,3,5], [myDict[x] for x in [1,2,4]])
        myDict.close()
        
        myDict2 = DiskMirroredDict(self._fn)
        myDict2[2] = 2
        myDict2[6] = 7
        self.assertEqual([1,2,5,7], [myDict2[x] for x in [1,2,4,6]])
        myDict2.close()

        myDict3 = DiskMirroredDict(self._fn)
        self.assertEqual([1,2,5,7], [myDict3[x] for x in [1,2,4,6]])
        myDict3.close()
    
    def testSafeMirror(self):
        myDict = SafeDiskMirroredDict(self._fn)
        myDict.update({0:2, 1:1, 2:3})
        myDict.close()
        
        myDict2a = SafeDiskMirroredDict(self._fn)
        myDict2a[1] = 2
        myDict2a[3] = 7

        myDict2b = SafeDiskMirroredDict(self._fn)
        myDict2b[2] = 4
        myDict2b[4] = 10

        self.assertRaises(Exception, myDict2b.close)
        
        myDict2a.close()
        
        self.assertRaises(ShouldNotOccurError, myDict2b.close)        

        myDict3 = SafeDiskMirroredDict(self._fn)
        self.assertEqual([2,2,3,7], [myDict3[x] for x in [0,1,2,3]])
        self.assertEqual(4, len(myDict3.keys()))
        myDict3.close()
        
    def tearDown(self):
        removeFile(self._fn)
    
    def runTest(self):
        pass
    
if __name__ == "__main__":
    #TestDiskMirroredDict().debug()
    unittest.main()