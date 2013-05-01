import os
import sys
import shutil
import numpy
from config.Config import PROCESSED_DATA_PATH
from gold.description.TrackInfo import TrackInfo, TrackInfoDataCollector
from gold.description.TrackInfo import TrackInfoDataCollector
from gold.origdata.GenomeElement import GenomeElement
from gold.origdata.GenomeElementSource import BoundingRegionTuple
from gold.track.BoundingRegionShelve import BoundingRegionShelve
from gold.track.CommonMemmapFunctions import findEmptyVal
from gold.track.GenomeRegion import GenomeRegion
from gold.track.TrackFormat import TrackFormat
from gold.track.TrackSource import TrackSource
from gold.util.CommonConstants import RESERVED_PREFIXES
from gold.util.CommonFunctions import createDirPath
from gold.util.CustomExceptions import InvalidFormatError, ShouldNotOccurError
from quick.util.GenomeInfo import GenomeInfo

class PreProcessUtils(object):
    @staticmethod
    def shouldPreProcessGESource(trackName, geSource, allowOverlaps):
        storedInfo = TrackInfo(geSource.getGenome(), trackName)
        
        validFilesExist = PreProcessUtils.preProcFilesExist(trackName, geSource, allowOverlaps) and \
            storedInfo.isValid()
        
        if not geSource.hasOrigFile():
            return False if validFilesExist or geSource.isExternal() else True
        
        storedAsAccordingToGeSource = \
            (PreProcessUtils.constructId(geSource) == storedInfo.id and \
             geSource.getVersion() == storedInfo.preProcVersion)
        
        #from gold.application.LogSetup import logMessage
        #logMessage(geSource.getGenome())
        #logMessage(':'.join(trackName))
        #logMessage('%s %s %s %s %s' % (PreProcessUtils.preProcFilesExist(trackName, geSource, allowOverlaps), \
        #                               storedInfo.isValid(), \
        #                               geSource.hasOrigFile(), \
        #                               PreProcessUtils.constructId(geSource) == storedInfo.id, \
        #                               geSource.getVersion() == storedInfo.preProcVersion))
        
        return not (validFilesExist and storedAsAccordingToGeSource)
    
    @staticmethod
    def preProcFilesExist(trackName, geSource, allowOverlaps):
        genome = geSource.getGenome()
        
        preProcFilesExist = TrackInfoDataCollector(genome, trackName).preProcFilesExist(allowOverlaps)
        if preProcFilesExist is None:
            dirPath = createDirPath(trackName, genome, allowOverlaps=allowOverlaps)
            if BoundingRegionShelve(genome, trackName, allowOverlaps).fileExists():
                preProcFilesExist = \
                    any( fn.split('.')[0] in ['start', 'end', 'val', 'edges'] \
                         for fn in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, fn)) )
            else:
                preProcFilesExist = os.path.exists(dirPath) and \
                    any( not PreProcessUtils._isSubTrackDirectory(os.path.join(dirPath, fn)) \
                         for fn in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, fn)) )
            TrackInfoDataCollector(genome, trackName).updatePreProcFilesExistFlag(allowOverlaps, preProcFilesExist)
        return preProcFilesExist
    
    @staticmethod
    def _isSubTrackDirectory(dirPath):
        return any(os.path.isdir(os.path.join(dirPath, subFn)) or \
                   os.path.islink(os.path.join(dirPath, subFn)) \
                   for subFn in os.listdir(dirPath))
    @staticmethod
    def constructId(geSource):
        from gold.origdata.PreProcessTracksJob import PreProcessTracksJob
        if geSource.hasOrigFile():
            origPath = os.path.dirname(geSource.getFileName()) if not geSource.isExternal() else geSource.getFileName()
            return TrackInfo.constructIdFromPath(geSource.getGenome(), origPath, \
                                                 geSource.getVersion(), PreProcessTracksJob.VERSION)
        else:
            return None
        
    @staticmethod
    def removeOutdatedPreProcessedFiles(trackName, geSource, allowOverlaps, mode):
        genome = geSource.getGenome()
    
        if PreProcessUtils.preProcFilesExist(trackName, geSource, allowOverlaps) and not \
            TrackInfoDataCollector(genome, trackName).hasRemovedPreProcFiles(allowOverlaps):
                dirPath = createDirPath(trackName, genome, allowOverlaps=allowOverlaps)
                
                assert( dirPath.startswith(PROCESSED_DATA_PATH) )
                if mode == 'Real':
                    print 'Removing outdated preprocessed data: ', dirPath
                    for fn in os.listdir(dirPath):
                        fullFn = os.path.join(dirPath, fn)
                        if os.path.isfile(fullFn):
                            os.unlink(fullFn)
                        if os.path.isdir(fullFn):
                            if not PreProcessUtils._isSubTrackDirectory(fullFn):
                                shutil.rmtree(fullFn)
                else:
                    print 'Would now have removed outdated preprocessed data if real run: ', dirPath
                
                TrackInfoDataCollector(genome, trackName).updateRemovedPreProcFilesFlag(allowOverlaps, True)
        
        if mode == 'Real':
            ti = TrackInfo(genome, trackName)
            ti.resetTimeOfPreProcessing()
                
    @staticmethod
    def createBoundingRegionShelve(genome, trackName, allowOverlaps):
        collector = TrackInfoDataCollector(genome, trackName)
        geChrList = collector.getPreProcessedChrs(allowOverlaps)

        boundingRegionTuples = [x for x in collector.getBoundingRegionTuples(allowOverlaps) if x.region.chr is not None]
        
        if len(boundingRegionTuples) == 0:
            boundingRegionTuples = [BoundingRegionTuple( \
                                     GenomeRegion(chr=chr, start=0, end=GenomeInfo.getChrLen(genome, chr)), \
                                     collector.getNumElements(chr, allowOverlaps) ) \
                                    for chr in geChrList]
        brShelve = BoundingRegionShelve(genome, trackName, allowOverlaps)
        brShelve.storeBoundingRegions(boundingRegionTuples, geChrList, not collector.getTrackFormat().reprIsDense())
        
        boundingRegionChrs = set([br.region.chr for br in boundingRegionTuples])
        for chr in boundingRegionChrs | set(geChrList):
            if brShelve.getTotalElementCount(chr) != collector.getNumElements(chr, allowOverlaps):
                raise ShouldNotOccurError("Error: The total element count for all bounding regions of chromosome '%s' is not equal to the number of genome elements of that chromosome. %s != %s" % \
                                          (chr, brShelve.getTotalElementCount(chr), collector.getNumElements(chr, allowOverlaps)) )
    
    @staticmethod
    def removeChrMemmapFolders(genome, trackName, allowOverlaps):
        chrList = TrackInfoDataCollector(genome, trackName).getPreProcessedChrs(allowOverlaps)
        for chr in chrList:
            path = createDirPath(trackName, genome, chr, allowOverlaps)
            assert os.path.exists(path), 'Path does not exist: ' + path
            assert os.path.isdir(path), 'Path is not a directory: ' + path
            shutil.rmtree(path)

    @staticmethod
    def checkIfEdgeIdsExist(genome, trackName, allowOverlaps):
        collector = TrackInfoDataCollector(genome, trackName)
        if not collector.getTrackFormat().isLinked():
            return
        
        uniqueIds = numpy.array([], dtype='S')
        uniqueEdgeIds = numpy.array([], dtype='S')
        
        for chr in collector.getPreProcessedChrs(allowOverlaps):
            trackSource = TrackSource()
            trackData = trackSource.getTrackData(trackName, genome, chr, allowOverlaps)
            uniqueIds = numpy.unique(numpy.concatenate((uniqueIds, trackData['id'][:])))
            uniqueEdgeIds = numpy.unique(numpy.concatenate((uniqueEdgeIds, trackData['edges'][:].flatten())))
        
        uniqueIds = uniqueIds[uniqueIds != '']
        uniqueEdgeIds = uniqueEdgeIds[uniqueEdgeIds != '']
        
        unmatchedIds = set(uniqueEdgeIds) - set(uniqueIds)
        if len(unmatchedIds) > 0:
            raise InvalidFormatError("Error: the following ids specified in the 'edges' column do not exist in the dataset: " + ', '.join(sorted(unmatchedIds)))
    
    @staticmethod
    def checkUndirectedEdges(genome, trackName, allowOverlaps):
        collector = TrackInfoDataCollector(genome, trackName)
        if not (collector.getTrackFormat().isLinked() and collector.hasUndirectedEdges()):
            return
        
        complementEdgeWeightDict = {}
        
        for chr in collector.getPreProcessedChrs(allowOverlaps):
            trackSource = TrackSource()
            trackData = trackSource.getTrackData(trackName, genome, chr, allowOverlaps)
            
            ids = trackData['id']
            edges = trackData['edges']
            weights = trackData.get('weights')
            
            for i, id in enumerate(ids):
                edgesAttr = edges[i][edges[i] != '']
                weightsAttr = weights[i][edges[i] != ''] if weights is not None else None
                PreProcessUtils._adjustComplementaryEdgeWeightDict(complementEdgeWeightDict, id, edgesAttr, weightsAttr)
        
        if len(complementEdgeWeightDict) != 0:
                unmatchedPairs = []
                for toId in complementEdgeWeightDict:
                    for fromId in complementEdgeWeightDict[toId]:
                        unmatchedPairs.append((fromId, toId, complementEdgeWeightDict[toId][fromId]))
                raise InvalidFormatError("Error: All edges are not undirected. The following edges specifications " +\
                                         "are not matched by an opposite edge with equal weight:" + os.linesep +\
                                         os.linesep.join(["from '%s' to '%s'" % (fromId, toId) + \
                                                          (" with weight '%s'" % weight  if weight != '' else '') \
                                                          for fromId, toId, weight in unmatchedPairs]))
        
    @staticmethod
    def _adjustComplementaryEdgeWeightDict(complementEdgeWeightDict, id, edges, weights):
        for index, edgeId in enumerate(edges):
            weight = weights[index] if weights is not None else ''
                
            if id in complementEdgeWeightDict and edgeId in complementEdgeWeightDict[id]:
                check = (complementEdgeWeightDict[id][edgeId] != weight)
                if (type(check) == bool and check) or (type(check) != bool and check.all()):
                    raise InvalidFormatError("Error: edge ('%s' <-> '%s') is not undirected. The weight must be equal in both directions (%s != %s)" % (edgeId, id, complementEdgeWeightDict[id][edgeId], weights[index]))
                del complementEdgeWeightDict[id][edgeId]
                if len(complementEdgeWeightDict[id]) == 0:
                    del complementEdgeWeightDict[id]
                        
            elif edgeId in complementEdgeWeightDict:
                if id in complementEdgeWeightDict[edgeId]:
                    raise ShouldNotOccurError('Error: the complementary edge(%s) has already been added to complementEdgeWeightDict["%s"] ... ' % (id, edgeId))
                complementEdgeWeightDict[edgeId][id] = weight
            else:
                complementEdgeWeightDict[edgeId] = {id: weight}
    