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
from quick.statistic.ThreeWayBpOverlapStat import ThreeWayBpOverlapStatUnsplittable
from quick.statistic.BinSizeStat import BinSizeStat
from quick.util.CommonFunctions import numAsPaddedBinary
import numpy

class ThreeWayFocusedTrackCoveragesAtDepthsStat(MagicStatFactory):
    pass

class ThreeWayFocusedTrackCoveragesAtDepthsStatSplittable(StatisticDictSumResSplittable):
    pass
            
class ThreeWayFocusedTrackCoveragesAtDepthsStatUnsplittable(ThreeWayBpOverlapStatUnsplittable):
    from gold.util.CommonFunctions import repackageException
    from gold.util.CustomExceptions import ShouldNotOccurError
    @repackageException(Exception, ShouldNotOccurError)
    
    def _compute(self):
        zeroOneTracks = [child.getResult().getBinaryBpLevelArray()+0 for child in self._children] #+0 to get as integer arrays
        binSize = len(zeroOneTracks[0])
        numTracks = len(zeroOneTracks)
        res = {}
        res['BinSize'] = binSize
        
        for focusTrackIndex in range(numTracks):
            sumTrack = numpy.zeros(binSize,dtype='int')
            for index, track in enumerate(zeroOneTracks):
                if index != focusTrackIndex:
                    sumTrack += track
            
            splittedSumTrack = {}
            splittedSumTrack[True] = sumTrack[zeroOneTracks[focusTrackIndex]==1] #WhereFocus
            splittedSumTrack[False] = sumTrack[zeroOneTracks[focusTrackIndex]==0] #WhereNotFocus
            depthCounts = {}
            for focus in [False,True]:
                if len(splittedSumTrack[focus]) > 0:
                    #print 'ST: ', splittedSumTrack[focus][0:20]
                    numpy.bincount(splittedSumTrack[focus])
                    #list(enumerate(numpy.bincount(splittedSumTrack[focus])))
                    depthCounts[focus] = dict(enumerate(numpy.bincount(splittedSumTrack[focus])))
                else:
                    depthCounts[focus] = {}
                for depth in range(len(depthCounts[focus]), numTracks):
                    depthCounts[focus][depth] = 0
                
            for depth in range(numTracks):
                #denom = sum( depthCounts[focus][depth] for focus in [False, True]) 
                #if denom > 0:
                    #res['Prop. cover by T%i where depth %i by other tracks'%(focusTrackIndex+1, depth)] = float(depthCounts[True][depth]) / denom
                #else:
                    #res['Prop. cover by T%i where depth %i by other tracks'%(focusTrackIndex+1, depth)] = None
                res['Coverage by T%i where depth %i by other tracks'%(focusTrackIndex+1, depth)] = depthCounts[True][depth]
                res['Not covered by T%i where depth %i by other tracks'%(focusTrackIndex+1, depth)] = depthCounts[False][depth]
                    
        return res       
