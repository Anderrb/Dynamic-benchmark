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

import os
from gold.util.CommonFunctions import smartSum, getClassName, isIter
from gold.util.CompBinManager import CompBinManager
from gold.util.CustomExceptions import ShouldNotOccurError, CentromerError, TooLargeBinError, \
                                       TooSmallBinError, AbstractClassError, NoneResultError, \
                                       OutsideBoundingRegionError
from config.Config import TRACE_STAT, DebugConfig
from gold.track.Track import Track
from gold.statistic.ResultsMemoizer import ResultsMemoizer
from gold.application.LogSetup import logging, HB_LOGGER, exceptionLogging, logException, logExceptionOnce, logMessageOnce, logMessage
from gold.track.GenomeRegion import GenomeRegion
from copy import copy
from collections import OrderedDict
from quick.util.CommonFunctions import convertTNstrToTNListFormat
import numpy
from math import ceil

class Statistic(object):
    VERSION = '1.0'
    IS_MEMOIZABLE = True

    def _trace(self, methodName):
        
        if TRACE_STAT[methodName]:
            if not hasattr(Statistic, 'objAddresses'):
                Statistic.objAddresses = {}

            if not hasattr(self, '_traceId'):
                if not self.__class__.__name__ in Statistic.objAddresses:
                    Statistic.objAddresses[self.__class__.__name__] = 0
                self._traceId = str(Statistic.objAddresses[self.__class__.__name__])
                Statistic.objAddresses[self.__class__.__name__] += 1
            
            logMessage(  self.__class__.__name__ + '(' + self._traceId + ').' + methodName \
                  + ( (' (' + str(self._region) +')') if TRACE_STAT['printRegions'] else '') \
                  + ( ( ' (' + str(self._track.trackName) \
                  + (',' + str(self._track2.trackName) if hasattr(self,'_track2') else '') \
                  + ')' ) if TRACE_STAT['printTrackNames'] else '') )

    def __init__(self, region, track, track2=None, *args, **kwArgs):
        from config.Config import IS_EXPERIMENTAL_INSTALLATION
        if 'isExperimental' in kwArgs:
            x = kwArgs['isExperimental'].lower()
            if not x in ['false','true']:
                logMessage('isExperimental has value other than false/true', level=logging.WARN)
                raise ShouldNotOccurError('isExperimental has value other than false/true.')
            if x=='true':
                assert IS_EXPERIMENTAL_INSTALLATION
        #else:
        #    assert IS_EXPERIMENTAL_INSTALLATION
                
        if 'assumptions' in kwArgs:
            self._checkAssumptions(kwArgs['assumptions'])
            
        self._region = region
        self._track = track
        if track2 not in [None, []]:
            if track.trackName == track2.trackName:
                #if not kwArgs.get('allowIdenticalTracks') in [True,'True']: #Does not work, as all kwArgs are not sent further down in createChildren, meaning that a base statistic like RawDataStat would not find allowIdenticalTracks and throw exception..
                #if not IS_EXPERIMENTAL_INSTALLATION: #does not work either, as results in: gold.util.CustomExceptions.IncompatibleTracksError: Track 'Unmarked segments (Sample tracks)'was created, but not touched by statistic
                from gold.util.CustomExceptions import IdenticalTrackNamesError
                raise IdenticalTrackNamesError("Track names are identical. Track name = " + ':'.join(track.trackName))
            self._track2 = track2
        self._kwArgs = kwArgs

        self._init(**kwArgs)

        self._trace('__init__')
        #self._loadMemoized()
        
        #removed _result and _children entirely, to mark difference between not created and None/empty.
        #self._result = None
        #self._children = None
        
    def _init(self, **kwArgs):
        pass

    def _checkAssumptions(self, assumptions):
        pass

    def getDescription(self):
        import gold.description.StatDescriptionList as StatDescrModule
        statClassName = getClassName(self).replace('Unsplittable','')
        #statClassName = cls.__name__

        if statClassName == 'RandomizationManagerStat':
            assert hasattr(self, 'getRawStatisticMainClassName')
            statClassName += '_' + self.getRawStatisticMainClassName()
            
        if not statClassName in vars(StatDescrModule):
            return 'No description available.'
        assert type(vars(StatDescrModule)[statClassName]) is str
        return vars(StatDescrModule)[statClassName]
        
    @exceptionLogging(level=logging.WARNING)
    def _loadMemoized(self):
        self.resultLoadedFromDisk = False
        try:
            ResultsMemoizer.loadResult(self)
        except IOError, e:
            logMessageOnce('No memoization due to IOError (probably because some other process are writing same data): ' + str(e))
            #raise #NB! Remove, only for debugging..
            #logging.getLogger(HB_LOGGER).debug('No memoization due to IOError (probably because some other process are writing same data): ' + str(e))
        except AssertionError, e:
            logMessageOnce('No memoization due to assertionError (probably missing formatConverter): ' + str(e))
            #raise #NB! Remove this, only for debugging..
            #logging.getLogger(HB_LOGGER).debug('No memoization due to assertionError (probably missing formatConverter): ' + str(e))
            
    #def _loadMemoized(self):
    #    self.resultLoadedFromDisk = False
    #    try:
    #        ResultsMemoizer.loadResult(self)
    #    except AssertionError, e:
    #        logging.getLogger(HB_LOGGER).debug('No memoization due to assertionError (probably missing formatConverter): ' + str(e))
    #        
    #    except Exception, e:
    #        logging.getLogger(HB_LOGGER).warning('Exception when loading memo - ' + getClassName(e) + ': ' + str(e))
    #        #logging.getLogger(HB_LOGGER).warning('TRACE: ' + traceback.format_exc())
    #        logging.getLogger(HB_LOGGER).debug(traceback.format_exc())
            
    def setMemoizedResult(self, result):
        self._result = result
        self.resultLoadedFromDisk = True
        
    def compute(self):
        self._trace('compute')
        self.createChildren()

        while not self.hasResult():
            self.computeStep()
            
    def computeStep(self):
        self._trace('computeStep')
                
        if not self.hasResult():
            self._loadMemoized()
        if self.hasResult():
            return
        
        for child in self._children:
            if not child.hasResult():
                child.computeStep()
        
        if not all([child.hasResult() for child in self._children]):
            return
        
        self._trace('_compute')
        #The method _compute may either return the result, or set the result variable directly:
        res = None
        with StatisticExceptionHandling(**self._kwArgs):
            res = self._compute()
        
        #try:
        #    self._trace('_compute')
        #    #The method _compute may either return the result, or set the result variable directly:
        #    res = self._compute()
        #
        #except (TooLargeBinError, TooSmallBinError, CentromerError),e:
        #    logException(e)
        #    raise
        #except (ZeroDivisionError, FloatingPointError, TypeError, ValueError),e:
        #    #print 'Error: ', e.__class__.__name__, e
        #    res = None
        #    if DebugConfig.VERBOSE or e.__class__ in [TypeError, ValueError]:
        #        logException(e, message='kwArgs: ' + str(self._kwArgs))
        #    if DebugConfig.PASS_ON_COMPUTE_EXCEPTIONS:
        #        raise
        
        if not self.hasResult():
            #Only set _result if this was not set directly by the previous call to _compute
            self._result = res
            
        self._storeResult()
        
    def _storeResult(self):
        try:
            ResultsMemoizer.storeResult(self)
        except IOError, e:
            #logging.getLogger(HB_LOGGER).debug('No memoization due to IOError (probably because some other process are reading/writing same data): ' + str(e))
            logExceptionOnce(e, message='No memoization due to IOError (probably because some other process are reading/writing same data) ')
            #raise
        except Exception,e :
            logExceptionOnce(e, logging.WARNING, 'Error when trying to store memoized result.')
            
                
    def afterComputeCleanup(self):
        if self.hasChildren():
            for child in self._children:
                child.afterComputeCleanup()
        
        self._trace('_afterComputeCleanup')
        self._afterComputeCleanup()

    def _afterComputeCleanup(self):
        pass

    def prepareForNewIteration(self):
        if self.hasChildren():
            for child in self._children:
                child.prepareForNewIteration()
        
        self._trace('_prepareForNewIteration')
        self._prepareForNewIteration()
    
    def _prepareForNewIteration(self):
        if self.hasResult():
            del self._result

    def setNotMemoizable(self):
        if self.hasChildren():
            for child in self._children:
                child.setNotMemoizable()
        
        self._trace('_setNotMemoizable')
        self._setNotMemoizable()

    def _setNotMemoizable(self):
        self.IS_MEMOIZABLE = False

    def updateInMemoDict(self, statKwUpdateDict):
        if self.hasChildren():
            for child in self._children:
                child.updateInMemoDict(statKwUpdateDict)
        
        self._trace('_updateInMemoDict')
        self._updateInMemoDict(statKwUpdateDict)

    def _updateInMemoDict(self, statKwUpdateDict):
        from gold.statistic.MagicStatFactory import MagicStatFactory
        MagicStatFactory.updateMemoDict(self, statKwUpdateDict)
        
    def createChildren(self):
        if self.hasResult() or self.hasChildren():
            return

        self._setNoChildren()
        
        self._trace('_createChildren')
        self._createChildren()
        for child in self._children:
            child.createChildren()
    
    def getResult(self):
        if not self.hasResult():
            self.compute()
        if self._result is None:
            raise NoneResultError('None returned from statClass: ' + self.__class__.__name__)
        #logMessage(self.__class__.__name__ + ' ' + str(self._result))
        return self._result

    def hasResult(self):
        return hasattr(self, '_result')

    def hasChildren(self):
        return hasattr(self, '_children')
    
    def _setNoChildren(self):
        self._children = []

    def _addChild(self, child):
        if not self.hasChildren():
            self._setNoChildren()
        self._children.append(child)
        return child

    def _combineResults(self):
        raise ShouldNotOccurError()
        
    def __cmp__(self, other):
        return cmp(self.getUniqueKey, other.getUniqueKey)
    
    #def __hash__(self):
    #    reg = tuple(self._region) if hasattr(self._region, '__iter__') else self._region        
    #    return (self.__class__, reg, tuple(self._track.trackName), tuple(self._track2.trackName) if hasattr(self,'_track2') else '').__hash__()
    
    def getUniqueKey(self):
        #reg = tuple(self._region) if hasattr(self._region, '__iter__') else self._region        
        #return (self.__class__, reg, tuple(self._track.trackName), tuple(self._track2.trackName) if hasattr(self,'_track2') else '')
        return Statistic.constructUniqueKey(self.__class__, self._region, self._track, \
                                            self._track2 if hasattr(self,'_track2') else None, **self._kwArgs)

    def getConfigKey(self):
        return Statistic._constructConfigKey(self._kwArgs)

    @staticmethod
    def _constructConfigKey(configDict):
        return hash( tuple( [configDict[key] for key in sorted(configDict.keys())] ) )


    # NOTE:
    # Keep in mind that the key has to be unique across interpreters and machines
    # Therefore each element used in the hash has to be portable - do not try to hash
    # magical objects like None, as the hash value is implementation specific
    # The same goes for hashing objects (like cls)
    @staticmethod
    def constructUniqueKey(cls, region, track, track2=None, *args, **kwArgs):
        #If only one track is provided to a stat, other params may turn up as track2 above. Then set to None..
        if track2!=None and not isinstance(track2, Track):
            track2 = None
            
        reg = id(region) if isIter(region) else region

        #logMessage('%s, %s, %s, %s, %s' % (str(cls), Statistic._constructConfigKey(kwArgs), (str([str(x) for x in reg]) if hasattr(reg, '__iter__') else str(reg)), tuple(track.trackName), tuple(track2.trackName) if track2 != None else ''))
        return (hash(str(cls)), Statistic._constructConfigKey(kwArgs), hash(reg), tuple(track.trackName), tuple(track2.trackName) if track2 != None else '')
        
    def getGenome(self):
        if isinstance(self._region, GenomeRegion):
            return self._region.genome
        else:
            for reg in self._region:
                return reg.genome
            
    @classmethod
    def validateAndPossiblyResetLocalResults(cls, stats):
        #return True
        return 0
    @classmethod
    def validateAndPossiblyResetGlobalResult(cls, stat):
        return 0
    
    @staticmethod
    def getRawStatisticClass(rawStatistic):
        if type(rawStatistic) is str:
            from gold.statistic.AllStatistics import STAT_CLASS_DICT
            rawStatistic = STAT_CLASS_DICT[rawStatistic]
        return rawStatistic

    def _configuredToAllowOverlaps(self, strict=True):
        withOverlaps = self._kwArgs.get('withOverlaps')        
        if strict:
            assert withOverlaps in ['yes','no'], withOverlaps
        else:
            assert withOverlaps in ['yes','no',None], withOverlaps            
        return withOverlaps == 'yes'

