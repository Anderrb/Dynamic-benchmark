from quick.util.StaticFile import GalaxyRunSpecificFile
from quick.util.GenomeInfo import GenomeInfo
from quick.application.GalaxyInterface import GalaxyInterface
from gold.application.StatRunner import AnalysisDefJob
from gold.util.CommonFunctions import getOrigFn
import os

class BasicTrackIntersection:
    def __init__(self, genome, referenceTrackFn, queryTrack):
        self._genome = genome
        self._referenceTrackFn = referenceTrackFn
        self._queryTrackName = queryTrack
        self._intersectedReferenceBins = None
        self._result = None
        
    def getNumberOfIntersectedBins(self):
        return len(self.getIntersectedReferenceBins() )

    def run(self):
        regSpec, binSpec = 'file', self._referenceTrackFn
        trackName1 = self._queryTrackName
        trackName2 = None
        from gold.description.TrackInfo import TrackInfo
        
        formatName = TrackInfo(self._genome, trackName1).trackFormatName
        formatConv = ''
        if 'segments' in formatName:
            formatConv = '[tf1:=SegmentToStartPointFormatConverter:]'

        analysisDef = formatConv + '-> CountPointStat'

        print '<div class="debug">'
        #trackName1, trackName2, analysisDef = GalaxyInterface._cleanUpAnalysisDef(trackName1, trackName2, analysisDef)
        #trackName1, trackName2 = GalaxyInterface._cleanUpTracks([trackName1, trackName2], genome, realPreProc=True)
        #
        #userBinSource, fullRunArgs = GalaxyInterface._prepareRun(trackName1, trackName2, analysisDef, regSpec, binSpec, self._genome)
        #res = AnalysisDefJob(analysisDef, trackName1, trackName2, userBinSource, **fullRunArgs).run()
        res = GalaxyInterface.runManual([trackName1, trackName2], analysisDef, regSpec, binSpec, self._genome, printResults=False, printHtmlWarningMsgs=False)
        #print res
        print '</div>'
        
        resDictKeys = res.getResDictKeys()
        assert len(resDictKeys)==1, resDictKeys
        resDictKey = resDictKeys[0]
        targetBins = [bin for bin in res.keys() if res[bin][resDictKey]>0]
        self._result = res
        self._intersectedReferenceBins = targetBins            
        
    def getIntersectedReferenceBins(self):
        if self._intersectedReferenceBins is None:
            self.run()
        return self._intersectedReferenceBins

    def getIntersectionResult(self):
        if self._result is None:
            self.run()
        return self._result

    def getUniqueResDictKey(self):    
        resDictKeys = self._result.getResDictKeys()
        assert len(resDictKeys)==1, resDictKeys
        return resDictKeys[0]
        
class TrackIntersection(BasicTrackIntersection):
    def __init__(self, genome, referenceTrackFn, queryTrack, galaxyFn):
        BasicTrackIntersection.__init__(self, genome, referenceTrackFn, queryTrack)
        self._galaxyFn = galaxyFn
        pass
    
    #def setReferenceTrackFn(self, referenceTrack):
    #    self._referenceTrackFn = referenceTrackFn
    
    def expandReferenceTrack(self, upFlankSize, downFlankSize):        
        if not (upFlankSize == downFlankSize == 0):
            self._intersectedReferenceBins = None
            flankedGeneRegsTempFn  = GalaxyRunSpecificFile(['flankedGeneRegs.category.bed'],self._galaxyFn).getDiskPath()            
            GalaxyInterface.expandBedSegments(self._referenceTrackFn, flankedGeneRegsTempFn, self._genome, upFlankSize, downFlankSize)
            self._referenceTrackFn = flankedGeneRegsTempFn
            #print 'flankedGeneRegsTempFn: ',flankedGeneRegsTempFn

    def getIntersectedRegionsStaticFileWithContent(self):
        intersectedRegs = self.getIntersectedReferenceBins()
        staticFile = GalaxyRunSpecificFile(['intersected_regions.bed'],self._galaxyFn)
        self.writeRegionListToBedFile(intersectedRegs, staticFile.getDiskPath() )
        return staticFile

    @staticmethod
    def writeRegionListToBedFile(regList, fn):
        from quick.util.CommonFunctions import ensurePathExists
        ensurePathExists(fn)
        f = open(fn, 'w')
        for reg in regList:
            f.write( '\t'.join([reg.chr, str(reg.start), str(reg.end)]) + os.linesep )
        f.close()
        
            
        
class GeneIntersection(TrackIntersection):
    def __init__(self, genome, geneSource, queryTrack, galaxyFn):
        assert geneSource == 'Ensembl'
        geneRegsTrackName = GenomeInfo.getStdGeneRegsTn(genome)
        geneRegsTrackFn = getOrigFn(genome, geneRegsTrackName, '.category.bed')
        TrackIntersection.__init__(self, genome, geneRegsTrackFn, queryTrack, galaxyFn)
        pass
    
    def getGeneIdStaticFileWithContent(self):
        targetBins = self.getIntersectedReferenceBins()
        idFileNamer = GalaxyRunSpecificFile(['allGeneIds.txt'],self._galaxyFn)
        idFileNamer.writeTextToFile(os.linesep.join([str(bin.val).split('|')[0] for bin in targetBins]) + os.linesep)
        return idFileNamer