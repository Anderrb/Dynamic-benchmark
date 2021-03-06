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
from collections import OrderedDict

class TestPropPointCountsAllowOverlapsVsSegsStatUnsplittable(StatUnitTest):
    classToCreate = PropPointCountsAllowOverlapsVsSegsStat

    #def testIncompatibleTracks(self):
    #    self._assertIncompatibleTracks(SampleTV(  ))

    def test_compute(self):
        self._assertCompute(OrderedDict([('Both', 0), ('Only1', 0), ('BothProp', None), ('Only1Prop', None), ('SegCoverage', 0)]), \
                            SampleTV( starts=[], anchor=[10,100] ), SampleTV( segments=[], anchor=[10,100] ))
        
        self._assertCompute(OrderedDict([('Both', 3), ('Only1', 2), ('BothProp', 0.6), ('Only1Prop', 0.4), ('SegCoverage', 0.25)]), \
                            SampleTV( starts=[10, 20, 40, 40, 65], anchor=[10,90] ), SampleTV( segments=[[20,30], [40,50]], anchor=[10,90] ))
        
    #def test_createChildren(self):
    #    self._assertCreateChildren([YStat], SampleTV( data2 ))

    def runTest(self):
        pass
    
#class TestPropPointCountsVsSegsStatSplittable(StatUnitTest):
#    classToCreate = PropPointCountsVsSegsStat
#
#    def test_compute(self):
#        pass
#        
#    def test_createChildren(self):
#        pass
    
    #def runTest(self):
    #    pass
    
if __name__ == "__main__":
    #TestPropPointCountsVsSegsStatSplittable().debug()
    #TestPropPointCountsVsSegsStatUnsplittable().debug()
    unittest.main()