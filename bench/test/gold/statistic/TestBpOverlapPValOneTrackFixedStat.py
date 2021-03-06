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

class TestBpOverlapPValOneTrackFixedStatUnsplittable(StatUnitTest):
    #THROW_EXCEPTION = False
    classToCreate = BpOverlapPValOneTrackFixedStat

    #def testIncompatibleTracks(self):
    #    self._assertIncompatibleTracks(SampleTV( (  )) ))

    def test_compute(self):
        self._assertCompute({'BpsInTrack2Segments': 5, 'P-value': 1.0, 'track2Coverage': 0.25, 'E(Test statistic): ExpBpOverlap': 2.5, 'track1Coverage': 0.5, 'Test statistic: ObsBpOverlap': 0, 'DiffFromMean': -2.5},\
                            SampleTV( segments=[[5,10],[15,20]], anchor=[0,20] ), SampleTV( segments=[[10,15]], anchor=[0,20] ))
        self._assertCompute({'BpsInTrack2Segments': 10, 'P-value': 0.5, 'track2Coverage': 0.5, 'E(Test statistic): ExpBpOverlap': 5.0, 'track1Coverage': 0.5, 'Test statistic: ObsBpOverlap': 5, 'DiffFromMean': 0.0},\
                            SampleTV( segments=[[0,10]], anchor=[0,20] ), SampleTV( segments=[[5,15]], anchor=[0,20] ))
        self._assertCompute({'BpsInTrack2Segments': 100, 'P-value': 0.0, 'track2Coverage': 0.5, 'E(Test statistic): ExpBpOverlap': 50.0, 'track1Coverage': 0.5, 'Test statistic: ObsBpOverlap': 100, 'DiffFromMean': 50.0},\
                            SampleTV( segments=[[0,100]], anchor=[0,200] ), SampleTV( segments=[[0,100]], anchor=[0,200] ))
        self._assertCompute({'BpsInTrack2Segments': 10, 'P-value': 0.5, 'track2Coverage': 0.5, 'E(Test statistic): ExpBpOverlap': 5.0, 'track1Coverage': 0.5, 'Test statistic: ObsBpOverlap': 5, 'DiffFromMean': 0.0},\
                            SampleTV( segments=[[0,10]], anchor=[0,20] ), SampleTV( segments=[[5,15]], anchor=[0,20] ))

        self._assertCompute({'BpsInTrack2Segments': 0, 'P-value': None, 'track2Coverage': 0.0, 'E(Test statistic): ExpBpOverlap': 0.0, 'track1Coverage': 0.5, 'Test statistic: ObsBpOverlap': 0, 'DiffFromMean': 0.0},\
                            SampleTV( segments=[[0,10]], anchor=[0,20] ), SampleTV( segments=[], anchor=[0,20] ))
        self._assertCompute({'BpsInTrack2Segments': 0, 'P-value': None, 'track2Coverage': 0.0, 'E(Test statistic): ExpBpOverlap': 0.0, 'track1Coverage': 0.0, 'Test statistic: ObsBpOverlap': 0, 'DiffFromMean': 0.0},\
                            SampleTV( segments=[], anchor=[0,20] ), SampleTV( segments=[], anchor=[0,20] ))
        
    #def test_createChildren(self):
    #    self._assertCreateChildren([], SampleTV_Num( anchor=   ))

    def runTest(self):
        pass
    
#class TestBpOverlapPValOneTrackFixedStatSplittable(StatUnitTest):
#    classToCreate = BpOverlapPValOneTrackFixedStat
#
#    def test_compute(self):
#        pass
#        
#    def test_createChildren(self):
#        pass
    
    #def runTest(self):
    #    pass
    
if __name__ == "__main__":
    #TestBpOverlapPValStatSplittable().debug()
    #TestBpOverlapPValStatUnsplittable().debug()
    unittest.main()
