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
from gold.statistic.AllStatistics import *

from test.gold.statistic.StatUnitTest import StatUnitTest
from test.gold.track.common.SampleTrackView import SampleTV, SampleTV_Num

class TestHistReducerStatUnsplittable(StatUnitTest):
    classToCreate = HistReducerStat

    #def testIncompatibleTracks(self):
    #    self._assertIncompatibleTracks(SampleTV( 1 ))

    def test_compute(self):
        self._assertCompute(range(4), SampleTV_Num( vals=range(10,30) ), \
                            numDiscreteVals=4, reducedNumDiscreteVals=4, assertFunc=self.assertListsOrDicts)


    #def test_createChildren(self):
    #    self._assertCreateChildren([4], SampleTV_Num( anchor=5 ))

    def runTest(self):
        pass
    
#class TestHistReducerStatSplittable(StatUnitTest):
#    classToCreate = HistReducerStat
#
#    def test_compute(self):
#        pass
#        
#    def test_createChildren(self):
#        pass
    
    def runTest(self):
        pass
    
if __name__ == "__main__":
    #TestHistReducerStatSplittable().debug()
    #TestHistReducerStatUnsplittable().debug()
    unittest.main()
