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

from gold.origdata.GESourceWrapper import ListGESourceWrapper, ChrPausedGESourceWrapper
from gold.origdata.GEOverlapClusterer import GEOverlapClusterer
from gold.origdata.GEBoundingRegionElementCounter import GEBoundingRegionElementCounter
from gold.origdata.GenomeElementSource import GenomeElementSource, BoundingRegionTuple
from gold.util.CommonFunctions import flatten
from gold.util.CommonConstants import RESERVED_PREFIXES
from gold.util.CommonClasses import OrderedDefaultDict
from gold.util.CustomExceptions import AbstractClassError, NotSupportedError
from gold.track.TrackFormat import TrackFormat
from quick.util.CommonFunctions import isNan
from quick.util.GenomeInfo import GenomeInfo
from collections import OrderedDict, Iterable, defaultdict, deque
from itertools import chain
from functools import partial

class GESourceManager(object):
    def __init__(self, geSource):
        self._geSource = geSource
        
    def getAllOverlapRules(self):
        raise AbstractClassError
    
    def getAllChrs(self):
        raise AbstractClassError
        
    def getSortedGESource(self, chr, allowOverlaps):
        raise AbstractClassError
        
    def getSortedBoundingRegionTuples(self, allowOverlaps):
        raise AbstractClassError
    
    def getNumElements(self, chr, allowOverlaps):
        raise AbstractClassError
    
    def getValCategories(self, chr, allowOverlaps):
        raise AbstractClassError
    
    def getEdgeWeightCategories(self, chr, allowOverlaps):
        raise AbstractClassError

    def getMaxNumEdges(self, chr, allowOverlaps):
        raise AbstractClassError
        
    def getMaxStrLens(self, chr, allowOverlaps):
        raise AbstractClassError


def sortInChrBuckets(source, getChrFunc):
    import sys
    geBuckets = defaultdict(list)
    for i,el in enumerate(source):
        if getChrFunc(el) is not None:
            geBuckets[getChrFunc(el)].append(el.getCopy())
    
    sortedDict = OrderedDict()
    for chr in sorted(geBuckets.keys()):
        sortedDict[chr] = geBuckets[chr]
    return sortedDict
    #return OrderedDict(sorted(geBuckets.items(), key=lambda t: t[0]))


