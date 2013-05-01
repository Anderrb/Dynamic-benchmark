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

#!/usr/bin/env python

import os
import sys
import traceback
#import pyximport; pyximport.install()

from gold.description.TrackInfo import TrackInfo, TrackInfoDataCollector
from gold.origdata.ChrMemmapFolderMerger import ChrMemmapFolderMerger
from gold.origdata.GEDependentAttributesHolder import GEDependentAttributesHolder
from gold.origdata.GESourceManager import StdGESourceManager, OneChrSortedNoOverlapsGESourceManager
from gold.origdata.GenomeElementSource import GenomeElementSource
from gold.origdata.PreProcessGeSourceJob import PreProcessGeSourceJob
from gold.origdata.PreProcessUtils import PreProcessUtils
from gold.util.CommonFunctions import createOrigPath, createDirPath, prettyPrintTrackName
from gold.util.CustomExceptions import NotSupportedError, AbstractClassError, Warning
from quick.application.ExternalTrackManager import ExternalTrackManager
from quick.application.ProcTrackOptions import ProcTrackOptions
from quick.aux.RenameTrack import renameTrack
from quick.origdata.OrigTrackFnSource import OrigTrackNameSource
from quick.util.CommonFunctions import reorderTrackNameListFromTopDownToBottomUp
from quick.util.GenomeInfo import GenomeInfo


