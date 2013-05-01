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
from gold.statistic.MagicStatFactory import MagicStatFactory
from gold.statistic.Statistic import Statistic, StatisticDictSumResSplittable
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
from gold.util.RandomUtil import random

class MarksSortedProbabilityLevelSegmentsStat(MagicStatFactory):
    pass

class MarksSortedProbabilityLevelSegmentsStatSplittable(StatisticDictSumResSplittable):
    def _combineResults(self):
        results = self._childResults
        data = []
        
        for result in results:
            for element in result:
                data.append(element)
        
        return data

'''
Creates a ROC mark list on probability level for benchmark evaluation, 
by comparing a prediction function track to an answer track.
'''
class MarksSortedProbabilityLevelSegmentsStatUnsplittable(Statistic):
    
    def _compute(self):
        predictions, answerSegments = self._children[0].getResult(), self._children[1].getResult()

        answerStart = answerSegments.startsAsNumpyArray()
        answerEnd = answerSegments.endsAsNumpyArray()
        thresholds = predictions.valsAsNumpyArray()
        
        answerIndex = 0
        markList = []
        
        # For every nucleotide along the sequence
        for i in range(len(thresholds)):
            
            # Check if there are still more answers segments
            if answerIndex < len(answerStart):
                # If the nucleotide is outside the current answer segment
                if i > answerEnd[answerIndex]:
                    answerIndex = answerIndex + 1 # Go to the next segment by incrementing answerIndex by 1
                
                # If the nucleotide is outside the current answer segment, set mark to 0
                if (answerIndex >= len(answerStart)) or (i <= answerStart[answerIndex]):
                    markList.append([thresholds[i], random.random(), 0])
                else: # If the nucleotide is inside the current answer segment, set mark to 1
                    markList.append([thresholds[i], random.random(), 1])
            else: # If no more answer segments, set the mark to 0
                markList.append([thresholds[i], random.random(), 0])
        
        return markList
        
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(val='number')))
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(interval=True)))