class StdGESourceManager(GESourceManager):
    def __new__(self, geSource):
        tf = TrackFormat.createInstanceFromGeSource(geSource)
        if tf.reprIsDense():
            return DenseStdGESourceManager.__new__(DenseStdGESourceManager, geSource)
        else:
            return SparseStdGESourceManager.__new__(SparseStdGESourceManager, geSource)

    def __init__(self, geSource):
        GESourceManager.__init__(self, geSource)
        self._tf = TrackFormat.createInstanceFromGeSource(geSource)
        self._numElements = defaultdict(partial(OrderedDefaultDict, int))
        self._valCategories = defaultdict(partial(OrderedDefaultDict, set))
        self._edgeWeightCategories = defaultdict(partial(OrderedDefaultDict, set))
        self._maxStrLens = defaultdict(partial(OrderedDefaultDict, \
            partial(self._initMaxStrLens, self._getMaxStrLensKeys())))
        self._maxNumEdges = defaultdict(partial(OrderedDefaultDict, int))

    def _getMaxStrLensKeys(self):
        prefixSet = set(self._geSource.getPrefixList())
            
        return (['val'] if 'val' in prefixSet and self._geSource.getValDataType() == 'S' else []) + \
               (['id'] if 'id' in prefixSet else []) + \
               (['edges'] if 'edges' in prefixSet else []) + \
               (['weights'] if 'weights' in prefixSet and self._geSource.getEdgeWeightDataType() == 'S' else []) + \
               [x for x in prefixSet if x not in RESERVED_PREFIXES]

    @staticmethod
    def _initMaxStrLens(keys):
        return dict([(x,0) for x in keys])
        
    def _updateTrackStatistics(self, el, chr, allowOverlaps, firstElInPartitionBoundingRegion=False):
        self._numElements[allowOverlaps][chr] += 1
        
        if firstElInPartitionBoundingRegion:
            return
        
        if self._tf.getValTypeName() == 'Category':
            self._valCategories[allowOverlaps][chr].add(el.val)
            
        if self._tf.getWeightTypeName() == 'Category':
            self._edgeWeightCategories[allowOverlaps][chr] |= set(el.weights)
    
        for prefix in self._maxStrLens[allowOverlaps][chr]:
            content = getattr(el, prefix)
            
            self._maxStrLens[allowOverlaps][chr][prefix] = \
                    max( self._maxStrLens[allowOverlaps][chr][prefix], \
                         max(1, len(content)) if isinstance(content, basestring) else \
                            max([1] + [len(x) for x in flatten(content)]) )
            
            if prefix == 'edges':
                self._maxNumEdges[allowOverlaps][chr] = max(self._maxNumEdges[allowOverlaps][chr], len(el.edges))

    def _calcTrackStatistics(self, chr, allowOverlaps):
        raise AbstractClassError

    def getNumElements(self, chr, allowOverlaps):
        assert allowOverlaps in self.getAllOverlapRules()
        self._calcTrackStatistics(chr, allowOverlaps)
        return self._numElements[allowOverlaps][chr]

    def getValCategories(self, chr, allowOverlaps):
        assert allowOverlaps in self.getAllOverlapRules()
        self._calcTrackStatistics(chr, allowOverlaps)
        return self._valCategories[allowOverlaps][chr]
    
    def getEdgeWeightCategories(self, chr, allowOverlaps):
        assert allowOverlaps in self.getAllOverlapRules()
        self._calcTrackStatistics(chr, allowOverlaps)
        return self._edgeWeightCategories[allowOverlaps][chr]

    def getMaxNumEdges(self, chr, allowOverlaps):
        assert allowOverlaps in self.getAllOverlapRules()
        self._calcTrackStatistics(chr, allowOverlaps)
        return self._maxNumEdges[allowOverlaps][chr]
        
    def getMaxStrLens(self, chr, allowOverlaps):
        assert allowOverlaps in self.getAllOverlapRules()
        self._calcTrackStatistics(chr, allowOverlaps)
        return self._maxStrLens[allowOverlaps][chr]


