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
from gold.statistic.Statistic import Statistic, StatisticDictSumResSplittable
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
from gold.util.RandomUtil import random

class MarksSortedSequenceLevelSegmentsStat(MagicStatFactory):
    pass

class MarksSortedSequenceLevelSegmentsStatSplittable(StatisticDictSumResSplittable):
    def _combineResults(self):
        results = self._childResults
        data = []
        
        for result in results:
            for element in result:
                data.append(element)
        
        return data
        
'''
Creates a ROC mark list on sequence level for benchmark evaluation, 
by comparing a prediction track to an answer track.
'''
class MarksSortedSequenceLevelSegmentsStatUnsplittable(Statistic):

    def _compute(self):
        predictionSegments, answerSegments = self._children[0].getResult(), self._children[1].getResult()

        predictionStart = predictionSegments.startsAsNumpyArray()
        predictionEnd = predictionSegments.endsAsNumpyArray()  
        answerStart = answerSegments.startsAsNumpyArray()
        answerEnd = answerSegments.endsAsNumpyArray()
        # Thresholds between 0 and 100 (higher is better)
        thresholds = predictionSegments.valsAsNumpyArray()
        # Binary values, 1 = pattern exist within sequence, 0 = it don't
        values = answerSegments.valsAsNumpyArray()
        
        predictionIndex = 0
        answerIndex = 0
        markList = []
        threshold = 0
        
        # If no predictions, just add the values and set threshold to 0.0
        if len(predictionStart) == 0:
            for val in values:
                if val == True:
                    markList.append([0.0, random.random(), 1])
                else:
                    markList.append([0.0, random.random(), 0])
                    
            return markList
        
        # For every answer segment...
        while answerIndex < len(answerStart):
            # If prediction is within answer
            if (predictionIndex < len(predictionStart)) and (predictionStart[predictionIndex] >= answerStart[answerIndex]) and (predictionEnd[predictionIndex] <= answerEnd[answerIndex]):
                threshold = thresholds[predictionIndex]
                
                # Find and use the highest threshold value within this segment
                while True:
                    predictionIndex = predictionIndex + 1
                    
                    if (predictionIndex < len(predictionStart)):
                        if (predictionStart[predictionIndex] >= answerStart[answerIndex]) and (predictionEnd[predictionIndex] <= answerEnd[answerIndex]):
                            
                            if threshold < thresholds[predictionIndex]:
                                threshold = thresholds[predictionIndex]
                        else:
                            break
                    else:
                        break
            else: # If prediction is not within answer, set threshold to 0.0
                threshold = 0.0
            
            # Append results to marklist
            if values[answerIndex] == True:
                markList.append([threshold, random.random(), 1])
            else:
                markList.append([threshold, random.random(), 0])            
                
            answerIndex = answerIndex + 1
        
        return markList
        
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(allowOverlaps=True, interval=True, val='number')))
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(allowOverlaps=True, interval=True, val='tc')))