class StatisticSplittable(Statistic):
    #IS_MEMOIZABLE = False
    
    def __init__(self, region, track, *args, **kwArgs):
        Statistic.__init__(self, region, track, *args, **kwArgs)
        self._args = args
        #self._kwArgs = kwArgs
        self._childResults = []
        self._bins = self._splitRegion()
        #self._binIndex = 0
        self._curChild = None
        
    def createChildren(self):
        if self.hasResult() or self._curChild is not None:
            return
        self._trace('_createChildren')
        #logMessage(str(self._bins))
        try:
            self._curChild = self._getChildObject(self._bins.next())
        except StopIteration,e:
            logException(e)
            raise ShouldNotOccurError('Splittable statistic should not have zero bins!')
        self._curChild.createChildren()

    def _compute(self):
        raise ShouldNotOccurError()
    
    def _splitRegion(self):
        if isIter(self._region):
            #return self._region.__iter__()
            return self._region.__iter__()
        else:
            return CompBinManager.splitUserBin(self._region).__iter__()
        
    def computeStep(self):
#        if self.hasResult():
#            return
        
        self._trace('computeStep')
        try:
            try:
                if not self._curChild.hasResult():
                    self._curChild.computeStep()
                if not self._curChild.hasResult():
                    return
                nextRes = self._curChild.getResult()
            except NoneResultError:
                nextRes = None
                if DebugConfig.PASS_ON_NONERESULT_EXCEPTIONS:
                    raise

            self._childResults.append(nextRes)
            tempRefHolderChild = self._curChild # To avoid children of this _curChild to be collected in the next line.
                                                # It will live long enough for createChildren to be called on new _curChild
            self._curChild = None #first sets curchild to None to free memory even when self._bins.next() raises StopIteration..
            self._curChild = self._getChildObject(self._bins.next())

            self._curChild.createChildren()
            #self._binIndex += 1
        except StopIteration:
            #if self._binIndex == len(self._bins):
            self._trace('_combineResults')
            
            with StatisticExceptionHandling(**self._kwArgs):
                ret = None
                ret = self._combineResults()
            
            if not self.hasResult():
                self._result = ret
            del self._bins
        
    def afterComputeCleanup(self):
