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
from numpy import memmap
import os
import sys

import gold.util.CompBinManager
import gold.origdata.OutputIndexFilePair

from gold.origdata.GenomeElement import GenomeElement
from test.util.Asserts import AssertList
from test.util.FileUtils import removeFile

sys.stderr = open('/dev/null', 'w')

class TestOutputIndexFilePair(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.tempnam())
        gold.util.CompBinManager.COMP_BIN_SIZE = 100
        self.prevCompBinSize = gold.util.CompBinManager.COMP_BIN_SIZE
        #self.prevCompBinSize = gold.origdata.OutputIndexFilePair.COMP_BIN_SIZE
        #gold.origdata.OutputIndexFilePair.COMP_BIN_SIZE = 100

    def tearDown(self):
        self._removeFiles()
        #gold.origdata.OutputIndexFilePair.COMP_BIN_SIZE = self.prevCompBinSize
        gold.util.CompBinManager.COMP_BIN_SIZE = self.prevCompBinSize
        
    def _removeFiles(self):
        removeFile(self.path + os.sep + 'leftIndex.int32')
        removeFile(self.path + os.sep + 'rightIndex.int32')
        
    def _assertIndexFile(self, contents, prefix):
        fn = self.path + os.sep + prefix + '.int32'
        if len(contents) == 0:
            self.assertFalse(os.path.exists(fn))
        else:
            self.assertTrue(os.path.exists(fn))
            fileContents = [el for el in memmap(fn, 'int32', mode='r')]
            AssertList(contents, fileContents, self.assertEqual)
        
    def _assertWriteIndexes(self, leftContents, rightContents, startList, endList, endIndex):
        prefixList = (['start'] if startList!=[] else []) + (['end'] if endList!=[] else [])
        from gold.origdata.OutputIndexFilePair import OutputIndexFilePair
        of = OutputIndexFilePair(self.path, prefixList, endIndex)
        
        genomeElements = [ GenomeElement(start = startList[i] if i<len(startList) else None, \
                                         end = endList[i] if i<len(endList) else None) \
                           for i in xrange( max(len(startList), len(endList)) ) ]
        
#        for ge in genomeElements:
#            print ge.start, ge.end
        
        for ge in genomeElements:
            of.writeElement(ge)
        of.close()
        
        self._assertIndexFile(leftContents, 'leftIndex')
        self._assertIndexFile(rightContents, 'rightIndex')
        self._removeFiles()

    def testWriteIndexes(self):
        self._assertWriteIndexes([], [], [], [], 300)

        self._assertWriteIndexes([1, 1, 1], [1, 1, 1], [-1], [], 300)
        self._assertWriteIndexes([1, 1, 1], [1, 1, 1], [-1], [0], 300)
        self._assertWriteIndexes([1, 1, 1], [1, 1, 1], [], [0], 300)
        
        self._assertWriteIndexes([0, 1, 3, 3], [1, 3, 3, 4], [10, 120, 130, 300], [], 400)
        self._assertWriteIndexes([0, 1, 2, 3], [1, 3, 3, 4], [10, 120, 130, 300], [20, 130, 300, 310], 400)
        
        self._assertWriteIndexes([0, 1, 2, 3], [3, 4, 4, 5], [], [0, 20, 130, 300, 400], 400)
        self._assertWriteIndexes([0, 1, 2, 3], [3, 4, 4, 5], [], [10, 20, 130, 300, 400], 400)
        self._assertWriteIndexes([0, 1, 1, 3], [3, 3, 3, 5], [], [10, 20, 300, 300, 400], 400)
        
        self._assertWriteIndexes([0, 1, 3, 3, 4], [1, 3, 3, 4, 4], [10, 120, 130, 300], [], 450)
        self._assertWriteIndexes([0, 1, 2, 3, 4], [1, 3, 3, 4, 4], [10, 120, 130, 300], [20, 130, 300, 310], 450)
        
        self._assertWriteIndexes([0, 1, 2, 3, 3], [3, 4, 4, 5, 5], [], [0, 20, 130, 300, 450], 450)
        self._assertWriteIndexes([0, 1, 2, 3, 3], [3, 4, 4, 5, 5], [], [10, 20, 130, 300, 450], 450)

        self._assertWriteIndexes([0, 0, 0, 2, 2, 3, 3], [0, 0, 2, 2, 3, 3, 3], [210, 220, 400], [], 650)
        self._assertWriteIndexes([0, 0, 0, 1, 2, 3, 3], [0, 0, 2, 2, 3, 3, 3], [210, 220, 400], [220, 350, 410], 650)
        
        self._assertWriteIndexes([0, 1, 1, 1, 2, 2, 2], [1, 1, 1, 2, 2, 2, 3], [0, 350, 650], [], 700)
        self._assertWriteIndexes([0, 0, 0, 0, 1, 1, 1], [1, 1, 1, 2, 2, 2, 3], [0, 350, 650], [350, 650, 700], 700)
        
        self._assertWriteIndexes([0, 0, 0, 0, 1, 1, 1], [2, 2, 2, 3, 3, 3, 4], [], [0, 350, 650, 700], 700)
        self._assertWriteIndexes([0, 0, 0, 0, 1, 1, 1], [1, 1, 2, 3, 3, 3, 4], [], [200, 350, 650, 700], 700)
    
    def runTest(self):
        self.testWriteIndexes()
    
if __name__ == "__main__":
    #TestOutputIndexFilePair().debug()
    unittest.main()
