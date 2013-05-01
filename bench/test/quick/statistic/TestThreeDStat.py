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
from numpy import nan
from gold.statistic.AllStatistics import *

from test.gold.statistic.StatUnitTest import StatUnitTest
from test.gold.track.common.SampleTrackView import SampleTV, SampleTV_Num

class TestThreeDStatUnsplittable(StatUnitTest):
    classToCreate = ThreeDStat
    
    def test_compute(self):
        self._assertCompute({'weights': 4, 'a': 0.3}, \
                            SampleTV( segments=[[10,20], [80,90]], ids=['a','b'], \
                                      edges=[['b','a'],['a']], weights=[[1,2],[1]], \
                                      extras={'a':['0.1','0.2']}, anchor=[10,100] ))
        
    def test_createChildren(self):
        self._assertCreateChildren([RawDataStatUnsplittable], SampleTV( ids=True, edges=True, \
                                                                        weights=True, extras=['a'], numElements=3, \
                                                                        anchor=[0,100] ))

class TestThreeDStatSplittable(StatUnitTest):
    classToCreate = ThreeDStat

    def test_compute(self):
        self._assertCompute({'weights': 5, 'a': 0.5}, \
                            SampleTV( segments=[[10,20], [80,111]], ids=['a','b'], \
                                      edges=[['b','a'],['a']], weights=[[1,2],[1]], \
                                      extras={'a':['0.1','0.2']}, anchor=[10,121] ))
        
        self._assertCompute({'weights': 4, 'a': 0.3}, \
                            SampleTV( segments=[[10,20], [100,111]], ids=['a','b'], \
                                      edges=[['b','a'],['a']], weights=[[1,2],[1]], \
                                      extras={'a':['0.1','0.2']}, anchor=[10,121] ))
        
if __name__ == "__main__":
    unittest.main()