#        assert self._curChild is None, 'Error with: ' + getClassName(self) +' '+str(self._track.trackName) + (' '+str(self._track2.trackName) if hasattr(self, '_track2') else '')
        if hasattr(self, '_childResults'):
            del self._childResults
           
    def _prepareForNewIteration(self):
        self._curChild = None
        self._bins = self._splitRegion()
        self._childResults = []
        del self._result
        self.createChildren()
    
    def _getChildObject(self, bin):
        childName = getClassName(self).replace('Splittable','')
        try:
            module = __import__('.'.join(['gold','statistic',childName]),globals(), locals(), [childName])
        except:
            module = __import__('.'.join(['quick','statistic',childName]),globals(), locals(), [childName])
        
        return getattr(module, childName)(bin, self._track, *self._args, **self._kwArgs)

class StatisticExceptionHandling(object):
    def __init__(self, **kwArgs):
        self._kwArgs = kwArgs

    def __enter__(self):
        pass
        
    def __exit__(self, type, value, traceback):
        if type in [TooLargeBinError, TooSmallBinError, CentromerError]:
            logException(value)
        
        if type in [ZeroDivisionError, FloatingPointError, TypeError, ValueError, OutsideBoundingRegionError]:
            if DebugConfig.VERBOSE or type in [TypeError, ValueError]:
                logException(value, message='kwArgs: ' + str(self._kwArgs))
                return True
            if not DebugConfig.PASS_ON_COMPUTE_EXCEPTIONS:
                return True