class SparseStdGESourceManager(StdGESourceManager):
    def __new__(cls, *args, **kwArgs):
        return object.__new__(cls, *args, **kwArgs)
    
    def __init__(self, geSource):
        StdGESourceManager.__init__(self, geSource)

        self._sortedGEBuckets = OrderedDict()
        self._sortedBRBuckets = OrderedDict()
        self._sortedAndClusteredGEBuckets = OrderedDefaultDict(list)
        self._sortedAndClusteredBRBuckets = OrderedDefaultDict(list)
        self._splittedAndProcessed = False
        
    def _splitAndProcess(self):
        #import pdb; pdb.set_trace()
        geBuckets = sortInChrBuckets(self._geSource, lambda el:el.chr)
        brBuckets = sortInChrBuckets(self._geSource.getBoundingRegionTuples(), lambda el:el.region.chr)
        
        if not self._geSource.isSorted():
            for chr in geBuckets:
                geBuckets[chr].sort(key=lambda el: [el.chr, el.start, el.end])
            for chr in brBuckets:
                brBuckets[chr].sort()
        
        self._sortedGEBuckets = geBuckets    
        self._sortedBRBuckets = brBuckets
            
        if self._geSource.hasNoOverlappingElements():
            self._sortedAndClusteredGEBuckets = self._sortedGEBuckets
            self._sortedAndClusteredBRBuckets = self._sortedBRBuckets
        else:
            chrList = self._sortedBRBuckets.keys() if len(self._sortedBRBuckets) > 0 else self._sortedGEBuckets.keys()
            for chr in chrList:
                if len(self._sortedBRBuckets) > 0:
                    geCount = 0
                    for i, br in enumerate(self._sortedBRBuckets[chr]):
                        if chr in self._sortedGEBuckets:
                            geClusteredList = self._sortedGEBuckets[chr][geCount:geCount+br.elCount]
                            geClusteredList = list( GEOverlapClusterer(ListGESourceWrapper \
                                                    (self._geSource, geClusteredList)) )
                        else:
                            geClusteredList = []
                        self._sortedAndClusteredGEBuckets[chr] += geClusteredList
                        self._sortedAndClusteredBRBuckets[chr].append(BoundingRegionTuple(br.region, len(geClusteredList)))
                        geCount += br.elCount
                else:
                    self._sortedAndClusteredGEBuckets[chr] = \
                        list( GEOverlapClusterer(ListGESourceWrapper(self._geSource, self._sortedGEBuckets[chr])) )
                    self._sortedAndClusteredBRBuckets[chr] = []
                    
    def _splitAndProcessIfNecessary(self):
        if not self._splittedAndProcessed:
            self._splitAndProcess()
            self._splittedAndProcessed = True
    
    def _getGEBuckets(self, allowOverlaps):
        self._splitAndProcessIfNecessary()
        return self._sortedGEBuckets if allowOverlaps else self._sortedAndClusteredGEBuckets

    def _getBRBuckets(self, allowOverlaps):
        self._splitAndProcessIfNecessary()
        return self._sortedBRBuckets if allowOverlaps else self._sortedAndClusteredBRBuckets
        
    def _calcTrackStatistics(self, chr, allowOverlaps):
        if chr not in self._numElements[allowOverlaps]:
            
            # In order to handle the first element of each bounding region for
            # genome partitions and step functions correctly
            tf = TrackFormat.createInstanceFromGeSource(self._geSource)
            if tf.isDense() and tf.isInterval():
                geList = self._getGEBuckets(allowOverlaps)[chr]
                prevEnd = 0
                for br in self._getBRBuckets(allowOverlaps)[chr]:
                    for i, el in enumerate(geList[prevEnd:prevEnd + br.elCount]):
                        self._updateTrackStatistics(el, chr, allowOverlaps, \
                            firstElInPartitionBoundingRegion=(i==0))
                    prevEnd += br.elCount
            else:
                for el in self._getGEBuckets(allowOverlaps)[chr]:
                    self._updateTrackStatistics(el, chr, allowOverlaps)

    def getAllOverlapRules(self):
        if self._tf.isDense() or self._geSource.hasNoOverlappingElements():
            return [False]
        return [True, False]
        
    def getAllChrs(self):
        return self._getGEBuckets(allowOverlaps=True).keys()
    
    def getSortedGESource(self, chr, allowOverlaps):
        assert chr in self.getAllChrs()
        return ListGESourceWrapper(self._geSource, self._getGEBuckets(allowOverlaps)[chr])
    
    def getSortedBoundingRegionTuples(self, allowOverlaps):
        from itertools import chain
        return list(chain(*self._getBRBuckets(allowOverlaps).values()))
    

class DenseStdGESourceManager(StdGESourceManager):
    def __new__(cls, *args, **kwArgs):
        return object.__new__(cls, *args, **kwArgs)
        
    def __init__(self, geSource):
        StdGESourceManager.__init__(self, geSource)
        self._maxValuesCalculated = False

    def getAllOverlapRules(self):
        return [False]
            
    def _calcTrackStatistics(self, chr='', allowOverlaps=False):
        if not self._maxValuesCalculated:
            for el in self._geSource:
                self._updateTrackStatistics(el, el.chr, False)
                
            self._maxValuesCalculated = True
    
    def getAllChrs(self):
        self._calcTrackStatistics()
        self._chrPausedGeSource = None
        return self._numElements[False].keys()
        
    def getSortedGESource(self, chr, allowOverlaps):
        assert allowOverlaps == False
        
        if self._chrPausedGeSource is None:
            self._chrPausedGeSource = ChrPausedGESourceWrapper(self._geSource)
            
        self._chrPausedGeSource.checkCurChr(chr)
        return self._chrPausedGeSource
        
    def getSortedBoundingRegionTuples(self, allowOverlaps):
        assert allowOverlaps == False
        return self._geSource.getBoundingRegionTuples()


