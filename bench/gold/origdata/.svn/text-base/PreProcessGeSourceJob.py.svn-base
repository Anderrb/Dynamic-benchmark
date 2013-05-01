#from gold.origdata.SplitGESourceByChrs import SplitGESourceByChrs
from gold.description.TrackInfo import TrackInfo, TrackInfoDataCollector
from gold.origdata.OutputDirectory import OutputDirectory
from gold.util.CommonFunctions import createDirPath
from quick.util.GenomeInfo import GenomeInfo
from gold.util.CustomExceptions import EmptyGESourceError
from gold.origdata.PreProcessUtils import PreProcessUtils
from config.Config import PROCESSED_DATA_PATH
import os
import shutil

class PreProcessGeSourceJob(object):
    VERSION = '0.95'
        
    def __init__(self, trackName, allowOverlaps, chr, geSource, mode='Real'):
        self._trackName = trackName
        self._allowOverlaps = allowOverlaps
        self._chr = chr
        self._geSource = geSource
        self._mode = mode
        self._genome = geSource.getGenome()
        self._dirty = False
        
    def process(self):
        self._createPreProcFiles()
        
        if self._mode in ['UpdateMeta', 'Real']:
            self._dirty = True

    def _createPreProcFiles(self):
        collector = TrackInfoDataCollector(self._genome, self._trackName)
        collector.updateMetaDataForFinalization(self._geSource.getFileSuffix(), self._geSource.getPrefixList(), \
                                                self._geSource.getValDataType(), self._geSource.getValDim(), \
                                                self._geSource.getEdgeWeightDataType(), self._geSource.getEdgeWeightDim(), \
                                                self._geSource.hasUndirectedEdges(),
                                                self._geSource.getVersion(), PreProcessUtils.constructId(self._geSource))

        if collector.getNumElements(self._chr, self._allowOverlaps) == 0:
            return
        
        if self._mode != 'Real':
            for ge in self._geSource:
                pass
            return
        
        dirPath = createDirPath(self._trackName, self._genome, self._chr, self._allowOverlaps)

        dir = OutputDirectory(dirPath, collector.getPrefixList(self._allowOverlaps), \
                              collector.getNumElements(self._chr, self._allowOverlaps),\
                              GenomeInfo.getChrLen(self._genome, self._chr), \
                              collector.getValDataType(), collector.getValDim(), \
                              collector.getEgdeWeightDataType(), collector.getEgdeWeightDim(), \
                              collector.getMaxNumEdges(self._chr, self._allowOverlaps), \
                              collector.getMaxStrLens(self._chr, self._allowOverlaps))
        
        writeFunc = dir.writeRawSlice if self._geSource.isSliceSource() else dir.writeElement
        
        for ge in self._geSource:
            writeFunc(ge)
        
        collector.appendPreProcessedChr(self._allowOverlaps, self._chr)
        
        dir.close()

    def hasModifiedData(self):
        return self._dirty
