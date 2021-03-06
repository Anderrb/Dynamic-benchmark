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

import numpy
from gold.track.RandomizedTrack import RandomizedTrack
from gold.util.CustomExceptions import IncompatibleTracksError

class ShuffledMarksTrack(RandomizedTrack):    
    def _checkTrackFormat(self, origTV):
        if not origTV.trackFormat.isValued():
            raise IncompatibleTracksError(str(origTV.trackFormat))
        
    def _createRandomizedNumpyArrays(self, binLen, starts, ends, vals, strands, ids, edges, weights, extras, origTrackFormat, region):
        #isPointTrack = (not origTrackFormat.isInterval())

        #if len(vals)==0:
        #    assert len(ends)==len(starts)==0
        #    return starts, (ends if not isPointTrack else None), vals, strands
            
        newVals = numpy.copy(vals)
        numpy.random.shuffle(newVals)        
        
        #return starts,(ends if not isPointTrack else None),newVals,strands
        return starts, ends, newVals, strands, ids, edges, weights, extras
    
 
