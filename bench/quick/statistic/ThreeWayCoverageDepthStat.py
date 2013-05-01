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
from gold.statistic.Statistic import Statistic, StatisticDictSumResSplittable, MultipleRawDataStatistic
from quick.statistic.ThreeWayBpOverlapStat import ThreeWayBpOverlapStatUnsplittable
from quick.statistic.BinSizeStat import BinSizeStat
from quick.util.CommonFunctions import numAsPaddedBinary
from gold.track.TrackFormat import TrackFormatReq
import numpy

class ThreeWayCoverageDepthStat(MagicStatFactory):
    pass

class ThreeWayCoverageDepthStatSplittable(StatisticDictSumResSplittable):
    pass
            
class ThreeWayCoverageDepthStatUnsplittable(MultipleRawDataStatistic):
    #from gold.util.CommonFunctions import repackageException
    #from gold.util.CustomExceptions import ShouldNotOccurError
    #@repackageException(Exception, ShouldNotOccurError)
    
    def _compute(self):
        zeroOneTracks = [child.getResult().getBinaryBpLevelArray()+0 for child in self._children] #+0 to get as integer arrays
        binSize = len(zeroOneTracks[0])
        numTracks = len(zeroOneTracks)
        
        sumTrack = numpy.zeros(binSize,dtype='int')
        for track in zeroOneTracks:
            sumTrack += track
        depthCount = dict(enumerate(numpy.bincount(sumTrack)))
        for depth in range(len(depthCount), numTracks+1):
            depthCount[depth] = 0
            
        res = {}
        for key,val in depthCount.items():
            res['Depth %i'%key] = val
        res['BinSize'] = binSize
        #print res
        return res       
        
    def _getTrackFormatReq(self):
        return TrackFormatReq(dense=False)
        
    #_createChildren = ThreeWayBpOverlapStatUnsplittable._createChildren    
    
    #def _compute(self):
    #    t = self._children[0].getResult()
    #    binSize = self._children[1].getResult()
    #    
    #    numTracks = len(t.keys()[0])
    #    from collections import Counter
    #    countPerDepth = Counter()
    #    for combA in range(1,2**numTracks): #enumerate with binary number corresponding to all subsets
    #        binaryA = numAsPaddedBinary(combA,numTracks)
    #        #tracksInA = set([i for i,x in enumerate(binaryA) if x=='1'])
    #        depth = binaryA.count('1')
    #        countPerDepth[depth] += t[binaryA]
    #        
    #    countPerDepth[0] = binSize
    #    
    #    distinctCountPerDepth = {}
    #    for depth in range(numTracks):
    #        distinctCountPerDepth[depth] = countPerDepth[depth] - countPerDepth[depth+1]
    #    distinctCountPerDepth[numTracks] = countPerDepth[numTracks]
    #    print 'DICTS: ',countPerDepth, distinctCountPerDepth
    #    assert binSize == sum(distinctCountPerDepth.values())
    #
    #    chanceOfExtraPerDepth = {}        
    #    for depth in range(numTracks):
    #        chanceOfExtraPerDepth[depth] = countPerDepth[depth+1] / float(countPerDepth[depth])
    #        
    #    #countPerDepth['Depth 0'] = binSize - 
    #    res = {}
    #    for key,val in distinctCountPerDepth.items():
    #        res['Depth '+str(key)] = val
    #    for key,val in chanceOfExtraPerDepth.items():
    #        res['Proportion of extra coverage given depth '+str(key)] = val
    #    res['BinSize'] = binSize
    #    #print res
    #    return res       
    #    
    #
    #def _createChildren(self):
    #    self._addChild( ThreeWayBpOverlapStat(self._region, self._track, self._track2, **self._kwArgs) )
    #    self._addChild( BinSizeStat(self._region, self._track) )
    #    
