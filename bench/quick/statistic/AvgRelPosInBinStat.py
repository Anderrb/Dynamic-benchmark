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

import gold
from gold.statistic.MagicStatFactory import MagicStatFactory
from gold.statistic.Statistic import Statistic, StatisticConcatNumpyArrayResSplittable, OnlyGloballySplittable
#from gold.statistic.RawDataStat import RawDataStat
#from quick.statistic.BinSizeStat import BinSizeStat
from quick.statistic.RelPositionsInBinStat import RelPositionsInBinStat
from gold.track.TrackFormat import TrackFormatReq
from gold.util.CustomExceptions import NotSupportedError

class AvgRelPosInBinStat(MagicStatFactory):
    pass

#class MostCommonCategoryStatSplittable(StatisticConcatNumpyArrayResSplittable, OnlyGloballySplittable):
#    IS_MEMOIZABLE = False

class AvgRelPosInBinStatUnsplittable(Statistic):
    IS_MEMOIZABLE = False

    def _compute(self):
        tvArray = self._children[0].getResult()
        
        #rawRelPos = tvArray.mean()
        #if self._region.strand == False:
        #    return 1.0-rawRelPos
        #else:
        #    return rawRelPos
        return tvArray.mean()
        
    #def _compute(self):
    #    bpSize = self._children[1].getResult()
    #    tvArray = self._children[0].getResult().startsAsNumpyArray()/float(bpSize)
    #    
    #    rawRelPos = tvArray.mean()
    #    if self._region.strand == False:
    #        return 1.0-rawRelPos
    #    else:
    #        return rawRelPos
        
            
    #def _createChildren(self):
    #    self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(interval=False, dense=False) ) )
    #    self._addChild(BinSizeStat(self._region, self._track))
    def _createChildren(self):
        self._addChild(RelPositionsInBinStat(self._region, self._track))
