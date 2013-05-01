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
from gold.statistic.Statistic import Statistic, StatisticSumResSplittable
from gold.statistic.RawDataStat import RawDataStat
from quick.statistic.BinSizeStat import BinSizeStat
from gold.track.TrackFormat import TrackFormatReq
from gold.util.CustomExceptions import InvalidFormatError
from gold.track.TrackView import TrackView
from gold.application.LogSetup import logMessage
from gold.util.CommonFunctions import getStringFromStrand
from gold.application.LogSetup import logMessage
import numpy as np

class MakeDistanceToNearestSegmentStat(MagicStatFactory):
    pass

            
class MakeDistanceToNearestSegmentStatUnsplittable(Statistic):
    def _init(self, valTransformation=None, **kwArgs):
        self._valTransformation = valTransformation
                
    def _compute(self):
        
        binSize = self._children[0].getResult()
        result = []
        tv = self._children[1].getResult()
        starts = tv.startsAsNumpyArray()
        ends = tv.endsAsNumpyArray()
        #logMessage('trackName and region'+',  '+  repr(self._track.trackName)+',  '+ str(self._region))
        if len(starts)>0:
            if starts[0]>0:
                result.extend(range(starts[0], 0 ,-1))
            result.extend([0]*(ends[0]-starts[0]))
            
            for index in xrange(1, len(starts)):
                delta = starts[index]-ends[index-1]
                if delta>0:
                    ascending = range(1,delta/2+1)
                    descending = range(delta/2,0,-1)
                    if delta % 2 == 1:
                        ascending.append(len(descending)+1)
                    result.extend(ascending)
                    result.extend(descending)
                result.extend([0]*(ends[index]-starts[index]))
                
                    
            if ends[-1]<binSize:
                result.extend(range(1,binSize-ends[-1]+1))
            
            res = np.array(result, dtype='float64')
            if self._valTransformation in [None, 'None']:
                pass
            elif self._valTransformation == 'log10':                
                res = np.log10(res+1)
            elif self._valTransformation =='power0.2':
                res = res**0.2
            else:
                raise
            return res
        else:
            #logMessage('trackName and region'+',  '+  repr(self._track.trackName)+',  '+ str(self._region))
            return np.zeros(binSize) + np.nan
            
    def _createChildren(self):
        self._addChild( BinSizeStat(self._region, self._track) )
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(interval=True, dense=False)) )
        