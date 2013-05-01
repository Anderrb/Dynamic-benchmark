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

from gold.statistic.MagicStatFactory import MagicStatFactory
from gold.statistic.Statistic import Statistic, StatisticDictSumResSplittable
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
from gold.util.CustomExceptions import ShouldNotOccurError
from quick.statistic.BinSizeStat import BinSizeStat
from collections import OrderedDict
import numpy

class RawOverlapAllowSingleTrackOverlapsStat(MagicStatFactory):
    pass

class RawOverlapAllowSingleTrackOverlapsStatSplittable(StatisticDictSumResSplittable):
    pass

class RawOverlapAllowSingleTrackOverlapsStatUnsplittable(Statistic):
    VERSION = '1.0'

    #def __init__(self, region, track, track2, **kwArgs):
    #    Statistic.__init__(self, region, track, track2, **kwArgs)

    def _compute(self): #Numpy Version..
        tv1, tv2 = self._children[0].getResult(), self._children[1].getResult()
        binSize = self._binSizeStat.getResult()

        tv1BpLevelCoverage = tv1.getCoverageBpLevelArray()
        tv2BpLevelCoverage = tv2.getCoverageBpLevelArray()
        
        tp = (tv1BpLevelCoverage*tv2BpLevelCoverage).sum()
        fp = tv1BpLevelCoverage[tv2BpLevelCoverage==0].sum()
        fn = tv2BpLevelCoverage[tv1BpLevelCoverage==0].sum()
        tn = ((tv1BpLevelCoverage==0) * (tv2BpLevelCoverage==0)).sum()
        
        return OrderedDict(zip(['Neither','Only1','Only2','Both'] , (tn,fp,fn,tp)))                
        
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(dense=False, allowOverlaps=None)) )
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(dense=False, allowOverlaps=None)) )
        self._binSizeStat = self._addChild( BinSizeStat(self._region, self._track2))
