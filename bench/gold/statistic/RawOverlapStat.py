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

class RawOverlapStat(MagicStatFactory):
    pass

class RawOverlapStatSplittable(StatisticDictSumResSplittable):
    pass

class RawOverlapStatUnsplittable(Statistic):
    VERSION = '1.1'

    #def __init__(self, region, track, track2, **kwArgs):
    #    Statistic.__init__(self, region, track, track2, **kwArgs)

    def _compute(self): #Numpy Version..
        tv1, tv2 = self._children[0].getResult(), self._children[1].getResult()

        t1s = tv1.startsAsNumpyArray()
        t1e = tv1.endsAsNumpyArray()  
        t2s = tv2.startsAsNumpyArray()
        t2e = tv2.endsAsNumpyArray()

        #add bps before first and after last segment
        binSize = self._binSizeStat.getResult()
        #binSize = len(self._region)
        
        tn,fp,fn,tp = self._computeRawOverlap(t1s,t1e,t2s,t2e,binSize)


        return OrderedDict(zip(['Neither','Only1','Only2','Both'] , (tn,fp,fn,tp)))
        
    @staticmethod
    def _computeRawOverlap(t1s,t1e,t2s,t2e,binSize):
        #assert no overlaps..
        #create arrays multiplied by 8 to use last three bits to code event type,
        #Last three bits: relative to 4 (100): +/- 1 for start/end of track1, +/- 2 for track2..
        t1CodedStarts = t1s * 8 +5
        t1CodedEnds= t1e  * 8 +3
        t2CodedStarts = t2s * 8 +6
        t2CodedEnds= t2e * 8 +2
        
        allSortedCodedEvents = numpy.concatenate( (t1CodedStarts,t1CodedEnds,t2CodedStarts,t2CodedEnds) )
        allSortedCodedEvents.sort()
        
        allEventCodes = (allSortedCodedEvents % 8) -4
        
        allSortedDecodedEvents = allSortedCodedEvents / 8
        allEventLengths = allSortedDecodedEvents[1:] - allSortedDecodedEvents[:-1]
        
        #due to the coding, the last bit now has status of track1, and the second last bit status of track2
        #thus, 3 is cover by both, 2 is cover by only track2, 1 is cover by only track1, 0 is no cover
        #this works as there are no overlaps, and bits will thus not "spill over"..
        cumulativeCoverStatus = numpy.add.accumulate(allEventCodes)
        
        tn,fp,fn,tp = [long((allEventLengths[ cumulativeCoverStatus[:-1] ==status ]).sum()) for status in range(4)]
        
        if len(allSortedDecodedEvents)>0:
            tn += allSortedDecodedEvents[0] + (binSize - allSortedDecodedEvents[-1])
        else:
            tn+=binSize
            
        return tn,fp,fn,tp
        
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(dense=False)) )
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(dense=False)) )
        self._binSizeStat = self._addChild( BinSizeStat(self._region, self._track2))
