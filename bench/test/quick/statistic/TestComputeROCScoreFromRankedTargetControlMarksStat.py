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
from quick.statistic.MarksSortedBySegmentOverlapStat import *
from quick.statistic.MarksSortedByFunctionValueStat import *

from test.gold.statistic.StatUnitTest import StatUnitTest
from test.gold.track.common.SampleTrackView import SampleTV, SampleTV_Num

class TestComputeROCScoreFromRankedTargetControlMarksStatUnsplittable(StatUnitTest):
    classToCreate = ComputeROCScoreFromRankedTargetControlMarksStat

    def testIncompatibleTracks(self):
        pass
    
    def test_compute(self):
        self._assertCompute(0.25, SampleTV( segments = [[10,20],[30,40],[50,55], [60,62]], vals = [1,0,1,0], anchor = [0,100], valDType='bool8'),\
                                     SampleTV_Num( vals = range(100), anchor = [0,100] ), rankType = 'funcval' )
        self._assertCompute(0.75, SampleTV( segments = [[10,20],[30,40],[50,55], [60,62]], vals = [0,1,0,1], anchor = [0,100], valDType='bool8'),\
                                     SampleTV_Num( vals = range(100), anchor = [0,100] ), rankType = 'funcval' )
        self._assertCompute(0.5, SampleTV( numElements = 0, anchor = [0,100], valDType='bool8'),\
                                     SampleTV_Num( vals = range(100),anchor = [0,100]), rankType = 'funcval' ) 

        self._assertCompute(0.25, SampleTV( segments = [[10,20],[30,40],[50,55],[80,90]], vals = [1,0,1,0], valDType='bool8'),\
                                     SampleTV(segments = [[15,25],[34,40],[51,55], [80,90]]), rankType = 'overlap' ) 
        self._assertCompute(0.75, SampleTV( segments = [[10,20],[30,40],[50,55],[80,90]], vals = [0,1,0,1], valDType='bool8'),\
                                     SampleTV(segments = [[15,25],[34,40],[51,55], [80,90]]), rankType = 'overlap' ) 
        self._assertCompute(0.5, SampleTV( numElements = 0, valDType='bool8'),\
                                     SampleTV(segments = [[15,25],[34,40],[51,55]]), rankType = 'overlap' ) 
        
                
    def test_createChildren(self):
        self._assertCreateChildren([MarksSortedBySegmentOverlapStatUnsplittable],
                                   SampleTV( numElements=5 ), SampleTV( starts=False, numElements=5 ), rankType = 'overlap')
        self._assertCreateChildren([MarksSortedByFunctionValueStatUnsplittable], \
                                    SampleTV( numElements=5 ), SampleTV_Num( anchor = [10,1000]  ), rankType = 'funcval')


    def runTest(self):
        self.test_compute()
    
#class TestComputeROCScoreFromRankedTargetControlMarksStatSplittable(StatUnitTest):
#    classToCreate = ComputeROCScoreFromRankedTargetControlMarksStat
#
#    def test_compute(self):
#        pass
#        
#    def test_createChildren(self):
#        pass
    
    #def runTest(self):
    #    pass
    
if __name__ == "__main__":
    #TestComputeROCScoreFromRankedTargetControlMarksStatSplittable().debug()
    #TestComputeROCScoreFromRankedTargetControlMarksStatUnsplittable().debug()
    unittest.main()