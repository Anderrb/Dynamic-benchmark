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

from gold.track.TrackFormat import TrackFormatReq
from gold.statistic.MagicStatFactory import MagicStatFactory
from gold.statistic.Statistic import Statistic
from gold.statistic.CountStat import CountStat
from gold.statistic.SumStat import SumStat
from gold.statistic.SumInsideStat import SumInsideStat
from gold.statistic.SumOfSquaresStat import SumOfSquaresStat
from gold.statistic.SumOfSquaresInsideStat import SumOfSquaresInsideStat
from gold.util.CustomExceptions import IncompatibleAssumptionsError
from quick.statistic.BinSizeStat import BinSizeStat

import math
import numpy
from collections import OrderedDict
#from scipy.stats import distributions
#from gold.application.RSetup import r

#fixme: Should be checked for correctness!!
from quick.statistic.CommonStatisticalTests import studentsT_uneqSize_uneqVar, \
                                                   unbiasedVar, df, dfWelchSatterthwaite

#from gold.statistic.RawDataStat import RawDataStat
#from rpy import r
#import numpy

class HigherFunctionInSegsPValStat(MagicStatFactory):
    pass

class HigherFunctionInSegsPValStatUnsplittable(Statistic):    
    #def __init__(self, region, track, track2, assumptions='independentFuncVals', **kwArgs):
    #    assert assumptions == 'independentFuncVals'
    #    Statistic.__init__(self, region, track, track2, assumptions=assumptions, **kwArgs)

    def _checkAssumptions(self, assumptions):
        if not assumptions == 'independentFuncVals':
            raise IncompatibleAssumptionsError

    def _compute(self):
        bpInside = self._children[0].getResult()
        sumBoth = self._children[1].getResult()
        sumInside = self._children[2].getResult()
        sumOfSquares = self._children[3].getResult()
        sumOfSquaresInside = self._children[4].getResult()
        regionBpSize = self._children[5].getResult()
        
        bpOutside = regionBpSize - bpInside
        #print 'len(self._region) - bpInside'
        #print len(self._region), self._region
        #from dbgp.client import brk
        #brk(host='localhost', port=9000, idekey='galaxy')
        
        #print 'here.. ',bpOutside, len(self._region), bpInside, len(self._region) - bpInside, ' to here..'

        sumOutside = sumBoth - sumInside
        sumOfSquaresOutside = sumOfSquares - sumOfSquaresInside

        meanInside = (1.0 * sumInside) / bpInside
        meanOutside = (1.0 * sumOutside) / bpOutside

        varInside = unbiasedVar(sumOfSquaresInside, sumInside, bpInside)
        varOutside = unbiasedVar(sumOfSquaresOutside, sumOutside, bpOutside)
        
        t = studentsT_uneqSize_uneqVar(bpInside, bpOutside, meanInside, meanOutside, \
                                       varInside, varOutside)
        degreesOfFreedom = dfWelchSatterthwaite(bpInside, bpOutside, varInside, varOutside)
        #print 'dfWelchSatterthwaite(bpInside, bpOutside, varInside, varOutside)'
        #print dfWelchSatterthwaite(bpInside, bpOutside, varInside, varOutside)
        #print (bpInside, bpOutside, varInside, varOutside)
        #print t
        if numpy.isnan(t) or numpy.isnan(degreesOfFreedom):
            pval = numpy.nan
        else:
            from gold.application.RSetup import r
            pval = r.pt( -numpy.abs(t),degreesOfFreedom) * 2
        return OrderedDict([ ('P-value', pval), ('Test statistic: T-score', t), ('meanInside', meanInside), ('meanOutside', meanOutside), \
                            ('diffOfMeanInsideOutside', meanInside - meanOutside), ('varInside', varInside) , ('varOutside', varOutside) ])

        #segData = self._children[0].getResult()
        #numData = self._children[1].getResult()
        #tot_inside = []
        #tot_outside = [] 
        #currPos = 0
        #for el in segData:
        #    tot_outside += [float(x.val()) for x in numData[currPos:el.start()]]
        #    tot_inside += [float(x.val()) for x in numData[el.start():el.end()]]
        #    currPos = el.end()
        #
        ##BUG? What about the rest of the bin, after last end()???
        #
        #if sum(1 for x in tot_inside if not numpy.isnan(x))==0 or sum(1 for x in tot_outside if not numpy.isnan(x))==0:
        #    return None
        #
        #c=r.t_test(tot_inside, tot_outside, 'two.sided')
        #return c['p.value']
    
    def _createChildren(self):
        self._addChild(CountStat(self._region, self._track))
        self._addChild(SumStat(self._region, self._track2))
        self._addChild(SumInsideStat(self._region, self._track, self._track2))
        self._addChild(SumOfSquaresStat(self._region, self._track2))
        self._addChild(SumOfSquaresInsideStat(self._region, self._track, self._track2))
        self._addChild(BinSizeStat(self._region, self._track))

        #
        #self._addChild(RawDataStat(self._region, self._track, TrackFormatReq(interval=True, dense=False)))
        #self._addChild(RawDataStat(self._region, self._track2, TrackFormatReq(dense=True, interval=False, val='number')))

    
