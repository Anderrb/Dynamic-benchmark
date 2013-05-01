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

from gold.util.CustomExceptions import InvalidFormatError, ShouldNotOccurError, AbstractClassError
from gold.origdata.GenomeElementSource import GenomeElementSource
from copy import copy

class GESourceWrapper(object):
    def __init__(self, geSource):
        self._geSource = geSource
    
    def getTrackName(self):
        return self._geSource.getTrackName()
    
    def getGenome(self):
        return self._geSource.getGenome()
        
    def getFileName(self):
        return self._geSource.getFileName()
        
    def getFileSuffix(self):
        return self._geSource.getFileSuffix()
        
    def isExternal(self):
        return self._geSource.isExternal()
        
    def hasOrigFile(self):
        return self._geSource.hasOrigFile()
        
    def isSliceSource(self):
        return self._geSource.isSliceSource()
        
    def addsStartElementToDenseIntervals(self):
        return self._geSource.addsStartElementToDenseIntervals()
        
    def isSorted(self):
        return self._geSource.isSorted()
        
    def hasCircularElements(self):
        return self._geSource.hasCircularElements()
        
    def getFixedLength(self):
        return self._geSource.getFixedLength()
        
    def getFixedGapSize(self):
        return self._geSource.getFixedGapSize()
        
    def hasNoOverlappingElements(self):
        return self._geSource.hasNoOverlappingElements()
        
    def hasUndirectedEdges(self):
        return self._geSource.hasUndirectedEdges()
        
    def inputIsOneIndexed(self):
        return self._geSource.inputIsOneIndexed()
    
    def inputIsEndInclusive(self):
        return self._geSource.inputIsEndInclusive()
    
    def hasBoundingRegionTuples(self):
        return len(self.getBoundingRegionTuples()) > 0
    
    def getBoundingRegionTuples(self):
        return self._geSource.getBoundingRegionTuples()
    
    def parseFirstDataLine(self):
        return self._geSource.parseFirstDataLine()
    
    def getPrefixList(self):
        return self._geSource.getPrefixList()

    def getValDataType(self):
        return self._geSource.getValDataType()

    def getValDim(self):
        return self._geSource.getValDim()
        
    def getEdgeWeightDataType(self):
        return self._geSource.getEdgeWeightDataType()

    def getEdgeWeightDim(self):
        return self._geSource.getEdgeWeightDim()
        
    def getVersion(self):
        return self._geSource.getVersion()
        
    def anyWarnings(self):
        return self._geSource.anyWarnings()
        
    def getLastWarning(self):
        return self._geSource.getLastWarning()
    
    genome = property(getGenome)
    
class ListGESourceWrapper(GESourceWrapper):
    def __init__(self, geSource, geList, brList=[]):
        GESourceWrapper.__init__(self, geSource)
        self._geList = geList
        self._brList = brList

    def __iter__(self):
        self._geIter = self._geList.__iter__()
        return copy(self)
        
    def next(self):
        return self._geIter.next()
            
    def getBoundingRegionTuples(self):
        return self._brList
        
class SortedListGESourceWrapper(ListGESourceWrapper):
    def isSorted(self):
        return True
        
class PrefixListGESourceWrapper(ListGESourceWrapper):
    def __init__(self, geSource, geList, brList, prefixList):
        ListGESourceWrapper.__init__(self, geSource, geList, brList)
        self._prefixList = prefixList
        
    def getPrefixList(self):
        return self._prefixList
        
class ElementModifierGESourceWrapper(GESourceWrapper, GenomeElementSource):
    def __new__(cls, *args, **kwArgs):
        return object.__new__(cls)
        
    def __init__(self, geSource, genome=None):
        from gold.origdata.GEDependentAttributesHolder import GEDependentAttributesHolder
        geSource = GEDependentAttributesHolder(geSource)
        GESourceWrapper.__init__(self, geSource)
        GenomeElementSource.__init__(self, '', genome=genome)
        
        for ge in geSource:
            pass
        
    def __iter__(self):
        self._brtAndGeIter = self._brtAndGeIterator()
        self._iter()
        return self
        
    def _brtAndGeIterator(self):
        from gold.origdata.GEDependentAttributesHolder import iterateOverBRTuplesWithContainedGEs
        brtAndGeIter = iterateOverBRTuplesWithContainedGEs(self._geSource)
        
        while True:
            try:
                brt, geList = brtAndGeIter.next()
            except StopIteration:
                return
            
            for i, ge in enumerate(geList):
                yield brt, ge, i

    def _iter(self):
        pass
        
    def next(self):
        return self._next(*self._brtAndGeIter.next())
        
    def _next(self, ge):
        raise AbstractClassError

    def parseFirstDataLine(self):
        return GenomeElementSource.parseFirstDataLine(self)
        
    def getPrefixList(self):
        return GenomeElementSource.getPrefixList(self)

    def getBoundingRegionTuples(self):
        return self._geSource.getBoundingRegionTuples()

    def inputIsOneIndexed(self):
        return self._geSource.inputIsOneIndexed()
    
    def inputIsEndInclusive(self):
        return self._geSource.inputIsOneIndexed()

class ChrPausedGESourceWrapper(GESourceWrapper):
    def __init__(self, geSource):
        GESourceWrapper.__init__(self, geSource)
        self._geIter = self._geSource.__iter__()
        #self._curEl = deepcopy(self._geIter.next())
        self._curEl = self._geIter.next().getCopy()
        self._chrList = [self._curEl.chr]
        self._finished = False
    
    def __iter__(self):
        try:
            while not self._finished:
                yield self._curEl
                self._curEl = self._geIter.next()
                if self._curEl.chr != self._chrList[-1]:
                    if self._curEl.chr in self._chrList:
                        raise InvalidFormatError('Error: chromosome %s has been previously encountered. Dense datasets must not skip back and forth between chromosomes.' % self._curEl.chr)
                    self._chrList.append(self._curEl.chr)
                    break
            
        except StopIteration:
            self._finished = True
            raise
    
    def checkCurChr(self, chr):
        if chr != self._chrList[-1]:
            raise ShouldNotOccurError('Error: current chromosome %s is not what is expected (%s). This should not have happened.' % (self._chrList[-1], chr))