class StatisticSumResSplittable(StatisticSplittable):
    def _combineResults(self):
        self._result = smartSum(self._childResults)
#        print self._childResults, self._result
    
#Assumes all dicts have same keys (or dict is None)
class StatisticDictSumResSplittable(StatisticSplittable):
    def _combineResults(self):
        self._result = OrderedDict([ (key, smartSum([res[key] for res in self._childResults])) for key in self._childResults[0] ])

#Assumes all lists are of same length
class StatisticListSumResSplittable(StatisticSplittable):
    def _combineResults(self):
        import numpy
        numpyMatrix = numpy.array(self._childResults) #self._childResults is assumed to be list of lists
        self._result = list(numpyMatrix.sum(axis=0))

class StatisticDynamicDictSumResSplittable(StatisticSplittable):
    def _combineResults(self):
        allKeys = reduce(lambda l1,l2:l1+l2, [childDict.keys() for childDict in self._childResults])
        uniqueKeys = set(allKeys)
        self._result = OrderedDict([ (key, smartSum([res.get(key) for res in self._childResults])) for key in uniqueKeys ])
        return self._result

class StatisticDynamicDoubleDictSumResSplittable(StatisticSplittable):
    def _combineResults(self):
        res = OrderedDict()
        for childDict in self._childResults:
            for key1 in childDict.keys():
                if key1 not in res:
                    res[key1] = copy(childDict[key1])
                else:
                    for key2 in childDict[key1]:
                        if key2 in res[key1]:
                            res[key1][key2] = smartSum((res[key1][key2], childDict[key1][key2]))
                        else:
                            res[key1][key2] = childDict[key1][key2]
        self._result = res
        return self._result