class OneChrSortedNoOverlapsGESourceManager(GESourceManager):
    def __new__(self, geSource, brRegionList):
        tf = TrackFormat.createInstanceFromGeSource(geSource)
        if tf.reprIsDense():
            if tf.getValTypeName() == 'Number':
                return NumberFunctionOneChrSortedNoOverlapsGESourceManager.__new__\
                    (NumberFunctionOneChrSortedNoOverlapsGESourceManager, geSource, brRegionList)
            else:
                raise NotSupportedError
        else:
            return SparseOneChrSortedNoOverlapsGESourceManager.__new__\
                (SparseOneChrSortedNoOverlapsGESourceManager, geSource, brRegionList)

    def __init__(self, geSource, brRegionList):
        GESourceManager.__init__(self, geSource)
        assert len(brRegionList) > 0
        brTuples = self._calcTrackStatisticsAndCountElementsInBoundingRegions(brRegionList)
        self._brBuckets = sortInChrBuckets(brTuples, lambda brTuple:brTuple.region.chr)
        
    def _calcTrackStatisticsAndCountElementsInBoundingRegions(self):
        raise AbstractClassError
    
    def getAllOverlapRules(self):
        return [False]
        
    def getAllChrs(self):
        return self._brBuckets.keys()
        
    def getNumElements(self, chr, allowOverlaps):
        assert allowOverlaps == False
        return sum(brTuple.elCount for brTuple in self._brBuckets[chr])
            
    def getSortedGESource(self, chr, allowOverlaps):
        assert allowOverlaps == False
        return self._geSource

    def getSortedBoundingRegionTuples(self, allowOverlaps):
        assert allowOverlaps == False
        return [brTuple for brTuple in \
                chain.from_iterable(self._brBuckets.values())]

    
class SparseOneChrSortedNoOverlapsGESourceManager(OneChrSortedNoOverlapsGESourceManager, StdGESourceManager):
    def __new__(cls, *args, **kwArgs):
        return object.__new__(cls)
    
    def __init__(self, geSource, brRegionList):
        StdGESourceManager.__init__(self, geSource)
        OneChrSortedNoOverlapsGESourceManager.__init__(self, geSource, brRegionList)
        
    def _calcTrackStatistics(self, chr, allowOverlaps):
        pass
        
    def _calcTrackStatisticsAndCountElementsInBoundingRegions(self, brRegionList):
        brTuples = [BoundingRegionTuple(region, 0) for region in brRegionList]
        chrList = set([br.region.chr for br in brTuples])
            
        decoratedGESource = GEBoundingRegionElementCounter(self._geSource, brTuples)
        for el in decoratedGESource:
            self._updateTrackStatistics(el, el.chr, False)
        
        return decoratedGESource.getBoundingRegionTuples()
    
    def getNumElements(self, chr, allowOverlaps):
        return OneChrSortedNoOverlapsGESourceManager.getNumElements(self, chr, allowOverlaps)
        
    def getSortedBoundingRegionTuples(self, allowOverlaps):
        return OneChrSortedNoOverlapsGESourceManager.getSortedBoundingRegionTuples(self, allowOverlaps)

        
class NumberFunctionOneChrSortedNoOverlapsGESourceManager(OneChrSortedNoOverlapsGESourceManager):
    def __new__(cls, *args, **kwArgs):
        return object.__new__(cls)
    
    def _calcTrackStatisticsAndCountElementsInBoundingRegions(self, brRegionList):
        return [BoundingRegionTuple(region, len(region)) for region in brRegionList]
    
    def getMaxNumEdges(self, chr, allowOverlaps):
        assert allowOverlaps == False
        return 0
        
    def getMaxStrLens(self, chr, allowOverlaps):
        assert allowOverlaps == False
        return {}
        
    def getValCategories(self, chr, allowOverlaps):
        assert allowOverlaps == False
        return set()
        
    def getEdgeWeightCategories(self, chr, allowOverlaps):
        assert allowOverlaps == False
        return set()
