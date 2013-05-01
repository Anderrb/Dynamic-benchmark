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
from quick.statistic.BinSizeStat import BinSizeStat

class FunctionTrackAnalysisStat(MagicStatFactory):
    pass

class FunctionTrackAnalysisStatSplittable(StatisticListSumResSplittable):
    pass

class FunctionTrackAnalysisStatUnsplittable(Statistic):
    
    def _compute(self):
        predictions, answerSegments = self._children[0].getResult(), self._children[1].getResult()
        
        values = predictions.valsAsNumpyArray()
        answerStart = answerSegments.startsAsNumpyArray()
        answerEnd = answerSegments.endsAsNumpyArray()
        
        nNucleotidesWithinAnswer = 0
        sumValuesWithinAnswer = 0.0
        
        # If no answers in this bin, just return
        if len(answerStart) == 0:
            nNucleotidesOutsideAnswer = len(values)
            sumValuesOutsideAnswer  = sum(values)
            
            return [nNucleotidesWithinAnswer, nNucleotidesOutsideAnswer, sumValuesWithinAnswer, sumValuesOutsideAnswer]
        
        # For each answer..
        for i in range(len(answerStart)):
            answerLength = answerEnd[i] - answerStart[i]
            start = answerStart[i]
            
            nNucleotidesWithinAnswer = nNucleotidesWithinAnswer + answerLength
            
            # Calculate the sum of function values within answer
            for j in range(answerLength):
                sumValuesWithinAnswer = sumValuesWithinAnswer + values[start+j]
        
        nNucleotidesOutsideAnswer = len(values) - nNucleotidesWithinAnswer
        sumValuesOutsideAnswer = sum(values) - sumValuesWithinAnswer

        return [nNucleotidesWithinAnswer, nNucleotidesOutsideAnswer, sumValuesWithinAnswer, sumValuesOutsideAnswer]
    
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(val='number')))
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(interval=True)))
        