class PreProcessTracksJob(object):
    VERSION = '1.0'
    
    PASS_ON_EXCEPTIONS = False
    
    def __init__(self, genome, username='', mode='Real', raiseIfAnyWarnings=False):
        self._genome = genome
        self._username = username
        self._mode = mode
        self._status = ''
        self._raiseIfAnyWarnings = raiseIfAnyWarnings
        self._warningTrackNames = []
    
    def process(self):
        atLeastOneFinalized = False
        for trackName in self._allTrackNames():
            assert trackName != ['']
            overlapRulesProcessedForTrackName = []
            
            try:
                trackName = self._renameTrackNameIfIllegal(trackName)
            
                for rawGESource in self._allGESources(trackName):
                    assert rawGESource.getGenome() is not None, 'Error: genome must be specified when preprocessing tracks.'
                    
                    geSourceManager = self._getGESourceManager(self._decorateGESource(rawGESource))
                    for allowOverlaps in geSourceManager.getAllOverlapRules():
                        self._status = 'Trying to prepare preprocessing for track "%s"' % ':'.join(trackName) + \
                                        ('(filename: "%s")' % rawGESource.getFileName() if rawGESource.hasOrigFile() else '')
                        if not PreProcessUtils.shouldPreProcessGESource(trackName, rawGESource, allowOverlaps):
                            break
                        
                        if self._shouldPreProcess():
                            PreProcessUtils.removeOutdatedPreProcessedFiles(trackName, rawGESource, allowOverlaps, self._mode)
                            
                            if self._shouldPrintProcessMessages() and allowOverlaps not in overlapRulesProcessedForTrackName:
                                self._printProcessTrackMessage(trackName, allowOverlaps)
                                overlapRulesProcessedForTrackName.append(allowOverlaps)
    
                            for chr in geSourceManager.getAllChrs():
                                self._status = 'Trying to sort geSource for chr: ' + chr
                                geSource = geSourceManager.getSortedGESource(chr, allowOverlaps)
                                
                                TrackInfoDataCollector(self._genome, trackName).updateFileSizeInfoForPreProc \
                                    (chr, allowOverlaps, \
                                     geSourceManager.getNumElements(chr, allowOverlaps), \
                                     geSourceManager.getValCategories(chr, allowOverlaps), \
                                     geSourceManager.getEdgeWeightCategories(chr, allowOverlaps), \
                                     geSourceManager.getMaxNumEdges(chr, allowOverlaps), \
                                     geSourceManager.getMaxStrLens(chr, allowOverlaps))
                                
                                self._status = 'Trying to preprocess geSource for chr: ' + chr
                                geSourceJob = PreProcessGeSourceJob(trackName, allowOverlaps, chr, geSource, self._mode)
                                geSourceJob.process()
                                
                                TrackInfoDataCollector(self._genome, trackName).updatePreProcDirtyStatus(geSourceJob.hasModifiedData())
                                
                                if self._raiseIfAnyWarnings and geSource.anyWarnings() and trackName not in self._warningTrackNames:
                                    self._warningTrackNames.append(trackName)

                            TrackInfoDataCollector(self._genome, trackName).appendBoundingRegionTuples(allowOverlaps, geSourceManager.getSortedBoundingRegionTuples(allowOverlaps))

                if self._shouldFinalize():
                    if TrackInfoDataCollector(self._genome, trackName).preProcIsDirty():
                        if self._mode == 'Real' and self._shouldMergeChrFolders():
                            for allowOverlaps in geSourceManager.getAllOverlapRules():
                                self._status = 'Trying to combine chromosome vectors into combined vectors.'
                                PreProcessUtils.createBoundingRegionShelve(self._genome, trackName, allowOverlaps)
                                ChrMemmapFolderMerger.merge(self._genome, trackName, allowOverlaps)
                                
                                self._status = 'Trying to remove chromosome folders'
                                PreProcessUtils.removeChrMemmapFolders(self._genome, trackName, allowOverlaps)
                                
                        for allowOverlaps in geSourceManager.getAllOverlapRules():
                            self._status = 'Trying to check whether 3D data is correct'
                            PreProcessUtils.checkIfEdgeIdsExist(self._genome, trackName, allowOverlaps)
                            PreProcessUtils.checkUndirectedEdges(self._genome, trackName, allowOverlaps)
                        
                        self._status = 'Trying to finalize.'
                        TrackInfoDataCollector(self._genome, trackName).finalize(self._username, self._shouldPrintProcessMessages())
                        if not atLeastOneFinalized:
                            atLeastOneFinalized = True
                    else:
                        TrackInfoDataCollector(self._genome, trackName).removeEntryFromShelve()                    

            except NotSupportedError, e:
                TrackInfoDataCollector(self._genome, trackName).removeEntryFromShelve()
                if self.PASS_ON_EXCEPTIONS:
                    raise
                else:
                    self._printExceptionMsg(e, trackName, Error=False)
            except Exception, e:
                TrackInfoDataCollector(self._genome, trackName).removeEntryFromShelve()
                if self.PASS_ON_EXCEPTIONS:
                    raise
                else:
                    self._printExceptionMsg(e, trackName, Error=True)                
                
            self._calcAndStoreSubTrackCount(trackName)
            
        if self._raiseIfAnyWarnings and len(self._warningTrackNames) > 0:
            raise Warning('Warnings occurred in the following tracks: ' + \
                          ', '.join(prettyPrintTrackName(tn) for tn in self._warningTrackNames))
        return atLeastOneFinalized

    def _allTrackNames(self):
        raise AbstractClassError
    
    def _allGESources(self, trackName):
        raise AbstractClassError
        
    def _decorateGESource(self, geSource):
        return GEDependentAttributesHolder(geSource)
        
    def _getGESourceManager(self, rawGESource):
        return StdGESourceManager(rawGESource)
        
    def _shouldPreProcess(self):
        return True
        
    def _shouldPrintProcessMessages(self):
        return True
        
    def _shouldFinalize(self):
        return True
        
    def _shouldMergeChrFolders(self):
        return True
        
    def _renameTrackNameIfIllegal(self, trackName):
        from gold.description.AnalysisDefHandler import replaceIllegalElements
        legalTrackName = [replaceIllegalElements(x) for x in trackName]
        
        if legalTrackName != trackName and os.path.exists(createDirPath(trackName, self._genome)):
            renameTrack(self._genome, trackName, legalTrackName)
            
        return legalTrackName
        
    def _updateAllChrs(self, allChrs, chrList, allowOverlaps):
        if not allowOverlaps in allChrs:
            allChrs[allowOverlaps] = set()
        assert all(chr not in allChrs[allowOverlaps] for chr in chrList), \
            'Error: chromosome %s already preprocessed for previous GenomeElementSource (this may be because of elements of the same chromosome is found in different files).' % chr
        allChrs[allowOverlaps].update(set(chrList))
    
    def _calcAndStoreSubTrackCount(self, trackName):
        ti = TrackInfo(self._genome, trackName)
        if ti.isValid():
            ti.subTrackCount = 1
            ti.store()
    
    def _printProcessTrackMessage(self, trackName, allowOverlaps):
        if self._mode == 'Simulated':
            print "Would now have processed track: '%s' with allowOverlaps: %s in a real run." % (':'.join(trackName), allowOverlaps)
        elif self._mode == 'UpdateMeta':
            print "Only updating meta info based on track: '%s' with allowOverlaps: %s" % (':'.join(trackName), allowOverlaps)
        elif self._mode == 'Real':
            print "Processing track: '%s' with allowOverlaps: %s" % (':'.join(trackName), allowOverlaps)
    
    def _printExceptionMsg(self, e, trackName, Error=False):
        print (os.linesep + '--- BEGIN ERROR ---' + os.linesep *2 if Error else 'Warning! ') + \
            "Could not pre-process track '%s'." % ':'.join(trackName)
        print "Status: %s" % self._status
        #print e.__class__.__name__ + ':', e
        if Error:
            traceback.print_exc(file=sys.stdout)
            print os.linesep + '--- END ERROR ---' + os.linesep

