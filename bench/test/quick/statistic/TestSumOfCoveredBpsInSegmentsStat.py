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

class TestSumOfCoveredBpsInSegmentsStatUnsplittable(StatUnitTest):
    classToCreate = SumOfCoveredBpsInSegmentsStat
    
    
    def test_compute(self):
        self._assertCompute(20, SampleTV_Num( vals=[2]*90, anchor=[10,100] ), SampleTV( segments=[[0,10]], anchor=[10,100] ))
        self._assertCompute(40, SampleTV( segments=[[10,20], [80,85]], vals=[1,10], anchor=[10,100] ), SampleTV( segments=[[10,20], [80,83]], anchor=[10,100] ))
        self._assertCompute(10,  SampleTV( starts=[2,15,60], vals=[1,10,100], anchor=[10,100] ), SampleTV( segments=[[10,20], [80,85]], anchor=[10,100] ))
        self._assertCompute(205, SampleTV( ends=[15,90], vals=[1,10], anchor=[10,100] ), SampleTV( segments=[[10,20], [40,55]], anchor=[10,100] ))
        #self._assertCompute(0, SampleTV( segments=[], anchor=[10,100] ), SampleTV( segments=[], anchor=[10,100] ))
        
    #def test_createChildren(self):
    #    self._assertCreateChildren([RawDataStatUnsplittable, RawDataStatUnsplittable], SampleTV_Num( anchor=[0,100] ), SampleTV(segments=[],  anchor=[0,100] ))

#class TestSumOfCoveredBpsInSegmentsStatUnsplittable(StatUnitTest):
#    classToCreate = SumOverCoveredBpsStat
#
#    def test_compute(self):
#        self._assertCompute(200, SampleTV_Num( vals=[2]*100, anchor=[10,110] ))
#        self._assertCompute(210, SampleTV( segments=[[10,20], [80,100]], vals=[1,10], anchor=[10,110] ))
#        self._assertCompute(111,  SampleTV( starts=[2,15,99], vals=[1,10,100], anchor=[10,110] ))
#        self._assertCompute(865, SampleTV( ends=[15,100], vals=[1,10], anchor=[10,110] ))
#        self._assertCompute(0, SampleTV( segments=[], anchor=[10,110] ))
        
if __name__ == "__main__":
    unittest.main()