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

from copy import copy
import os
import sys
from zipfile import ZipFile
from itertools import chain
from gold.description.TrackInfo import TrackInfo
from gold.track.GenomeRegion import GenomeRegion
from gold.track.Track import Track
from gold.track.TrackFormat import TrackFormatReq
from gold.util.CommonFunctions import getStringFromStrand, parseRegSpec, parseTrackNameSpec, createDirPath
from gold.util.CustomExceptions import NotSupportedError, ShouldNotOccurError
from quick.util.CommonFunctions import ensurePathExists
from quick.util.GenomeInfo import GenomeInfo

class TrackExtractor:
    ALLOW_OVERLAPS_TRUE_TEXT = 'possibly overlapping'
    ALLOW_OVERLAPS_FALSE_TEXT = 'any overlaps clustered'
    ORIG_FILE_FORMAT_TEXT = 'original file format'
    DEFAULT_FILE_FORMAT_NAME = 'gtrack'
    
    @classmethod
    def getAttrsFromExtractionFormat(cls, extractionFormat):
        asOriginal = extractionFormat.lower().startswith(cls.ORIG_FILE_FORMAT_TEXT)
        if asOriginal:
            fileFormatName = cls.DEFAULT_FILE_FORMAT_NAME
            allowOverlaps = True
        else:
            fileFormatName = cls.getFileFormatNameFromExtractionFormat(extractionFormat)
            allowOverlaps = extractionFormat.lower().endswith(cls.ALLOW_OVERLAPS_TRUE_TEXT)

        return fileFormatName, asOriginal, allowOverlaps
    
    @classmethod
    def getFileFormatText(cls, fileFormatName):
        return '(format: %s)' % fileFormatName
        
    @classmethod
    def getFileSuffixText(cls, fileFormatName):
        return '(suffix: %s)' % fileFormatName
        
    @classmethod
    def getFileFormatNameFromExtractionFormat(cls, extractionFormat):
        formatIndexStart = extractionFormat.find('(format: ')
        formatIndexEnd = extractionFormat.find(')')
        if formatIndexStart == -1 or formatIndexEnd == -1:
            raise ShouldNotOccurError()
        return extractionFormat[formatIndexStart + 9 : formatIndexEnd]
        
    @classmethod
    def getFileSuffixFromExtractionFormat(cls, extractionFormat):
        formatIndexStart = extractionFormat.find('(suffix: ')
        formatIndexEnd = extractionFormat.find(')')
        if formatIndexStart == -1 or formatIndexEnd == -1:
            raise ShouldNotOccurError()
        return extractionFormat[formatIndexStart + 9 : formatIndexEnd]
    
    @classmethod
    def extract(cls, trackName, regionList, fn, fileFormatName=DEFAULT_FILE_FORMAT_NAME, globalCoords=True, \
                addSuffix=False, asOriginal=False, allowOverlaps=False, ignoreEmpty=False):
        from gold.origdata.TrackGenomeElementSource import TrackGenomeElementSource
        from gold.origdata.FileFormatComposer import getComposerClsFromFileFormatName, getComposerClsFromFileSuffix
        
        assert len(regionList) > 0
        for region in regionList:
            genome = region.genome
            break
        
        #To silently extract correctly if track type is dense
        if allowOverlaps:
            allowOverlaps = os.path.exists(createDirPath(trackName, genome, allowOverlaps=True))
            
        trackGESource = TrackGenomeElementSource(genome, trackName, regionList, globalCoords=globalCoords, \
                                                 allowOverlaps=allowOverlaps, printWarnings=False)
        
        composerCls = None
        if asOriginal:
            ti = TrackInfo(genome, trackName)
            if ti.fileType != '':
                try:
                    composerCls = getComposerClsFromFileSuffix(ti.fileType)
                except:
                    pass
        
        if composerCls is None:
            composerCls = getComposerClsFromFileFormatName(fileFormatName)

        if addSuffix:
            fn = os.path.splitext(fn)[0] + '.' + composerCls.getDefaultFileNameSuffix()
        
        composer = composerCls(trackGESource)
        ok = composer.composeToFile(fn, ignoreEmpty=ignoreEmpty)
        
        if ok:
            return fn
    
    #
    # Note: asOriginal=True trumps fileFormatName for specifying output file format
    #
    @classmethod
    def extractManyToRegionDirs(cls, trackNameList, regionList, baseDir, fileFormatName=DEFAULT_FILE_FORMAT_NAME, \
                                globalCoords=False, asOriginal=False, allowOverlaps=False, ignoreEmpty=True):
        for trackName in trackNameList:
            for region in regionList:
                fn = baseDir + os.sep + \
                    str(region).replace(':','_') + os.sep + \
                    '_'.join(trackName)
                cls.extract(trackName, [region], fn, fileFormatName=fileFormatName, globalCoords=globalCoords, \
                            addSuffix=True, asOriginal=asOriginal, allowOverlaps=allowOverlaps, \
                            ignoreEmpty=ignoreEmpty)
                
    @classmethod
    def extractOneTrackManyToRegionFilesInOneZipFile(cls, trackName, regionList, zipFn, fileFormatName=DEFAULT_FILE_FORMAT_NAME, \
                                                     globalCoords=False, asOriginal=False, allowOverlaps=False, \
                                                     ignoreEmpty=True):
        ensurePathExists(zipFn)
        zipFile = ZipFile(zipFn, 'w')
        for region in regionList:
            fn = os.path.dirname(zipFn) + os.sep + str(region).replace(':','_')
            okFn = cls.extract(trackName, [region], fn, fileFormatName=fileFormatName, \
                               globalCoords=globalCoords, addSuffix=True, asOriginal=asOriginal, \
                               allowOverlaps=allowOverlaps, ignoreEmpty=ignoreEmpty)
            if okFn:
                zipFile.write(okFn, os.path.basename(okFn))
                os.remove(okFn)
        zipFile.close()

    @classmethod
    def extractOneTrackManyRegsToOneFile(cls, trackName, regionList, fn, fileFormatName=DEFAULT_FILE_FORMAT_NAME, \
                                         globalCoords=False, asOriginal=False, allowOverlaps=False):
        cls.extract(trackName, regionList, fn, fileFormatName=fileFormatName, globalCoords=globalCoords, \
                    addSuffix=False, asOriginal=asOriginal, allowOverlaps=allowOverlaps)
        
    @classmethod
    def extractManyToOneDir(cls, trackNameList, regionList, baseDir, fileFormatName=DEFAULT_FILE_FORMAT_NAME, \
                            globalCoords=False, asOriginal=False, allowOverlaps=False):
        for trackName in trackNameList:
            fn = baseDir + os.sep + '_'.join(trackName)
            cls.extractOneTrackManyRegsToOneFile(trackName, regionList, fn, fileFormatName=fileFormatName,
                                                 globalCoords=globalCoords, asOriginal=asOriginal, \
                                                 allowOverlaps=allowOverlaps)
                
if __name__ == "__main__":
    if len(sys.argv) not in [4, 5]:
        print 'Syntax: python TrackExtractor.py trackName:subtype genome:chr:start-end asOriginal [filename]'
        sys.exit(0)
        
    trackName = parseTrackNameSpec(sys.argv[1])
    regions = parseRegSpec(sys.argv[2])
    assert len(regions) == 1
    asOriginal = eval(sys.argv[3])
        
    fn = sys.argv[4] if len(sys.argv) == 5 else None
    
    TrackExtractor.extract(trackName, regions[0], fn, asOriginal=asOriginal)
