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

#Untested, to be rewritten
#import stats
from gold.util.RandomUtil import random
import numpy
from numpy import array
from gold.track.TrackView import TrackView
from gold.statistic.RawDataStat import RawDataStat
from gold.track.Track import Track
from gold.track.TrackFormat import NeutralTrackFormatReq
from test.gold.track.common.SampleTrackView import SampleTV_Num
from gold.util.CommonFunctions import isIter
from gold.util.CustomExceptions import AbstractClassError

class RandomizedTrack(Track):
    IS_MEMOIZABLE = False

    def __new__(cls, *args, **kwArgs):
        return object.__new__(cls)
    
    def __init__(self, origTrack, origRegion, randIndex, **kwArgs ):
        self._origTrack = origTrack
        self.trackName = origTrack.trackName + ['Randomized', str(randIndex)]        
        self._origRegion = origRegion
        self._trackFormatReq = NeutralTrackFormatReq()
        self._cachedTV = None

    def _checkTrackFormat(self, origTV):
        pass
    
    def getTrackView(self, region):
        #print 'get tv for reg: ',region
        #print str(type(self._origRegion)) + " and " + str(type(region))
        assert (not isIter(self._origRegion) and self._origRegion  == region) or (isIter(self._origRegion) and region in self._origRegion) 
        
        #if self._cachedTV is None:
        rawData = RawDataStat(region, self._origTrack, self._trackFormatReq)
        origTV = rawData.getResult()
        self._checkTrackFormat(origTV)
        assert(not origTV.allowOverlaps)
        assert(origTV.borderHandling == 'crop')
        assert region == origTV.genomeAnchor
        starts, ends, vals, strands, ids, edges, weights, extras = \
            self._createRandomizedNumpyArrays(len(origTV.genomeAnchor), origTV.startsAsNumpyArray(), \
                                              origTV.endsAsNumpyArray(), origTV.valsAsNumpyArray(), \
                                              origTV.strandsAsNumpyArray(), origTV.idsAsNumpyArray(), \
                                              origTV.edgesAsNumpyArray(), origTV.weightsAsNumpyArray(), \
                                              origTV.allExtrasAsDictOfNumpyArrays(), origTV.trackFormat, region)
        
        from gold.util.CommonFunctions import getClassName
        self._cachedTV = TrackView(origTV.genomeAnchor, \
                                   (starts + origTV.genomeAnchor.start if starts is not None else None), \
                                   (ends + origTV.genomeAnchor.start if ends is not None else None), \
                                   vals, strands, ids, edges, weights, origTV.borderHandling, origTV.allowOverlaps, extraLists=extras)
        assert self._trackFormatReq.isCompatibleWith(self._cachedTV.trackFormat), 'Incompatible track-format: '\
               + str(self._trackFormatReq) + ' VS ' + str(self._cachedTV.trackFormat)
        return self._cachedTV
        
    def _createRandomizedNumpyArrays(self, binLen, starts, ends, vals, strands, ids, edges, weights, extras, origTrackFormat, region):
        raise AbstractClassError
