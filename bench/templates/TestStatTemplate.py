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

class Test[[%tabstop1:X]]StatUnsplittable(StatUnitTest):
    classToCreate = [[%tabstop1:X]]Stat

    #def testIncompatibleTracks(self):
    #    self._assertIncompatibleTracks(SampleTV(  ))

    def test_compute(self):
        self._assertCompute([[%tabstop2:result]], SampleTV( [[%tabstop3:data]] ))
        
    #def test_createChildren(self):
    #    self._assertCreateChildren([[[%tabstop4:Y]]Stat], SampleTV( [[%tabstop5:data2]] ))

    def runTest(self):
        pass
    
#class Test[[%tabstop1:X]]StatSplittable(StatUnitTest):
#    classToCreate = [[%tabstop1:X]]Stat
#
#    def test_compute(self):
#        pass
#        
#    def test_createChildren(self):
#        pass
    
    #def runTest(self):
    #    pass
    
if __name__ == "__main__":
    #Test[[%tabstop1:X]]StatSplittable().debug()
    #Test[[%tabstop1:X]]StatUnsplittable().debug()
    unittest.main()