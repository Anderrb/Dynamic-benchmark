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
from gold.statistic.Statistic import Statistic, StatisticConcatNumpyArrayResSplittable, OnlyGloballySplittable
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
import numpy

class PointCountPerSegStat(MagicStatFactory):
    pass

class PointCountPerSegStatSplittable(StatisticConcatNumpyArrayResSplittable, OnlyGloballySplittable):
    IS_MEMOIZABLE = False
            
class PointCountPerSegStatUnsplittable(Statistic):    
    IS_MEMOIZABLE = False

    def _compute(self):
        tv1, tv2 = self._children[0].getResult(), self._children[1].getResult()

        codedPoints = tv1.startsAsNumpyArray()  * 8 +6 #+2 +4, with +4 to get correct sorting..
        codedStarts = tv2.startsAsNumpyArray()  * 8 +3
        codedEnds= tv2.endsAsNumpyArray()  * 8 +1
        
        if len(codedStarts)==0:
            return numpy.array([])

        allSortedCodedEvents = numpy.concatenate( (codedPoints, codedStarts, codedEnds) )
        allSortedCodedEvents.sort()

        allEventCodes = (allSortedCodedEvents % 4) -2 #Note %4, as this will remove the +4 for points
        allSortedDecodedEvents = allSortedCodedEvents / 8
        
        allIndexesOfSegEnds = numpy.nonzero(allEventCodes == -1)[0]
        
        cumulativeCoverStatus = numpy.add.accumulate(allEventCodes)
        
        pointInsidePerIndex = ( (cumulativeCoverStatus==1) & (allEventCodes==0) ).astype('int64')

        return numpy.add.reduceat(pointInsidePerIndex, numpy.concatenate(([0],allIndexesOfSegEnds)))[0:-1]
    
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(dense=False, interval=False)) )
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(dense=False, interval=True)) )
        #fixme: Track 2 should have borderhandling='include', but this is not supported yet. This to support correct splitting'
