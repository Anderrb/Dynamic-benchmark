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

from gold.origdata.GESourceWrapper import GESourceWrapper
from gold.util.CustomExceptions import ShouldNotOccurError

class GEBoundingRegionElementCounter(GESourceWrapper):    
    def __init__(self, geSource, boundingRegionTuples):
        GESourceWrapper.__init__(self, geSource)
        self._brTuples = boundingRegionTuples
        self._finishedCounting = False
    
    def __iter__(self):
        self._geIter = self._geSource.__iter__()
        self._brIter = self._brTuples.__iter__()
        self._brTuples = []
        self._finishedCounting = False
        return self
    
    def next(self):
        try:
            el = self._geIter.next()
            
            while len(self._brTuples) == 0 or not self._contains(self._brTuples[-1].region, el):
                try:
                    self._getNextBrTuple()
                except StopIteration:
                    raise ShouldNotOccurError
            
            self._brTuples[-1].elCount += 1
            return el
        
        except StopIteration:
            try:
                while True:    
                    self._getNextBrTuple()
            except StopIteration:
                pass
            
            self._finishedCounting = True
            raise
            
    def _getNextBrTuple(self):
        self._brTuples.append( self._brIter.next() )
        self._brTuples[-1].elCount = 0
        
    def _contains(self, br, el):
        if [br.genome, br.chr] != [el.genome, el.chr]:
            return False            

        return False if (el.start is not None and br.start > el.start) or \
                        (el.end is not None and br.end < el.end) else True
        
    def getBoundingRegionTuples(self):
        assert self._finishedCounting
        return self._brTuples
