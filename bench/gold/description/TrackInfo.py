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

import copy
import os
import os.path
import third_party.safeshelve as safeshelve
import datetime
from gold.util.CommonFunctions import createOrigPath, strWithStdFormatting
from gold.result.HtmlCore import HtmlCore
from config.Config import DATA_FILES_PATH
from gold.track.TrackFormat import TrackFormat, TrackFormatReq
from gold.util.CustomExceptions import ShouldNotOccurError
from quick.util.StaticFile import StaticImage
from collections import defaultdict, namedtuple
from functools import partial 

FieldInfo = namedtuple('FieldInfo', ['fullName', 'guiElementType'])

def constructKey(genome, trackName):
    key = ':'.join([genome] + trackName)
    assert type(key) == str, 'Non-str key: ' + key + ' of type: ' + str(type(key)) + '. Specific types: ' + str([type(x) for x in [genome] + trackName])
    return key
    
class TrackInfo(object):
    SHELVE_FN = DATA_FILES_PATH + os.sep + 'TrackInfo.shelve'
    SHELVE_COPY_FN = DATA_FILES_PATH + os.sep + 'TrackInfo.shelve.copy'
    SHELVE_ERRORS_FN = DATA_FILES_PATH + os.sep + 'TrackInfo.shelve.errors'
    
    PROTOCOL = 0

    FIELD_INFO_DICT = { \
        'description': FieldInfo('Description', 'textbox'), \
        'displayConvConf': FieldInfo('Display conventions and configuration', 'textbox'), \
        'methods': FieldInfo('Methods', 'textbox'), \
        'credits': FieldInfo('Credits', 'textbox'), \
        'reference': FieldInfo('References', 'textbox'), \
        'restrictions': FieldInfo('Data release policy', 'textbox'), \
        'version': FieldInfo('Version', 'textbox'), \
        'quality': FieldInfo('Quality', 'textbox'), \
        'hbContact': FieldInfo('HyperBrowser contact', 'textbox'), \
        'cellTypeSpecific': FieldInfo('Cell type specific', 'checkbox'), \
        'cellType': FieldInfo('Cell type', 'textbox'), \
        'private': FieldInfo('Private (our group only)', 'checkbox'), \
        'fileType': FieldInfo('File type', 'text'), \
        'trackFormatName': FieldInfo('Original track type', 'text'), \
        'markType': FieldInfo('Value type', 'text'), \
        'weightType': FieldInfo('Edge weight type', 'text'), \
        'undirectedEdges': FieldInfo('Undirected edges', 'text'), \
        'origElCount': FieldInfo('Original element count', 'text'), \
        'clusteredElCount': FieldInfo('Element count after clustering', 'text'), \
        'numValCategories': FieldInfo('Original number of value categories', 'text'), \
        'numClusteredValCategories': FieldInfo('Number of value categories after clustering', 'text'), \
        'numEdgeWeightCategories': FieldInfo('Number of edge categories', 'text'), \
        'subTrackCount': FieldInfo('Total number of tracks (with subtracks)', 'text'), \
        'timeOfPreProcessing': FieldInfo('Time of preprocessing', 'text'), \
        'timeOfLastUpdate': FieldInfo('Time of last update', 'text'), \
        'lastUpdatedBy': FieldInfo('Last update by', 'text')}

    def __new__(cls, genome, trackName):
        #Temporary hack
        if genome in ['hg18','NCBI36']:
            genome = 'NCBI36'
        
        trackInfoShelve = safeshelve.open(cls.SHELVE_FN, 'c', protocol=cls.PROTOCOL)
        stored = trackInfoShelve.get( constructKey(genome, trackName) )
        trackInfoShelve.close()
        if stored is not None:
            return stored
        else:
            return object.__new__(cls)
    
    def __init__(self, genome, trackName):
        #Temporary hack
        if genome in ['hg18','NCBI36']:
            genome = 'NCBI36'

        existingAttrs = copy.copy(self.__dict__)
        assert existingAttrs.get('trackName') in [None, trackName], '%s not in [None, %s]' % (existingAttrs.get('trackName'), trackName) #An exception could here occur if there is a preprocessed directory that contains colon in its name, as this may lead to splitting some place and not splitting other places..
        assert existingAttrs.get('genome') in [None, genome], '%s not in [None, %s]' % (existingAttrs.get('genome'), genome)
        self.trackName = trackName
        self.genome = genome
        
        self.id = None
        
        self.description = ''
        self.displayConvConf = ''
        self.methods = ''
        self.credits = ''
        self.reference = ''
        self.restrictions = ''
        self.version = ''
        self.quality = ''
        self.hbContact = ''
        self.cellTypeSpecific = False
        self.cellType = ''
        
        self.private = False
        
        self.lastUpdatedBy = ''
        self.timeOfLastUpdate = None
        
        #self.header = ''
        self.fileType = ''
        self.trackFormatName = ''
        self.markType = ''
        self.weightType = ''
        self.undirectedEdges = None
        self.subTrackCount = None
        self.origElCount = None
        self.clusteredElCount = None
        self.numValCategories = None
        self.numClusteredValCategories = None
        self.numEdgeWeightCategories = None
        self.timeOfPreProcessing = None
        self.preProcVersion = ''

        self.__dict__.update(existingAttrs)
        
    @staticmethod
    def createInstanceFromKey(key):
        key = key.split(':')
        return TrackInfo(key[0], key[1:])
        
    @staticmethod
    def createInstanceAsCopyOfOther(genome, trackName, otherTrackName):
        ti = TrackInfo(genome, otherTrackName)
        ti.trackName = trackName
        return ti
        
    @staticmethod
    def createInstanceFromAttrsFromStrRepr(genome, strReprOfAttrDict):
        attrDict = eval(strReprOfAttrDict)
        trackName = attrDict['trackName']
        ti = TrackInfo(genome, trackName)
        ti.__dict__.update(attrDict)
        return ti
    
    def isValid(self, fullAccess=True):
        return (fullAccess or not self.private) and \
                self.timeOfPreProcessing is not None
        
    def resetTimeOfPreProcessing(self):
        self.timeOfPreProcessing = None
        self.store()
    
    def store(self):
        trackInfoShelve = safeshelve.open(self.SHELVE_FN, protocol=self.PROTOCOL)
        trackInfoShelve[ constructKey(self.genome, self.trackName) ] = self
        trackInfoShelve.close()
        
    def removeEntryFromShelve(self):
        trackInfoShelve = safeshelve.open(self.SHELVE_FN, protocol=self.PROTOCOL)
        key = constructKey(self.genome, self.trackName)
        if key in trackInfoShelve:
            del trackInfoShelve[key]
        trackInfoShelve.close()

    def __str__(self):
        return self.allInfo(printEmpty=True)
        
    def _isDenseTrack(self):
        try:
            return TrackFormatReq(name=self.trackFormatName).isDense()
        except:
            return False
        
    def _getFieldInfoDict(self, field, isDense):
        if field == 'clusteredElCount' and isDense:
            return self.FIELD_INFO_DICT['origElCount']
        
        if field == 'numClusteredValCategories' and isDense:
            return self.FIELD_INFO_DICT['numValCategories']
            
        return self.FIELD_INFO_DICT[field]
        
    def _addDescriptionLineIfTrue(self, core, isDense, printEmpty, field, expression, formatFunc=lambda x: str(x)):
        if printEmpty or expression:
            core.descriptionLine(self._getFieldInfoDict(field, isDense).fullName, formatFunc(getattr(self, field)))
        
    def _addTrackTypeIllustration(self, core, trackFormatName):
        tfAbbrev = ''.join([x[0] for x in trackFormatName.split()]).upper()
        core.image(StaticImage(['illustrations','%s.png' % tfAbbrev]).getURL(), \
                   style='width: 300px')
        
    def allInfo(self, printEmpty=False):
        core = HtmlCore()
        isDense = self._isDenseTrack()
        
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'subTrackCount', \
            self.subTrackCount and (self.subTrackCount > 1 or not self.isValid()))
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'origElCount', self.origElCount, \
            lambda x: strWithStdFormatting(x))
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'clusteredElCount', self.clusteredElCount, \
            lambda x: strWithStdFormatting(x))
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'numValCategories', self.numValCategories, \
            lambda x: strWithStdFormatting(x))
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'numClusteredValCategories', self.numClusteredValCategories, \
            lambda x: strWithStdFormatting(x))
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'numEdgeWeightCategories', self.numEdgeWeightCategories, \
            lambda x: strWithStdFormatting(x))
        
        self._addTrackTypeIllustration(core, self.trackFormatName)

        return self.mainInfo(printEmpty) + unicode(core)

    def mainInfo(self, printEmpty=False):
        core = HtmlCore()
        isDense = self._isDenseTrack()
        
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'description', self.description)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'displayConvConf', self.displayConvConf)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'methods', self.methods)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'credits', self.credits)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'reference', self.reference, \
            lambda x: str( HtmlCore().link(x, x, True) ) if x.startswith('http://') else x)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'restrictions', self.restrictions)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'version', self.version)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'quality', self.quality)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'cellType', \
            self.cellTypeSpecific and self.cellType)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'hbContact', self.hbContact)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'trackFormatName', True)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'markType', self.markType)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'weightType', self.weightType)
        self._addDescriptionLineIfTrue(core, isDense, printEmpty, 'undirectedEdges', \
            self.undirectedEdges is not None and 'linked' in self.trackFormatName.lower())
        
        return unicode(core)
    
    def getUIRepr(self):
        uiRepr = []
        isDense = self._isDenseTrack()
        for field in ['description', 'displayConvConf', 'methods', 'credits', 'reference', 'restrictions', \
                      'version', 'quality', 'hbContact', 'cellTypeSpecific', 'cellType', \
                      'private', 'fileType', 'trackFormatName', 'markType', 'weightType', 'undirectedEdges', \
                      'origElCount', 'clusteredElCount', 'numValCategories', 'numClusteredValCategories', \
                      'numEdgeWeightCategories', 'subTrackCount', 'timeOfPreProcessing', 'timeOfLastUpdate', \
                      'lastUpdatedBy']:
            fieldInfo = self._getFieldInfoDict(field, isDense)
            uiRepr.append((fieldInfo.fullName, field, getattr(self, field), fieldInfo.guiElementType))
        return tuple(uiRepr)
        
    def getStrReprOfAttrDict(self):
        attrs =  [attr for attr in dir(self) \
                  if not callable(getattr(self, attr)) and not attr.startswith("__")]
        return repr( dict([(attr, getattr(self, attr)) for attr in attrs]) )
    
    
    def setAttrs(self, attrDict, username):
        self.__dict__.update(attrDict)
        self.lastUpdatedBy = username
        self.timeOfLastUpdate = datetime.datetime.now()

    def getOrigFn(self):
        return createOrigPath(self.genome, self.trackName, None)

    @staticmethod
    def constructId(genome, trackName, geSourceVersion, preProcVersion):
        origPath = createOrigPath(genome, trackName)
        return TrackInfo.constructIdFromPath(genome, origPath, geSourceVersion, preProcVersion)
        
    @staticmethod
    def constructIdFromPath(genome, origPath, geSourceVersion, preProcVersion):
        if os.path.isdir(origPath):
            fileList = sorted([fn for fn in os.listdir(origPath) if os.path.isfile(origPath+os.sep+fn) and fn[0]!='.'])
        elif os.path.isfile(origPath):
            fileList = [os.path.basename(origPath)]
            origPath = os.path.dirname(origPath)
        else:
            raise ShouldNotOccurError
        
        fileInfo = tuple([ (fn, os.stat(os.sep.join([origPath, fn])).st_mtime ) for fn in fileList ])
        return hash( (hash(fileInfo), geSourceVersion, preProcVersion) )

    @staticmethod
    def constructIdByTimeStamp():
        return hash(datetime.datetime.now())
    
    @classmethod
    def getFilteredEntriesFromShelve(cls, genome, trackNameFilter):
        filterKey = constructKey(genome, trackNameFilter)
        trackInfoShelve = safeshelve.open(cls.SHELVE_FN, 'r', protocol=cls.PROTOCOL)
        filteredKeys = [x for x in trackInfoShelve.keys() if x.startswith(filterKey)]
        trackInfoShelve.close()
        return filteredKeys

    @classmethod
    def removeFilteredEntriesFromShelve(cls, genome, trackNameFilter):
        filteredKeys = TrackInfo.getFilteredEntriesFromShelve(genome, trackNameFilter)
        trackInfoShelve = safeshelve.open(cls.SHELVE_FN, 'w', protocol=cls.PROTOCOL)
        for key in filteredKeys:
            del trackInfoShelve[key]
        trackInfoShelve.close()
        
    @classmethod
    def updateShelveItemsAndCopyToNewFile(cls):
        assert not os.path.exists(cls.SHELVE_COPY_FN)
        assert not os.path.exists(cls.SHELVE_ERRORS_FN)
        
        trackInfoShelveCopy = safeshelve.open(cls.SHELVE_COPY_FN, 'c', protocol=cls.PROTOCOL)
        trackInfoShelveErrors = safeshelve.open(cls.SHELVE_ERRORS_FN, 'c', protocol=cls.PROTOCOL)
        
        trackInfoShelve = safeshelve.open(cls.SHELVE_FN, 'r', protocol=cls.PROTOCOL)
        keys = trackInfoShelve.keys()
        trackInfoShelve.close()

        for i,key in enumerate(keys):
            try:
                ti = TrackInfo.createInstanceFromKey(key)
            except:
                trackInfoShelve = safeshelve.open(cls.SHELVE_FN, 'r', protocol=cls.PROTOCOL)
                trackInfoShelveErrors[key] = trackInfoShelve[key]
                trackInfoShelve.close()
            
            trackInfoShelveCopy[key] = ti
            
            if i%10000 == 0:
                print '.',

        trackInfoShelveCopy.close()
        trackInfoShelveErrors.close()


