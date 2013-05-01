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
from gold.util.CommonFunctions import getClassName, isIter
from gold.description.ResultInfo import ResultInfo
#from gold.application.RSetup import r
import numpy
import re
from quick.application.SignatureDevianceLogging import takes,returns
from collections import OrderedDict
from gold.result.ResultTypes import GlobalVisualizationResultType, LinePlotResultType, RawVisualizationResultType
from gold.track.TrackView import TrackView

class Results(dict):
    '''
    A class holding the result of a run of a statistic (through AnalysisDefJob/StatJob).
    Can be visualized by sending in to ResultsViewer/ResultsViewerCollection and calling print on the resulting object
    '''
    
#friend: ResultsViewer
    FDR_KEY = 'fdr'
    FDR_THRESHOLD = 0.1
    PVALUE_THRESHOLD = 0.05

    def __init__(self, trackName1, trackName2, statClassName):
        self._errors = []
        self._globalResult = None
        self._resDictKeys = None
        self._trackName1 = trackName1
        self._trackName2 = trackName2
        self._statClassName = statClassName
        self._analysis = None        
        self._analysisText = None #not needed anymore..
        self._runDescription = None
        self._resultInfo = ResultInfo(trackName1, trackName2, statClassName)
        dict.__init__(self)
    
    def setAnalysis(self, analysis): 
        self._analysis = analysis
        
    #probably obsolete
    def setAnalysisText(self, analysisText): 
        self._analysisText = analysisText
        
    def setRunDescription(self, descr):
        self._runDescription = descr
        
    def includeAdditionalResults(self, other, ensureAnalysisConsistency=True):
        if ensureAnalysisConsistency:
            raise NotImplementedError
        
        assert len( set(self.getResDictKeys()).intersection(other.getResDictKeys()) ) == 0
        
        if self._globalResult is None or len(self._globalResult) == 0:
            #What is this used for?
            resKeys = self.getResDictKeys()
            self._globalResult = OrderedDict(zip(resKeys, [None]*len(resKeys)))
        
        if len(self._globalResult) == 0:
            return
        
        if other._globalResult is not None:
            self._globalResult.update(other._globalResult)
        
        for key in self:
            self[key].update(other.get(key))
        
        self._errors += other._errors
        self._resDictKeys = None #reset..
        
    def setGlobalResult(self, result):
        self._globalResult = result

    def complementGlobalResult(self, result):        
        if result is None:
            return
        assert type(result) in [dict, OrderedDict]

        if self._globalResult is None:
            self._globalResult = {}
        assert len( set(self._globalResult.keys()).intersection(set(result.keys())) ) == 0
        self._globalResult.update(result)
    
    def addError(self, exception):
        self._errors.append(exception)
    
    def getAllValuesForResDictKey(self, resDictKey):
        return [ self[reg].get(resDictKey) for reg in self.getAllRegionKeys() ]
    
    def isEmpty(self):
        return self._globalResult is None and len(self.keys()) == 0
        
    def getResDictKeys(self):
        if self._resDictKeys is None:
            if self.isEmpty():
                if len(self._errors)>0:
                    #as the result has some errors set, these should be allowed to propagate even without resDictKeys
                    return []
                else:
                    raise Exception('Error: empty results and thus nothing to display')
            isOrdered = False
            if self._globalResult not in [None,{}]:
                isOrdered = (type(self._globalResult) == OrderedDict)
                keys = self._globalResult.keys()
                
            elif len(self.keys()) > 0:
                for val in self.values():
                    if val is not {}:
                        isOrdered = (type(self.values()[0]) == OrderedDict)
                        keys = self.values()[0].keys()
                        break
                else:
                    keys = []
            else:
                keys = []
                
            ASSEMBLY_GAP_KEY = 'Assembly_gap_coverage'
            
            pairs = [(self._resultInfo.getColumnLabel(key),key) for key in keys if not key==ASSEMBLY_GAP_KEY]
            if not isOrdered:
                pairs = sorted(pairs)
                
            if ASSEMBLY_GAP_KEY in keys and len(keys) > 0:
                pairs.append( (self._resultInfo.getColumnLabel(ASSEMBLY_GAP_KEY),ASSEMBLY_GAP_KEY) )
                
            self._resDictKeys = [key for label,key in pairs]
        return self._resDictKeys
        
    def getAllRegionKeys(self):
        return sorted(self.keys())
    
    def getGlobalResult(self):
        return self._globalResult

    def getLabelHelpPair(self, resDictKey):
        return self._resultInfo.getColumnLabel(resDictKey), self._resultInfo.getHelpText(resDictKey)
    
    def getLabelHelpPairs(self):
        return [self.getLabelHelpPair(key) for key in self.getResDictKeys()]
        
    def getStatClassName(self):
        return self._statClassName
    
    def getAnalysis(self):
        return self._analysis

    def getTrackNames(self):
        return self._trackName1, self._trackName2

    def getAllErrors(self):
        return self._errors

    def getPresCollectionType(self):
        #print 'self.getGlobalResult(): ',self.getGlobalResult()
        if self.getStatClassName() == 'DataComparisonStat': #a bit ad hoc criterion. Also should check plotType...
            presCollectionType = 'scatter'
        elif 'BinScaled' in self.getStatClassName(): #a bit ad hoc criterion. Also should check plotType...
            presCollectionType = 'binscaled'
        elif self.getGlobalResult() not in [None,{}] and len(self.getGlobalResult())>0 and \
            isinstance(self.getGlobalResult().values()[0], LinePlotResultType):
                assert len(self.getGlobalResult().values()) == 1
                presCollectionType = 'lineplot'
        elif (self.getGlobalResult() not in [None,{}] and isinstance(self.getGlobalResult().values()[0], dict)):
            if self.getGlobalResult().values()[0].get('Matrix') is not None:
                presCollectionType = 'matrix'
            else:
                presCollectionType = 'dictofdicts'
        elif self.getGlobalResult() not in [None,{}] and len(self.getGlobalResult())>0 and \
            isinstance(self.getGlobalResult().values()[0], GlobalVisualizationResultType):
                assert len(self.getGlobalResult().values()) == 1, 'Should currently be one if this is visualization result'
                presCollectionType = 'visualization'
        elif self.getGlobalResult() not in [None,{}] and len(self.getGlobalResult())>0 and \
            isinstance(self.getGlobalResult().values()[0], RawVisualizationResultType):
                #assert len(self.getGlobalResult().values()) == 1, 'Should currently be one if this is visualization result'
                presCollectionType = 'rawDataVisualization'        #elif self.getGlobalResult() not in [None,{}] and len(self.getGlobalResult())==1 and \
        #    hasattr(self.getGlobalResult().values()[0], '__iter__'):
        elif self.getGlobalResult() not in [None,{}] and \
            isIter(self.getGlobalResult().values()[0]):#and len(self.getGlobalResult().values()[0])>1:
            #or type(self.getGlobalResult().values()[0])==numpy.ndarray):
                #print 'TYPE: ',type(self.getGlobalResult().values()[0])
                presCollectionType = 'distribution'
        else:
            presCollectionType = 'standard'
        #print 'presCollectionType: ',presCollectionType
        #print isinstance(self.getGlobalResult(), GlobalVisualizationResultType), type(self.getGlobalResult()), str(type(self.getGlobalResult().values()[0])).replace('<','')
        return presCollectionType

    def _getSignBins(self, pvals, threshold):        
        numSign = sum(1 for x in pvals if x <= threshold)
        numTested = sum(1 for x in pvals if not numpy.isnan(x))
        numIgnored = len(pvals) - numTested
        return numSign, numTested, numIgnored
       
    def _getSignBinsText(self, pvals, threshold):
        numSign, numTested, numIgnored = self._getSignBins(pvals, threshold)
        text = '%i significant bins out of %i, at %i' % (numSign, numTested, threshold*100) + '% FDR'
        if numIgnored > 0:
            text += ' (%i bin%s excluded)' % (numIgnored, ('' if numIgnored==1 else 's') )
        return text

    #The following methods help interprete data in results, and thus contains some definitions of semantics
    def isSignificanceTesting(self):
        return self.getPvalKey() is not None
    
    def getPvalKey(self):
        keys = self.getResDictKeys()
        if keys is not None:
            for key in keys:
                if re.search('p.*val',key.lower()) is not None:
                    return key
        return None

    def getTestStatisticKey(self):
        keys = self.getResDictKeys()
        if keys is not None:
            for key in keys:
                if re.search('test.?statistic',key.lower()) is not None or 'TSMC' in key:
                    return key
        return None

    def getExpectedValueOfTsKey(self):
        keys = self.getResDictKeys()
        if keys is not None:
            for key in keys:
                if re.search('e\(test.?statistic',key.lower()) is not None:
                    return key
        return None
    
    def inferAdjustedPvalues(self):
        pValKey = self.getPvalKey()                
        if pValKey is None or self.FDR_KEY in self.getResDictKeys():
            return

        from gold.application.RSetup import r
        
        regKeys = self.getAllRegionKeys()
        #regPVals = [ self[reg].get(pValKey) if (self[reg].get(pValKey) is not None) else numpy.nan for reg in regKeys]
        #
        #from gold.application.RSetup import r
        #regFdrVals = r('p.adjust')(r.unlist(regPVals), self.FDR_KEY)
        regPVals = [ self[reg].get(pValKey) for reg in regKeys]
        from quick.statistic.McFdr import McFdr
        McFdr._initMcFdr() #to load r libraries..
        regFdrVals = McFdr.adjustPvalues(regPVals, verbose=False)
        
        #if len(regPVals) == 1:
        #    regFdrVals = [regFdrVals]
        assert len(regFdrVals) == len(regKeys), 'fdr: ' + str(len(regFdrVals)) + ', regs: ' + str(len(regKeys))
        for i, reg in enumerate(regKeys):
            self[reg][self.FDR_KEY] = (regFdrVals[i] if regPVals[i] is not None else numpy.nan)
            
        
        if self._globalResult is None:
            keys = self.getResDictKeys()
            self._globalResult = OrderedDict(zip((keys), [None]*len(keys)))
        
        #self._globalResult[self.FDR_KEY] = self.getSignBinsText(regFdrVals, self.FDR_THRESHOLD)
        #if self._globalResult[pValKey] is None:
            #self._globalResult[pValKey] = self.getSignBinsText(regPVals, self.PVALUE_THRESHOLD)
        
        tempGlobalResult = self._globalResult
        self._globalResult = OrderedDict()
        
        self._globalResult.update([(pValKey, tempGlobalResult[pValKey])])    
        self._globalResult.update([(self.FDR_KEY, None)])
        self._globalResult.update([(key, tempGlobalResult[key]) for key in tempGlobalResult.keys() if key != pValKey])
        
        self._resDictKeys = None #resetting..
 
    def getLocalFdrValues(self):
        assert self.FDR_KEY in self.getResDictKeys()
        return [ self[reg][self.FDR_KEY] for reg in self.getAllRegionKeys()]

    @returns((int,int,int)) #numSign, numTested, numIgnored
    def getFdrSignBins(self, threshold=None):
        if threshold is None:
            threshold = self.FDR_THRESHOLD
            
        return self._getSignBins( self.getLocalFdrValues(), threshold)

    @returns(str) 
    def getFdrSignBinsText(self, threshold=None):
        if threshold is None:
            threshold = self.FDR_THRESHOLD
            
        return self._getSignBinsText( self.getLocalFdrValues(), threshold)
        
    def hasOnlyLocalPvals(self):
        pvalKey = self.getPvalKey()
        globalRes = self.getGlobalResult()
        return (pvalKey is not None) and (globalRes is None or globalRes.get(pvalKey) is None or type(globalRes.get(pvalKey)) is str) #remove last part..

    def getTestStatisticText(self):
        key = self.getTestStatisticKey()
        if key is not None:
            key
            testStatText = self._resultInfo.getHelpText(key)
            if testStatText == '':
                testStatText = self._resultInfo.getColumnLabel(key)
            return testStatText
        else:
            return None
        
    #def getAdjustedPVals(self, resDictKey, adjustMethod):
    #    pValKey = 'p-value'
    #    if not resDictKey.lower() == pValKey:
    #        return None
    #    #if not pValKey in self.getResDictKeys():
    #        #return None        
    #    fdrVals = r('p.adjust')(r.unlist(self.getAllValuesForResDictKey(resDictKey)), adjustMethod)
    #    return fdrVals
        
    #def getNumSignificantAdjustedPVals(self, resDictKey, threshold, adjustMethod):
    #    fdrVals = self.getAdjustedPVals(resDictKey, adjustMethod)
    #    if fdrVals is None:
    #        return None
    #    return sum(1 for x in fdrVals if x <= threshold)

    
    #def items(self):
    #    return sorted(dict.items(self))
    
    #def addWarning(self):
    #    pass
    
