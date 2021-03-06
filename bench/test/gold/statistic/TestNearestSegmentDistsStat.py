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

class TestNearestSegmentDistsStatUnsplittable(StatUnitTest):
    classToCreate = NearestSegmentDistsStat

    def testIncompatibleTracks(self):
        self._assertIncompatibleTracks(SampleTV( starts=[0,5] ), SampleTV( starts=[0,5] ))
        self._assertIncompatibleTracks(SampleTV( ends=[0,5] ), SampleTV( ends=[0,5] ))
        self._assertIncompatibleTracks(SampleTV_Num( anchor=[5,10] ), SampleTV_Num( anchor=[5,10] ))

    def test_compute(self):
        self._assertCompute([], SampleTV( segments=[] ), SampleTV( segments=[[1,2],[4,5],[5,6],[6,7],[8,9]] ),\
                            assertFunc=self.assertListsOrDicts)
        self._assertCompute([None,None], SampleTV( segments=[[2,3],[6,7]] ), SampleTV( segments=[] ),\
                            assertFunc=self.assertListsOrDicts)
        self._assertCompute([1,1,0,1,2], SampleTV( segments=[[0,1],[2,3],[6,7],[7,8],[10,11]] ), \
                                         SampleTV( segments=[[1,2],[4,5],[5,6],[6,7],[8,9]] ),\
                                         assertFunc=self.assertListsOrDicts)
        
        self._assertCompute([3,2,0,0,3,7], SampleTV( segments=[[0,2],[8,11],[14,18],[20,23],[26,28],[30,32]] ), \
                                           SampleTV( segments=[[4,6],[12,16],[22,24]] ),\
                                           assertFunc=self.assertListsOrDicts)
        self._assertCompute([0,0,0,0,0], SampleTV( segments=[[20,26],[28,32],[34,36],[38,42],[54,58]] ), \
                                         SampleTV( segments=[[22,24],[30,40],[52,56],[57,60]] ),\
                                         assertFunc=self.assertListsOrDicts)

        #test strand-specific dist
        self._assertCompute([3,3,0,0,None,7], SampleTV( segments=[[0,2],[8,11],[14,18],[20,23],[26,28],[30,32]], strands=[True,False,False,True,True,False] ), \
                                           SampleTV( segments=[[4,6],[12,16],[22,24]] ),\
                                           assertFunc=self.assertListsOrDicts, distDirection='downstream')
        self._assertCompute([3,3,0,0,None,7], SampleTV( segments=[[0,2],[8,11],[14,18],[20,23],[26,28],[30,32]], strands=[False,True,True,False,False,True] ), \
                                           SampleTV( segments=[[4,6],[12,16],[22,24]] ),\
                                           assertFunc=self.assertListsOrDicts, distDirection='upstream')
        self._assertCompute([None,2,0,0,3,None], SampleTV( segments=[[0,2],[8,11],[14,18],[20,23],[26,28],[30,32]], strands=[True,False,False,True,True,False] ), \
                                           SampleTV( segments=[[4,6],[12,16],[22,24]] ),\
                                           assertFunc=self.assertListsOrDicts, distDirection='upstream')
        
        self._assertCompute([100], SampleTV( segments=[[110,120]] ), SampleTV( segments=[[0,11]] ),\
                                   assertFunc=self.assertListsOrDicts)
        
        
    def test_createChildren(self):
        self._assertCreateChildren([RawDataStatUnsplittable] * 2, SampleTV( segments=[[10,100]] ), SampleTV( segments=[[10,100]] ))

    def runTest(self):
        self.test_compute()
    
#class TestNearestSegmentDistStatSplittable(StatUnitTest):
#    classToCreate = NearestSegmentDistStat
#
#    def test_compute(self):
#        pass
#        
#    def test_createChildren(self):
#        pass
    
    #def runTest(self):
    #    pass

if __name__ == "__main__":    
    #TestNearestSegmentDistStatSplittable().debug()
    #TestNearestSegmentDistsStatUnsplittable().debug()
    unittest.main()
