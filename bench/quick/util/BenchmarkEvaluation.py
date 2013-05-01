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
from quick.application.GalaxyInterface import GalaxyInterface
from quick.util.StatisticPlot import StatisticPlot
from collections import OrderedDict
from quick.util.StaticFile import GalaxyRunSpecificFile

'''
Sets up and runs statistics on a given benchmark.
'''
class BenchmarkEvaluation():
    
    def __init__(self, galaxyFn, username, genome):
        
        self._galaxyFn = galaxyFn
        self._username = username
        self._genome = genome
    
    '''
    Checks if the prediction file uses valued segments, 
    so that it can be evaluated using a ROC curve.
    
    PARAMETERS
    
    predictionTrackName: string containing the track name of the prediction file
    
    RETURNS
    
    True if the prediction file is compatible with ROC Curves, False otherwise
    '''
    def _isRocCurveCompatible(self, predictionTrackName):
        
        predictionFile = predictionTrackName.split(':')[2]
        predfile = open(predictionFile, 'r')
        lines = predfile.readlines(20)
        
        for line in lines:
            
            if "valued segments" in line.lower():
                return True

        return False
    
    '''
    Finds an returns the total negatives and total positives in an answer given
    the results from an overlap stat run.
    
    PARAMETERS
    
    overlapResults: list with the results from an overlap statistic.
    
    RETURNS
    
    Floating values with total negatives and totalnegatives
    '''
    def _getTotalNegativesAndPositivesFromOverlapResults(self, overlapResults):
        overlapResult = overlapResults[0]
        
        tn = overlapResult['Neither']
        fp = overlapResult['Only1']
        fn = overlapResult['Only2']
        tp = overlapResult['Both']
        
        totalPositives = float(tp+fn)
        totalNegatives = float(tn+fp)
        
        return totalPositives, totalNegatives
    
    '''
    Runs a statistic on a single test set for a single prediction.
    
    PARAMETERS
    
    regionTrackName:        string of one region track name
    analysisDef:            string specifying the statistic we want to run
    predictionTrackName:    string of one prediction track name
    answerTrackName:        string of one answer track name 
    
    RETURNS
    
    A result object containing the result of the statistic run
    '''
    def _runSingleStatistic(self, regionTrackName, analysisDef, predictionTrackName, answerTrackName=None):
        splittedPredictionTrackName = predictionTrackName.split(':')
        regionFileName = regionTrackName.split(':')[2]
        
        if answerTrackName == None:
            resultObject = GalaxyInterface.runManual([splittedPredictionTrackName], 
                        analysisDef, 'gtrack', regionFileName, self._genome, username=self._username, 
                        printResults=False, printHtmlWarningMsgs=False)
        else:
            splittedAnswerTrackName = answerTrackName.split(':')
        
            resultObject = GalaxyInterface.runManual([splittedPredictionTrackName, splittedAnswerTrackName], 
                        analysisDef, 'gtrack', regionFileName, self._genome, username=self._username, 
                        printResults=False, printHtmlWarningMsgs=False)
        
        return resultObject.getGlobalResult()
    
    '''
    Evaluates and creates statistics for one or more prediction on a single test set,
    for a Function Track benchmark
    
    PARAMETERS
    
    algorithmNames:       list of strings containing the names of the algorithms used in the benchmark
    predictionDict:       OrderedDict of prediction track name strings for all predictions
    answerTrackName:      string of answer track name
    regionTrackName:      string of region track name
    functionAnalysisDef:  string containing the function analysis statistic to run
    ROCanalysisDef:       string containing the ROC analysis statistic to run
    scoreDistributionDef: string containing the score distribution statistic to run
    
    RETURNS
    
    A list containing a link to statistics
    '''
    def runFunctionTrackEvaluationStatistic(self, algorithmNames, predictionDict, 
            answerTrackName, regionTrackName, functionAnalysisDef, ROCanalysisDef, scoreDistributionDef):
        
        statPlot = StatisticPlot()
        statisticResults = []
        rocResults = []
        distributionResults = []
        
        for predictionTrackName in predictionDict.itervalues():
            
            statisticResult = self._runSingleStatistic(regionTrackName, 
                                functionAnalysisDef, predictionTrackName, answerTrackName)
            
            statisticResults.append(statisticResult)
            
            rocResult = self._runSingleStatistic(regionTrackName, ROCanalysisDef,
                            predictionTrackName, answerTrackName)
            
            rocResults.append(rocResult)
            
            
            distributionResult = self._runSingleStatistic(regionTrackName, scoreDistributionDef,
                            predictionTrackName, answerTrackName)
            
            distributionResults.append(distributionResult)
        
        
        functionStatisticLink = statPlot.createFunctionAnalysisStatistic(algorithmNames, 
                    statisticResults, self._galaxyFn, 'Benchmark results')
        
        totalPositives = statisticResults[0]['Result'][0]
        totalNegatives = statisticResults[0]['Result'][1]

        rocCurveLink = statPlot.createROCCurve(1, algorithmNames, 
                            totalPositives, totalNegatives, rocResults, self._galaxyFn)
        
        
        distributionLinks = statPlot.createScoreDistributionStatistic(algorithmNames, 
                                            distributionResults, self._galaxyFn)
        
        result = [functionStatisticLink, rocCurveLink]
        
        for link in distributionLinks:
            result.append(link)
        
        return result
    
    '''
    Evaluates and creates statistics for one or more predictions on a single test set, 
    for a binary classification benchmark.
    
    PARAMETERS
    
    algorithmNames:     list of strings containing the names of the algorithms used in the benchmark
    predictionDict:     OrderedDict of prediction track name strings for all predictions
    answerTrackName:    string of answer track name
    regionTrackName:    string of region track name
    overlapAnalysisDef: string defining the overlap statistic to run
    ROCAnalaysisDef:    string defining the ROC statistic to run
    
    RETURNS
    
    A list containing one link to statistics and one link to the ROC curve
    '''
    def runBinaryClassificationEvaluation(self, algorithmNames, 
            predictionDict, answerTrackName, regionTrackName, overlapAnalysisDef, ROCanalysisDef):
        
        statPlot = StatisticPlot()
        overlapResults = []
        rocResults = []
        
        # For every prediction track name...
        for predictionTrackName in predictionDict.itervalues():
            # Run the statistics on this prediction track names
            overlapResult = self._runSingleStatistic(regionTrackName, overlapAnalysisDef,
                        predictionTrackName, answerTrackName)
            
            # Check if we can evaluate this prediction using a ROC Curve
            if self._isRocCurveCompatible(predictionTrackName):
                rocResult = self._runSingleStatistic(regionTrackName, ROCanalysisDef,
                            predictionTrackName, answerTrackName)
            else:
                rocResult = None
            
            # Append results
            overlapResults.append(overlapResult)
            rocResults.append(rocResult)
        
        # Create statistics for this test set and return
        statisticsLink = statPlot.createBinaryClassificationStatistics(1, 
                algorithmNames, overlapResults, self._galaxyFn, 'Benchmark statistics')
        
        totalPositives, totalNegatives = self._getTotalNegativesAndPositivesFromOverlapResults(overlapResults)
        
        rocCurveLink = statPlot.createROCCurve(1, algorithmNames, 
                            totalPositives, totalNegatives, rocResults, self._galaxyFn)
        
        return [statisticsLink, rocCurveLink]

    '''
    Evaluates and creates statistics for one or more predictions on several test sets.
    
    PARAMETERS
    
    algorithmNames:         list of strings containing the names of the algorithms used in the benchmark
    predictionTrackNames:   list of prediction track name strings for all predictions
    answerTrackNames:       list of answer track name strings for all answers
    regionTrackNames:       list of region track name strings for all regions
    overlapAnalysisDef:     string defining the overlap statistic to run
    ROCAnalaysisDef:        string defining the ROC statistic to run
    
    RETURNS
    
    A list containing links to result files, which contains one link to statistics and one link to the ROC curve
    '''
    def runBinaryClassificationSuiteEvaluation(self, algorithmNames, predictionTrackNames, 
                    answerTrackNames, regionTrackNames, overlapAnalysisDef, ROCanalysisDef):
        
        # Number of test sets and number of algorithms to evaluate
        nTestSets = len(answerTrackNames)
        nAlgorithms = len(predictionTrackNames)/nTestSets
        # Initialize list data structures
        resultFiles = []
        globalOverlapResults = []
        globalEqOverlapResults = []
        globalRocResults = []
        tmpAlgorithmNames = []
        number = 1000000000000
        
        statPlot = StatisticPlot()
        globalResultFile = GalaxyRunSpecificFile(['globalResults.html'], self._galaxyFn)
        
        # Initialize the global result lists, which collects localResults across all test sets
        for i in range(0, nAlgorithms):
            
            tmpAlgorithmNames.append(algorithmNames[i*nTestSets])
            globalOverlapResults.append(OrderedDict(zip(['Neither','Only1','Only2','Both'] , (0,0,0,0))))
            globalEqOverlapResults.append(OrderedDict(zip(['Neither','Only1','Only2','Both'] , (0,0,0,0))))
            globalRocResults.append({'Result': []})
        
        algorithmNames = tmpAlgorithmNames
        
        # For all test sets...
        for i in range(0, nTestSets):
            # Create a result file for this test set
            resultFile = GalaxyRunSpecificFile(['testset%d.html' % i], self._galaxyFn)
            localOverlapResults = []
            localRocResults = []
            answerTrackName = answerTrackNames[i]
            regionTrackName = regionTrackNames[i]
            
            # Evaluate the predictions for every algorithm for this test set
            for j in range(0, nAlgorithms):
                predictionTrackName = predictionTrackNames[(j*nTestSets)+i]
                
                # Run statistics for to compute overlap and ROC values
                localOverlapResult = self._runSingleStatistic(regionTrackName, overlapAnalysisDef,
                                    predictionTrackName, answerTrackName)
                
                if self._isRocCurveCompatible(predictionTrackName):
                    localRocResult = self._runSingleStatistic(regionTrackName, ROCanalysisDef,
                                                    predictionTrackName, answerTrackName)
                else:
                    localRocResult = None
                
                # Collect the local results and global add to global results
                localOverlapResults.append(localOverlapResult)
                localRocResults.append(localRocResult)
                
                globalOverlapResults[j]['Neither'] = globalOverlapResults[j]['Neither'] + localOverlapResult['Neither']
                globalOverlapResults[j]['Only1'] = globalOverlapResults[j]['Only1'] + localOverlapResult['Only1']
                globalOverlapResults[j]['Only2'] = globalOverlapResults[j]['Only2'] + localOverlapResult['Only2']
                globalOverlapResults[j]['Both'] = globalOverlapResults[j]['Both'] + localOverlapResult['Both']
                
                testSetLength = localOverlapResult['Neither'] + localOverlapResult['Only1'] + localOverlapResult['Only2'] + localOverlapResult['Both']
                
                globalEqOverlapResults[j]['Neither'] = globalEqOverlapResults[j]['Neither'] + long(localOverlapResult['Neither']*number)/testSetLength
                globalEqOverlapResults[j]['Only1'] = globalEqOverlapResults[j]['Only1'] + long(localOverlapResult['Only1']*number)/testSetLength
                globalEqOverlapResults[j]['Only2'] = globalEqOverlapResults[j]['Only2'] + long(localOverlapResult['Only2']*number)/testSetLength
                globalEqOverlapResults[j]['Both'] = globalEqOverlapResults[j]['Both'] + long(localOverlapResult['Both']*number)/testSetLength
                
                if localRocResult != None:
                    globalRocResults[j]['Result'] = globalRocResults[j]['Result'] + localRocResult['Result']
            
            # Create statistics for this test set
            localStatisticsLink = statPlot.createBinaryClassificationStatistics(i, 
                    algorithmNames, localOverlapResults, self._galaxyFn, 'Benchmark statistics')
            
            totalPositives, totalNegatives = self._getTotalNegativesAndPositivesFromOverlapResults(localOverlapResults)
        
            localRocCurveLink = statPlot.createROCCurve(i, algorithmNames, 
                            totalPositives, totalNegatives, localRocResults, self._galaxyFn)
            
            # Write statistical information for this test set to file
            resultFile.writeTextToFile('%s</br>%s' % (localStatisticsLink, localRocCurveLink), 'w')
            resultFiles.append(resultFile)
        
        # Create statistics for all test sets
        globalStatisticsLink = statPlot.createBinaryClassificationStatistics(nTestSets, 
                    algorithmNames, globalOverlapResults, self._galaxyFn, 
                    'Benchmark statistics (sum, longer test set has higher weight)')
        
        globalEqStatisticsLink = statPlot.createBinaryClassificationStatistics(nTestSets+1, 
                    algorithmNames, globalEqOverlapResults, self._galaxyFn, 
                    'Benchmark statistics (same weight for each test set)')
        
        totalPositives, totalNegatives = self._getTotalNegativesAndPositivesFromOverlapResults(globalOverlapResults)
        
        globalRocCurveLink = statPlot.createROCCurve(nTestSets, algorithmNames, 
                            totalPositives, totalNegatives, globalRocResults, self._galaxyFn)
        
        # Write statistical information for all test sets to file
        globalResultFile.writeTextToFile('%s</br>%s</br>%s' % (globalStatisticsLink, globalEqStatisticsLink, globalRocCurveLink), 'w')
        
        # Add all result files to a result list, and return
        results = []
        
        results.append(globalResultFile.getLink('Global results\n\n'))
        
        for i in range(0, len(resultFiles)):
            results.append(resultFiles[i].getLink('Test set %d' % (i+1)))
        
        return results
