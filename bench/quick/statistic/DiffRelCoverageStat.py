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

#Note: Not yet tested. Should have unit and intTest.
import third_party.stats as stats
import math
from gold.statistic.MagicStatFactory import MagicStatFactory
from gold.statistic.Statistic import Statistic
from gold.statistic.CountPointStat import CountPointStat
from quick.statistic.CountPointAllowingOverlapStat import CountPointAllowingOverlapStat
from gold.statistic.CountStat import CountStat
from gold.util.CustomExceptions import SplittableStatNotAvailableError, ShouldNotOccurError
from config.Config import DEFAULT_GENOME
from quick.application.UserBinSource import GlobalBinSource, MinimalBinSource, UserBinSource
from gold.util.CommonFunctions import isIter
from collections import OrderedDict
from quick.statistic.GenericRelativeToGlobalStat import GenericRelativeToGlobalStatUnsplittable

class DiffRelCoverageStat(MagicStatFactory):
    pass

class DiffRelCoverageStatUnsplittable(Statistic):
    IS_MEMOIZABLE = False
    
    def _init(self, globalSource='', minimal=False, **kwArgs):
        self._globalSource = GenericRelativeToGlobalStatUnsplittable.getGlobalSource(globalSource, self.getGenome(), minimal)
                    
    def _createChildren(self):
        #countClass = CountPointAllowingOverlapStat if self._configuredToAllowOverlaps(strict=False) else CountPointStat
        countClass = CountStat
        globCount1 = countClass(self._globalSource , self._track)
        globCount2 = countClass(self._globalSource , self._track2)
        binCount1 = countClass(self._region, self._track)
        binCount2 = countClass(self._region, self._track2)

        self._addChild(globCount1)
        self._addChild(globCount2)
        self._addChild(binCount1)
        self._addChild(binCount2)

    def _compute(self):    
        n1 = self._children[0].getResult()
        n2 = self._children[1].getResult()
        c1 = self._children[2].getResult()
        c2 = self._children[3].getResult()
        #print '*',c1,c2,n1,n2
        
        t1BinProportion = 1.0 * c1 / n1
        t2BinProportion = 1.0 * c2 / n2
        res = (t1BinProportion / t2BinProportion) if t2BinProportion is not None else None
        print 'TEMP1: ', type(res), res
        res = float(res)
        print 'TEMP2: ', type(res), res
        return res
