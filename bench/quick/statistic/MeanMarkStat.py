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
from gold.statistic.Statistic import Statistic
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
import math

class MeanMarkStat(MagicStatFactory):
    pass

#class MeanMarkStatSplittable(StatisticSumResSplittable):
#    pass
            
class MeanMarkStatUnsplittable(Statistic):    
    def _compute(self):
        #return float(self._children[0].getResult().valsAsNumpyArray().mean())
        vals = self._children[0].getResult().valsAsNumpyArray()
        if vals is None or len(vals) == 0:
            return None
        else:
            meanVal = float(vals.mean())
            return math.log(meanVal, 2) if meanVal != 0 else 0
    
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(val='number', dense=False, interval=False)) )
