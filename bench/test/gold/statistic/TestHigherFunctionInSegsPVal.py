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
import numpy
from gold.statistic.AllStatistics import *

from test.gold.statistic.StatUnitTest import StatUnitTest
from test.gold.track.common.SampleTrackView import SampleTV, SampleTV_Num

class TestHigherFunctionInSegsPValStatUnsplittable(StatUnitTest):
    classToCreate = HigherFunctionInSegsPValStat

    def test_compute(self):
        self._assertCompute({'P-value': 0.012674105780756399, 'Test statistic: T-score': 2.842957256048134, 'meanInside': 13.833333333333334, 'meanOutside': 7.6428571428571432, 'diffOfMeanInsideOutside': 6.1904761904761907, 'varInside': 14.166666666666652, 'varOutside': 33.324175824175818}, \
                            SampleTV( anchor=[0,20], segments=[[10,14], [18,20]] ),\
                            SampleTV_Num( anchor=[0,20], vals=xrange(20) ))
        
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': numpy.nan, 'meanOutside': 9.5, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': numpy.nan, 'varOutside':  35.0}, \
                            SampleTV( anchor=[0,20], segments=[] ),\
                            SampleTV_Num( anchor=[0,20], vals=xrange(20) ))
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': 9.5, 'meanOutside': numpy.nan, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': 35.0, 'varOutside': numpy.nan}, \
                            SampleTV( anchor=[0,20], segments=[[0,20]] ),\
                            SampleTV_Num( anchor=[0,20], vals=xrange(20) ))
        
        #self._assertCompute( 0.026892673635612367, SampleTV( anchor=[0,20], segments=[[10,14], [18,20]] ),\
                            #SampleTV_Num( anchor=[0,20], vals=range(19) + [numpy.nan] ), assertFunc=self.assertAlmostEqual)
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': numpy.nan, 'meanOutside': numpy.nan, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': numpy.nan, 'varOutside': numpy.nan}, \
                            SampleTV( anchor=[0,20], segments=[[10,14], [18,20]] ),\
                            SampleTV_Num( anchor=[0,20], vals=range(19) + [numpy.nan] ))
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': numpy.nan, 'meanOutside': numpy.nan, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': numpy.nan, 'varOutside': numpy.nan}, \
                            SampleTV( anchor=[0,20], segments=[[10,14], [18,20]] ),\
                            SampleTV_Num( anchor=[0,20], vals=[numpy.nan]*20 ))

    def test_compute2(self):
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': numpy.nan, 'meanOutside': numpy.nan, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': numpy.nan, 'varOutside': numpy.nan}, \
                            SampleTV( segments=[], anchor=[0,0] ), \
                            SampleTV_Num( vals=[], anchor=[0,0] ))
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': numpy.nan, 'meanOutside': 7.5124998092651367, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': numpy.nan, 'varOutside': 41.432686031886469}, \
                            SampleTV( segments=[], anchor=[0,8] ), \
                            SampleTV_Num( vals=[13.0, 14.0, 1.2, 2.1, 14.2, 12.8, 0.6, 2.2], anchor=[0,8] ))
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': 13, 'meanOutside': numpy.nan, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': numpy.nan, 'varOutside': numpy.nan}, \
                            SampleTV( segments=[[0,1]], anchor=[0,1] ), \
                            SampleTV_Num( vals=[13.0], anchor=[0,1] ))
        self._assertCompute({'P-value': numpy.nan, 'Test statistic: T-score': numpy.nan, 'meanInside': 7.5750002861022949, 'meanOutside': numpy.nan, 'diffOfMeanInsideOutside': numpy.nan, 'varInside': 47.109162921905408, 'varOutside': numpy.nan}, \
                            SampleTV( segments=[[0,4]], anchor=[0,8] ), \
                            SampleTV_Num( vals=[13.0, 14.0, 1.2, 2.1, 14.2, 12.8, 0.6, numpy.nan], anchor=[0,8] ))
#{'P-value':0.0, 'T-score':23.090362405587562},
#{'P-value':0.0, 'T-score':-23.090156227804243},
#{'P-value':1.0, 'T-score':0.0}, 
        self._assertCompute({'P-value':  0.0, 'Test statistic: T-score':  23.090362405587562, 'meanInside': 13.5, 'meanOutside': 1.5249996185302734, 'diffOfMeanInsideOutside':  11.975000381469727, 'varInside':  0.49332682291666669 , 'varOutside': 0.582517827351694}, \
                            SampleTV( segments=[[0,2], [4,6]], anchor=[0,8] ), \
                            SampleTV_Num( vals=[13.0, 14.0, 1.2, 2.1, 14.2, 12.8, 0.6, 2.2], anchor=[0,8] ))
        self._assertCompute({'P-value':  0.0, 'Test statistic: T-score': -23.090156227804243, 'meanInside': 1.5249996185302734, 'meanOutside': 13.5, 'diffOfMeanInsideOutside': -11.975000381469727, 'varInside':  0.58249935785928153, 'varOutside':  0.49336433410614217}, \
                            SampleTV( segments=[[2,4], [6,8]], anchor=[0,8] ), \
                            SampleTV_Num( vals=[13.0, 14.0, 1.2, 2.1, 14.2, 12.8, 0.6, 2.2], anchor=[0,8] ))
        self._assertCompute({'P-value':  1.0, 'Test statistic: T-score': 0.0, 'meanInside':  2.575, 'meanOutside':  2.575, 'diffOfMeanInsideOutside': 0.0, 'varInside': 1.4425014368692548, 'varOutside': 1.4425014368692548}, \
                            SampleTV( segments=[[0,4]], anchor=[0,8] ), \
                            SampleTV_Num( vals=[3.0, 4.0, 1.2, 2.1, 4.0, 3.0, 1.2, 2.1], anchor=[0,8] ))
    def runTest(self):
        self.test_compute()
    
#class TestHigherFunctionInSegsPValStatSplittable(StatUnitTest):
#    classToCreate = HigherFunctionInSegsPValStat
#
#    def test_compute(self):
#        pass
#        
#    def test_createChildren(self):
#        pass
    
    #def runTest(self):
        #pass
    
if __name__ == "__main__":
    #TestHigherFunctionInSegsPValStatSplittable().debug()
    #TestHigherFunctionInSegsPValStatUnsplittable().debug()
    unittest.main()