#class StatisticDictUnionResSplittable(StatisticSplittable):
#    def _combineResults(self):
#        res = {}
#        for childDict in self._childResults:
#            res.update(childDict)
#        return res

class StatisticNumpyMatrixSplittable(StatisticSplittable):
    MAX_MATRICES_AT_ONCE = 10

    def _combineResults(self):
        return self._combineMatrices(self._childResults)

    def _combineMatrices(self, matrixDictList):
        combinedMatrices = []
        for i in range(int(ceil(1.0 * len(matrixDictList) / self.MAX_MATRICES_AT_ONCE))):
            combinedMatrices.append(self._combineMatricesFromSmallLists\
                                    (matrixDictList[i*self.MAX_MATRICES_AT_ONCE:(i+1)*self.MAX_MATRICES_AT_ONCE]))
        if len(combinedMatrices) == 1:
            return combinedMatrices[0]
        else:
            return self._combineMatrices(combinedMatrices)
    
    def _combineMatricesFromSmallLists(self, matrixDictList):
        #print matrixDictList
        if len(matrixDictList) == 1:
            return matrixDictList[0]
        matrixDictList = [x for x in matrixDictList if x is not None]
        allN, allM = (numpy.array([x['Result']['Matrix'].shape[i] for x in matrixDictList]) for i in [0,1])
        allN = numpy.add.accumulate(allN)
        allM = numpy.add.accumulate(allM)
        assert len(allN) == len(allM)
        if len(allN) == 0:
            return None
        
        matrix = numpy.zeros(shape=(allN[-1], allM[-1]), dtype='uint32')
    
        for i in range(len(allN)):
            matrix[numpy.ix_(range(allN[i-1] if i >= 1 else 0, allN[i]),
                             range(allM[i-1] if i >= 1 else 0, allM[i]))] = matrixDictList[i]['Result']['Matrix']
    
        allRows = numpy.concatenate([x['Result']['Rows'] for x in matrixDictList])
        allCols = numpy.concatenate([x['Result']['Cols'] for x in matrixDictList])

        rowSortIndexes = allRows.argsort()
        colSortIndexes = allCols.argsort()

        matrix = matrix[numpy.ix_(rowSortIndexes, colSortIndexes)]
        allRows = allRows[rowSortIndexes]
        allCols = allCols[colSortIndexes]

        uniqueRows = numpy.unique(allRows)
        uniqueCols = numpy.unique(allCols)
    
        matrix = numpy.array([matrix[allRows==row].sum(axis=0) for row in uniqueRows])
        matrix = numpy.array([matrix[:,allCols==col].sum(axis=1) for col in uniqueCols]).transpose()

        return {'Result': OrderedDict([('Matrix', matrix), ('Rows', uniqueRows), ('Cols', uniqueCols)])}

class StatisticConcatResSplittable(StatisticSplittable):
    def _combineResults(self):
        #self._result = reduce(lambda l1,l2:l1+l2, [childResult for childResult in self._childResults])
        self._result = reduce(lambda l1,l2:l1+l2, self._childResults)