#class TempTrackInfo(TrackInfo):
#    SHELVE_FN = DATA_FILES_PATH + os.sep + 'TempTrackInfo.shelve'
#    SHELVE_COPY_FN = DATA_FILES_PATH + os.sep + 'TempTrackInfo.shelve.copy'
#    SHELVE_ERRORS_FN = DATA_FILES_PATH + os.sep + 'TempTrackInfo.shelve.errors'
#    
#    PROTOCOL = 1
    
class TempTrackInfo(object):
    _tempTrackInfoStorage = {}

    def __new__(cls, genome, trackName):
        key = constructKey(genome, trackName)
        
        if key in cls._tempTrackInfoStorage:
            return cls._tempTrackInfoStorage[key]
        else:
            obj = object.__new__(cls)
            cls._tempTrackInfoStorage[key] = obj
            return obj
        
    def __init__(self, genome, trackName):
        existingAttrs = copy.copy(self.__dict__)
        
        self.genome = genome
        self.trackName = trackName
        
        self.preProcChrs = defaultdict(list)
        self.boundingRegionTuples = defaultdict(list)
        self.preProcDirty = False
        self.preProcFilesExist = {}
        self.removedPreProcFiles = {}
        
        self.fileType = ''
        self.prefixList = None
        self.valDataType = None
        self.valDim = None
        self.weightDataType = None
        self.weightDim = None
        self.undirectedEdges = None
        self.preProcVersion = ''
        self.id = None
        
        self.origElCountPerChr = defaultdict(int)
        self.clusteredElCountPerChr = defaultdict(int)
        self.valCategoriesPerChr = defaultdict(partial(defaultdict, set))
        self.edgeWeightCategoriesPerChr = defaultdict(partial(defaultdict, set))
        self.maxNumEdgesPerChr = defaultdict(partial(defaultdict, int))
        self.maxStrLensPerChr = defaultdict(partial(defaultdict, partial(defaultdict, int)))
        
        self.__dict__.update(existingAttrs)
        
    def store(self):
        pass
        
    def removeEntryFromShelve(self):
        del self._tempTrackInfoStorage[constructKey(self.genome, self.trackName)]

    
