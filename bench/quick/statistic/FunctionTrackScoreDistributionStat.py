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
from gold.statistic.MagicStatFactory import MagicStatFactory
from gold.statistic.Statistic import Statistic, StatisticListSumResSplittable
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
from numpy import *

class FunctionTrackScoreDistributionStat(MagicStatFactory):
    pass

class FunctionTrackScoreDistributionStatSplittable(StatisticListSumResSplittable):
    
    def _combineResults(self):
        results = self._childResults
        
        totalAnswers = 0
        totalValues = 0
        answerValueCount = zeros(101)
        functionValueCount = zeros(101)
        
        for result in results:
            totalAnswers = totalAnswers + result[0]
            totalValues = totalValues + result[1]
            answerValueCount = answerValueCount + result[2]
            functionValueCount = functionValueCount + result[3]
            
        return [totalAnswers, totalValues, answerValueCount, functionValueCount]

class FunctionTrackScoreDistributionStatUnsplittable(Statistic):
    
    def _compute(self):
        predictions, answerSegments = self._children[0].getResult(), self._children[1].getResult()
        
        scores = predictions.valsAsNumpyArray() # Numpy array containing all the scores in the function
        answerStart = answerSegments.startsAsNumpyArray() # Numpy array containing the start position of answer segments
        answerEnd = answerSegments.endsAsNumpyArray() # Contains end position of answer segments

        functionValueCount = zeros(101) # Array to save the score distribution of the function
        totalScores = len(scores) # Total number of scores
        answerValueCount = zeros(101) # Array to save the score distribution of the answer
        totalAnswers = 0
        
        # For every answer...
        for i in range(len(answerStart)):
            answerLength = answerEnd[i] - answerStart[i]
            start = answerStart[i]
            
            totalAnswers = totalAnswers + answerLength
            
            # Count the scores for every nucleotide within the answer
            for j in range(answerLength):
                index = int(scores[start+j]*100)
                answerValueCount[index] = answerValueCount[index] + 1
        
        # Count the scores for every nucleotide for the whole function
        for i in range(totalScores):
            index = int(scores[i]*100)
            
            functionValueCount[index] = functionValueCount[index] + 1
        
        return [totalAnswers, totalScores, answerValueCount, functionValueCount]
    
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(val='number')))
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(interval=True)))
        