class StatisticConcatDictOfListResSplittable(StatisticSplittable):
    def _combineResults(self):
        res = OrderedDict()
        for key in self._childResults[0]:
            res[key] = reduce(lambda l1,l2:l1+l2, [result[key] for result in self._childResults])
        return res
        
class StatisticConcatNumpyArrayResSplittable(StatisticSplittable):
    def _combineResults(self):
        #self._result = reduce(lambda l1,l2:l1+l2, [childResult for childResult in self._childResults])
        self._result = numpy.concatenate([result for result in self._childResults if result is not None])

class StatisticConcatDictOfNumpyArrayResSplittable(StatisticSplittable):
    def _combineResults(self):
        res = OrderedDict()
        for key in self._childResults[0]:
            res[key] = numpy.concatenate([result[key] for result in self._childResults if result is not None])
        return res

class StatisticConcatDictResSplittable(StatisticSplittable):
    def _combineResults(self):
        #self._result = reduce(lambda l1,l2:l1+l2, [childResult for childResult in self._childResults])
        self._result = {}
        for d in self._childResults:            
            self._result.update(d)
            
        
class StatisticDynamicDictSumOnlyValuesResSplittable(StatisticDynamicDictSumResSplittable, StatisticConcatResSplittable):
    def _combineResults(self):
        self._result = StatisticDynamicDictSumResSplittable._combineResults(self).values()
        return self._result
    
class OnlyGloballySplittable():
    pass

class RatioStatUnsplittable(Statistic):    
    def _compute(self):
        return 1.0 * self._children[0].getResult() / self._children[1].getResult()
                
    def _createChildren(self):
        raise AbstractClassError
    
class RatioDictSingleDenomStatUnsplittable(Statistic):
    def _compute(self):
        res = OrderedDict()
        c1res = self._children[0].getResult()
        for key in c1res:
            res[key] = 1.0 * c1res[key] / self._children[1].getResult()
        return res
                
    def _createChildren(self):
        raise AbstractClassError

class MultipleRawDataStatistic(Statistic):
    def _collectTracks(self):
        tracks = [self._track, self._track2]
        if 'trackNameIntensity' in self._kwArgs:
            assert not 'extraTracks' in self._kwArgs
            self._kwArgs['extraTracks'] = self._kwArgs['trackNameIntensity']
            
        if 'extraTracks' in self._kwArgs:
            from gold.track.Track import PlainTrack
            import re
            from config.Config import MULTIPLE_EXTRA_TRACKS_SEPARATOR
            extraTracks = self._kwArgs['extraTracks']
            if type(extraTracks) == str:
                extraTracks = extraTracks.split(MULTIPLE_EXTRA_TRACKS_SEPARATOR)
            for extraT in extraTracks:
                if type(extraT) == str:
                    #extraT = extraT.split('|')
                    #extraT = re.split('\^|\|',extraT)                    
                    extraT = convertTNstrToTNListFormat(extraT)
                if type(extraT) == list:
                    #print 'TEMP1: ', extraT
                    from urllib import unquote
                    extraT = [unquote(part) for part in extraT]
                    from quick.application.ExternalTrackManager import ExternalTrackManager
                    if ExternalTrackManager.isGalaxyTrack(extraT):
                        extraT = ExternalTrackManager.getPreProcessedTrackFromGalaxyTN(self.getGenome(), extraT)
                    extraT = PlainTrack(extraT)
                    tracks.append(extraT)
                
        return tracks
                
            #suppliedT3 = self._kwArgs['trackNameIntensity']
            #if type(suppliedT3) == str:
                #if suppliedT3 == 'test':
                #    print 'WARNING! USING FIXED TEST DATA AS TRACK 3 - Sample tracks|Unmarked segments'
                #    suppliedT3 = 'Sample tracks|Unmarked segments'
                #print 'Using as third track - ', suppliedT3
                #t3 = suppliedT3.split('|')

            #else:
            #    intensityTrack = suppliedT3
            #self._addChild( RawDataStat(self._region, intensityTrack, TrackFormatReq(dense=False)) )
            
    def _getTrackFormatReq(self):
        return AbstractClassError

    def _createChildren(self):
        from gold.statistic.RawDataStat import RawDataStat
        
        for track in self._collectTracks():
            self._addChild( RawDataStat(self._region, track, self._getTrackFormatReq() ) )