class TrackInfoDataCollector(object):
    def __init__(self, genome, trackName):
        self._tempTrackInfo = TempTrackInfo(genome, trackName)
        #self._tempTrackInfo = TempTrackInfo(genome, ['__tmp__'] + trackName)
        
        #existingAttrs = copy.copy(self._tempTrackInfo.__dict__)
        
        #self._tempTrackInfo.preProcChrs = defaultdict(list)
        #self._tempTrackInfo.boundingRegionTuples = defaultdict(list)
        #self._tempTrackInfo.preProcDirty = False
        #self._tempTrackInfo.preProcFilesExist = {}
        #self._tempTrackInfo.removedPreProcFiles = {}
        #self._tempTrackInfo.prefixList = None
        #self._tempTrackInfo.valDataType = None
        #self._tempTrackInfo.valDim = None
        #self._tempTrackInfo.weightDataType = None
        #self._tempTrackInfo.weightDim = None
        #self._tempTrackInfo.origElCountPerChr = defaultdict(int)
        #self._tempTrackInfo.clusteredElCountPerChr = defaultdict(int)
        #self._tempTrackInfo.valCategoriesPerChr = defaultdict(partial(defaultdict, set))
        #self._tempTrackInfo.edgeWeightCategoriesPerChr = defaultdict(partial(defaultdict, set))
        #self._tempTrackInfo.maxNumEdgesPerChr = defaultdict(partial(defaultdict, int))
        #self._tempTrackInfo.maxStrLensPerChr = defaultdict(partial(defaultdict, partial(defaultdict, int)))
        #
        #self._tempTrackInfo.__dict__.update(existingAttrs)
        
    def updateFileSizeInfoForPreProc(self, chr, allowOverlaps, numElements, valCategories, \
                                     edgeWeightCategories, maxNumEdges, maxStrLens):
        if allowOverlaps:
            self._tempTrackInfo.origElCountPerChr[chr] += numElements
        else:
            self._tempTrackInfo.clusteredElCountPerChr[chr] += numElements
            
        self._tempTrackInfo.valCategoriesPerChr[allowOverlaps][chr] |= valCategories
        
        self._tempTrackInfo.edgeWeightCategoriesPerChr[allowOverlaps][chr] |= edgeWeightCategories
        
        self._tempTrackInfo.maxNumEdgesPerChr[allowOverlaps][chr] = \
            max(self._tempTrackInfo.maxNumEdgesPerChr[allowOverlaps][chr], maxNumEdges)
        
        for key in maxStrLens:
            self._tempTrackInfo.maxStrLensPerChr[allowOverlaps][chr][key] = \
                max(self._tempTrackInfo.maxStrLensPerChr[allowOverlaps][chr][key], maxStrLens[key])
        
        self._tempTrackInfo.store()
        
    def _checkAndUpdateAttribute(self, attr, value, mayBeEmptyString=False, isGeSourceAttr=False, extraErrorMsg=''):
        emptyList = [None, ''] if mayBeEmptyString else [None]
        valAllowedList = emptyList + [value]
        assert getattr(self._tempTrackInfo, attr) in valAllowedList, \
            ('Files in the same folder use geSources with different %ss [%s != %s]' % (attr, getattr(self._tempTrackInfo, attr), value)) if isGeSourceAttr else \
            ('Files in the same folder have different %ss [%s != %s]' % (attr, getattr(self._tempTrackInfo, attr), value)) \
            + (' (%s)' if extraErrorMsg else '')
        
        if value not in emptyList:
            setattr(self._tempTrackInfo, attr, value)
            return True
        return False
        
    def updateMetaDataForFinalization(self, fileType, prefixList, valDataType, valDim, weightDataType, weightDim, undirectedEdges, preProcVersion, id):
        dirty = self._checkAndUpdateAttribute('fileType', fileType, mayBeEmptyString=True, isGeSourceAttr=False)
        dirty |= self._checkAndUpdateAttribute('prefixList', prefixList, mayBeEmptyString=False, isGeSourceAttr=False, extraErrorMsg='Different formats?')
        dirty |= self._checkAndUpdateAttribute('valDataType', valDataType, mayBeEmptyString=False, isGeSourceAttr=False, extraErrorMsg='Different formats?')
        dirty |= self._checkAndUpdateAttribute('valDim', valDim, mayBeEmptyString=False, isGeSourceAttr=False, extraErrorMsg='Different formats?')
        dirty |= self._checkAndUpdateAttribute('weightDataType', weightDataType, mayBeEmptyString=False, isGeSourceAttr=False, extraErrorMsg='Different formats?')
        dirty |= self._checkAndUpdateAttribute('weightDim', weightDim, mayBeEmptyString=False, isGeSourceAttr=False, extraErrorMsg='Different formats?')
        dirty |= self._checkAndUpdateAttribute('undirectedEdges', undirectedEdges, mayBeEmptyString=False, isGeSourceAttr=False, extraErrorMsg='Different formats?')
        dirty |= self._checkAndUpdateAttribute('preProcVersion', preProcVersion, mayBeEmptyString=True, isGeSourceAttr=True, extraErrorMsg='strange..')
        dirty |= self._checkAndUpdateAttribute('id', id, mayBeEmptyString=True, isGeSourceAttr=True, extraErrorMsg='Have the original files been modified during the run?')

        if dirty:
            self._tempTrackInfo.store()
        
    def appendPreProcessedChr(self, allowOverlaps, chr):
        if len(self._tempTrackInfo.preProcChrs[allowOverlaps]) > 0 and \
            self._tempTrackInfo.preProcChrs[allowOverlaps][-1] == chr:
                return
        
        self._tempTrackInfo.preProcChrs[allowOverlaps].append(chr)
        self._tempTrackInfo.store()        
    
    def appendBoundingRegionTuples(self, allowOverlaps, boundingRegionTuples):
        self._tempTrackInfo.boundingRegionTuples[allowOverlaps] += boundingRegionTuples
        self._tempTrackInfo.store()        
    
    def updatePreProcDirtyStatus(self, dirty):
        if dirty:
            self._tempTrackInfo.preProcDirty = True
            self._tempTrackInfo.store()
                    
    def updatePreProcFilesExistFlag(self, allowOverlaps, val):
        self._tempTrackInfo.preProcFilesExist[allowOverlaps] = val
        self._tempTrackInfo.store()
        
    def updateRemovedPreProcFilesFlag(self, allowOverlaps, val):
        self._tempTrackInfo.removedPreProcFiles[allowOverlaps] = val
        self._tempTrackInfo.store()
    
    def getPreProcessedChrs(self, allowOverlaps):
        return self._tempTrackInfo.preProcChrs[allowOverlaps]
    
    def getBoundingRegionTuples(self, allowOverlaps):
        return self._tempTrackInfo.boundingRegionTuples[allowOverlaps]
    
    def preProcIsDirty(self):
        return self._tempTrackInfo.preProcDirty
        
    def preProcFilesExist(self, allowOverlaps):
        return self._tempTrackInfo.preProcFilesExist.get(allowOverlaps)
        
    def hasRemovedPreProcFiles(self, allowOverlaps):
        return self._tempTrackInfo.removedPreProcFiles.get(allowOverlaps)
        
    def getTrackFormat(self):
        return TrackFormat.createInstanceFromPrefixList(self._tempTrackInfo.prefixList, \
                                                        self._tempTrackInfo.valDataType, \
                                                        self._tempTrackInfo.valDim, \
                                                        self._tempTrackInfo.weightDataType, \
                                                        self._tempTrackInfo.weightDim)
        
    def getPrefixList(self, allowOverlaps):
        if self._tempTrackInfo.prefixList is None:
            return None
        return self._tempTrackInfo.prefixList
    
    def getValDataType(self):
        return self._tempTrackInfo.valDataType
    
    def getValDim(self):
        return self._tempTrackInfo.valDim
        
    def getEgdeWeightDataType(self):
        return self._tempTrackInfo.weightDataType
    
    def getEgdeWeightDim(self):
        return self._tempTrackInfo.weightDim
        
    def hasUndirectedEdges(self):
        return self._tempTrackInfo.undirectedEdges
        
    def getNumElements(self, chr, allowOverlaps):
        if allowOverlaps:
            return self._tempTrackInfo.origElCountPerChr[chr]
        else:
            return self._tempTrackInfo.clusteredElCountPerChr[chr]
        
    def getMaxNumEdges(self, chr, allowOverlaps):
        return self._tempTrackInfo.maxNumEdgesPerChr[allowOverlaps][chr]
        
    def getMaxStrLens(self, chr, allowOverlaps):
        return self._tempTrackInfo.maxStrLensPerChr[allowOverlaps][chr]
    
    def _countNumCategories(self, categoryDoubleDict, allowOverlaps):
        numCategories = len(reduce(lambda x,y: x|y, categoryDoubleDict[allowOverlaps].values())) 
        return numCategories if numCategories > 0 else None
    
    def finalize(self, username, printMsg):
        ti = TrackInfo(self._tempTrackInfo.genome, self._tempTrackInfo.trackName)
        
        ti.fileType = self._tempTrackInfo.fileType
        trackFormat = self.getTrackFormat()
        ti.trackFormatName = trackFormat.getFormatName()
        ti.markType = trackFormat.getValTypeName()
        ti.weightType = trackFormat.getWeightTypeName()
        ti.undirectedEdges = self._tempTrackInfo.undirectedEdges
        ti.preProcVersion = self._tempTrackInfo.preProcVersion

        ti.origElCount = sum(self._tempTrackInfo.origElCountPerChr.values())
        ti.clusteredElCount = sum(self._tempTrackInfo.clusteredElCountPerChr.values())
        
        if trackFormat.isDense() and trackFormat.isInterval():
            ti.origElCount -= len(self._tempTrackInfo.boundingRegionTuples[True])
            ti.clusteredElCount -= len(self._tempTrackInfo.boundingRegionTuples[False])

        if True in self._tempTrackInfo.valCategoriesPerChr:
            ti.numValCategories = self._countNumCategories(self._tempTrackInfo.valCategoriesPerChr, allowOverlaps=True)
        
        if False in self._tempTrackInfo.valCategoriesPerChr:
            ti.numClusteredValCategories = self._countNumCategories(self._tempTrackInfo.valCategoriesPerChr, allowOverlaps=False)

        if True in self._tempTrackInfo.edgeWeightCategoriesPerChr:
            ti.numEdgeWeightCategories = self._countNumCategories(self._tempTrackInfo.edgeWeightCategoriesPerChr, allowOverlaps=True)
        
        ti.id = self._tempTrackInfo.id
        ti.timeOfPreProcessing = datetime.datetime.now()
    
        ti.lastUpdatedBy = username
        if ti.hbContact == '':
            ti.hbContact = username
        
        ti.store()
        
        if printMsg:
            print "Finished preprocessing track '%s'." % ':'.join(self._tempTrackInfo.trackName)
            print
        
        self._tempTrackInfo.removeEntryFromShelve()

    def removeEntryFromShelve(self):
        self._tempTrackInfo.removeEntryFromShelve()