class PreProcessAllTracksJob(PreProcessTracksJob):
    def __init__(self, genome, trackNameFilter=[], username='', mergeChrFolders=True, **kwArgs):
        PreProcessTracksJob.__init__(self, genome, username=username, **kwArgs)
        self._trackNameFilter = trackNameFilter
        self._mergeChrFolders = mergeChrFolders
        
    def _allTrackNames(self):
        avoidLiterature = len(self._trackNameFilter) == 0 or (self._trackNameFilter != GenomeInfo.getLiteratureTrackName(self._genome))
        trackSource = OrigTrackNameSource(self._genome, self._trackNameFilter, avoidLiterature)
        return reorderTrackNameListFromTopDownToBottomUp(trackSource)
        
    def _allGESources(self, trackName):
        baseDir = createOrigPath(self._genome, trackName)

        self._status = 'Trying os.listdir on: ' + baseDir
        for relFn in sorted(os.listdir( baseDir )):
            fn = os.sep.join([baseDir, relFn])

            self._status = 'Checking file: ' + fn
            if os.path.isdir(fn):
                continue
            
            fnPart = os.path.split(fn)[-1]
            if fnPart[0] in ['.','_','#'] or fnPart[-1] in ['~','#']: #to avoid hidden files..
                continue

            self._status = 'Trying to create geSource from fn: ' + fn
            yield GenomeElementSource(fn, self._genome, forPreProcessor=True)
    
    def _calcAndStoreSubTrackCount(self, trackName):
        ti = TrackInfo(self._genome, trackName)
        trackCount = 0
        for subTrackName in ProcTrackOptions.getSubtypes(self._genome, trackName, True):
            subTrackCount = TrackInfo(self._genome, trackName + [subTrackName]).subTrackCount
            if subTrackCount:
                trackCount += subTrackCount
        if ti.isValid():
            trackCount += 1
        ti.subTrackCount = trackCount
        ti.store()
    
    def _shouldMergeChrFolders(self):
        return self._mergeChrFolders
        
    
class PreProcessExternalTrackJob(PreProcessTracksJob):
    PASS_ON_EXCEPTIONS = True

    def __init__(self, genome, fullFn, extTrackName, fileSuffix, **kwArgs):
        PreProcessTracksJob.__init__(self, genome, **kwArgs)
        self._fullFn = fullFn
        self._extTrackName = extTrackName
        self._fileSuffix = fileSuffix
        
    def _allTrackNames(self):
        return [self._extTrackName]
        
    def _allGESources(self, trackName):
        return [ExternalTrackManager.getGESource(self._fullFn, self._fileSuffix, \
                                                 self._extTrackName, self._genome, printWarnings=True)]

class PreProcessCustomTrackJob(PreProcessTracksJob):
    PASS_ON_EXCEPTIONS = True

    def __init__(self, genome, trackName, regionList, getGeSourceCallBackFunc, username='', \
                 preProcess=True, finalize=True, mergeChrFolders=True, **callBackArgs):
        PreProcessTracksJob.__init__(self, genome, username=username)
        self._trackName = trackName
        assert len(regionList) > 0
        self._regionList = regionList
        self._getGeSourceCallBackFunc = getGeSourceCallBackFunc
        self._callBackArgs = callBackArgs
        self._preProcess = preProcess
        self._finalize = finalize
        self._mergeChrFolders = mergeChrFolders
        
    def _allTrackNames(self):
        return [self._trackName]
        
    def _allGESources(self, trackName):
        regionList = self._regionList if self._preProcess else [self._regionList[0]]
        for region in regionList:
            yield self._getGeSourceCallBackFunc(self._genome, self._trackName, region, **self._callBackArgs)
    
    def _decorateGESource(self, geSource):
        return geSource
    
    def _getGESourceManager(self, rawGESource):
        return OneChrSortedNoOverlapsGESourceManager(rawGESource, self._regionList)
        
    def _shouldPreProcess(self):
        return self._preProcess
        
    def _shouldPrintProcessMessages(self):
        return False

    def _shouldFinalize(self):
        return self._finalize
    
    def _shouldMergeChrFolders(self):
        return self._mergeChrFolders
    

if __name__ == "__main__":
    if not len(sys.argv) in [2,3,4]:
        print 'Syntax: python PreProcessTracksJob.py genome [trackName:subType] [mode=Real/Simulated/UpdateMeta]'
        sys.exit(0)
        
    if len(sys.argv) == 2:
        tn = []
        mode = 'Real'
    elif len(sys.argv) == 3:
        if sys.argv[2] in ['Real', 'Simulated', 'UpdateMeta']:
            tn = []
            mode = sys.argv[2]
        else:
            tn = sys.argv[2].split(':')
            mode = 'Real'
    else:
        tn = sys.argv[2].split(':')
        mode = sys.argv[3]

    assert mode in ['Real', 'Simulated', 'UpdateMeta']
    PreProcessAllTracksJob(sys.argv[1], tn, username='', mode=mode).process()
