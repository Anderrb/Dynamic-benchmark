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

from gold.util.CommonFunctions import parseRegSpec, parseShortenedSizeSpec
from gold.util.CustomExceptions import ShouldNotOccurError
from config.Config import DEFAULT_GENOME
from gold.origdata.GenomeElementSource import GenomeElementSource
from gold.origdata.BedGenomeElementSource import BedGenomeElementSource, BedCategoryGenomeElementSource
from gold.origdata.WigGenomeElementSource import WigGenomeElementSource
from gold.origdata.BedGraphGenomeElementSource import BedGraphGenomeElementSource
from gold.origdata.GtrackGenomeElementSource import GtrackGenomeElementSource
from quick.application.AutoBinner import AutoBinner
from gold.origdata.GenomeElementSorter import GenomeElementSorter
from gold.application.DataTypes import getSupportedFileSuffixesForBinning
    
class UserBinSource(object):
    '''Possible definitions of UserBinSource, based on (regSpec,binSpec)-tuple:
    ('file',fn) where instead of 'file', a more specific filetype such as 'bed' could be specified
    (chrReg,binSize) where chrReg is a Region specification as in UCSC Genome browser (string), or '*' to denote whole genome, and where binSize is a number specifying length of each bin that the region should be split into.
    '''
    def __new__(cls, regSpec, binSpec, genome=None, categoryFilterList=None, strictMatch=True): #,fileType):
        if regSpec in ['file'] + getSupportedFileSuffixesForBinning():
            #if fileType != 'bed':
            #    raise NotImplementedError
            if genome is None:
                genome = DEFAULT_GENOME
            
            from gold.origdata.GenomeElementSource import GenomeElementSource
            if regSpec == 'file':
                geSource = GenomeElementSource(binSpec, genome=genome)
            else:
                geSource = GenomeElementSource(binSpec, genome=genome, suffix=regSpec)
            
            if categoryFilterList is not None:
                from gold.origdata.GECategoryFilter import GECategoryFilter
                geSource = GECategoryFilter(geSource, categoryFilterList, strict=strictMatch)
            return cls._applyEnvelope(geSource)
        else:
            if binSpec == '*':
                binSize = None
            else:
                binSize = parseShortenedSizeSpec(binSpec)
            
            from quick.application.AutoBinner import AutoBinner
            return AutoBinner(parseRegSpec(regSpec, genome), binSize)
    
    @staticmethod
    def _applyEnvelope(geSource):
        from quick.origdata.RegionBoundaryFilter import RegionBoundaryFilter
        from gold.origdata.GEOverlapClusterer import GEOverlapClusterer
        return RegionBoundaryFilter(GEOverlapClusterer(GenomeElementSorter(geSource)), GlobalBinSource(geSource.genome))

class UnBoundedUserBinSource(UserBinSource):
    @staticmethod
    def _applyEnvelope(geSource):
        from gold.origdata.GEOverlapClusterer import GEOverlapClusterer
        return GEOverlapClusterer(GenomeElementSorter(geSource))

class UnBoundedUnClusteredUserBinSource(UserBinSource):
    @staticmethod
    def _applyEnvelope(geSource):
        return GenomeElementSorter(geSource)
        
class ValuesStrippedUserBinSource(UserBinSource):
    @staticmethod
    def _applyEnvelope(geSource):
        from gold.origdata.GEMarkRemover import GEMarkRemover
        return GenomeElementSorter(GEMarkRemover(geSource))

class BoundedUnClusteredUserBinSource(UserBinSource):
    @staticmethod
    def _applyEnvelope(geSource):
        from quick.origdata.RegionBoundaryFilter import RegionBoundaryFilter
        return RegionBoundaryFilter(GenomeElementSorter(geSource), GlobalBinSource(geSource.genome) )

class UnfilteredUserBinSource(UserBinSource):
    @staticmethod
    def _applyEnvelope(geSource):
        return geSource
    
class GlobalBinSource(object):
    def __new__(cls, genome):
        return UserBinSource(genome+':*','*')
    
class MinimalBinSource(object):
    def __new__(cls, genome):
        from gold.track.GenomeRegion import GenomeRegion
        from quick.util.GenomeInfo import GenomeInfo
        return [GenomeRegion(genome, GenomeInfo.getChrList(genome)[0], 0, 1)]
