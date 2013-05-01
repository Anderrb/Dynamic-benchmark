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
from collections import OrderedDict
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq

class SequenceLevelOverlapStat(MagicStatFactory):
    pass

class SequenceLevelOverlapStatSplittable(StatisticDictSumResSplittable):
    pass

'''
Evaluates sequence level overlap of predictions within an answer segment which may or may not contain a pattern.
'''
class SequenceLevelOverlapStatUnsplittable(Statistic):

    def _compute(self):
        predictionSegments, answerSegments = self._children[0].getResult(), self._children[1].getResult()

        predictionStart = predictionSegments.startsAsNumpyArray() # Start positions of every prediction
        predictionEnd = predictionSegments.endsAsNumpyArray()     # End positions of every prediction
        answerStart = answerSegments.startsAsNumpyArray()         # Start position of every answer
        answerEnd = answerSegments.endsAsNumpyArray()             # End position of every answer
        values = answerSegments.valsAsNumpyArray()  #Binary binary values for every answer 
                                                    # (1 contains pattern, 0 does not contain)
        
        tn, fp, fn, tp = 0, 0, 0, 0
        predictionIndex = 0
        answerIndex = 0
        
        # If no answer, just return 0 for all
        if len(answerStart) == 0:
            return OrderedDict(zip(['Neither','Only1','Only2','Both'] , (tn,fp,fn,tp)))
        
        # If no predictions, just add false negative and true negative occurrences
        if len(predictionStart) == 0:
            for val in values:
                if val == True:
                    fn = fn + 1
                else:
                    tn = tn + 1
            
            return OrderedDict(zip(['Neither','Only1','Only2','Both'] , (tn,fp,fn,tp)))
        
        # For every answer segment...
        while answerIndex < len(answerStart):
            
            # If the prediction segment is within the answer segment
            if (predictionIndex < len(predictionStart)) and (predictionStart[predictionIndex] >= answerStart[answerIndex]) and (predictionEnd[predictionIndex] <= answerEnd[answerIndex]):
                
                # If the answer contains a pattern
                if values[answerIndex] == True:
                    tp = tp + 1 # Increment true positive by 1
                else:
                    fp = fp + 1 # Else increment false positive by 1
                
                # Go to the next prediction segment outside the current answer segment
                while (predictionIndex < len(predictionStart)) and (predictionStart[predictionIndex] >= answerStart[answerIndex]) and (predictionEnd[predictionIndex] <= answerEnd[answerIndex]):
                    predictionIndex = predictionIndex + 1
            else: # If the answer contains a pattern
                if values[answerIndex] == True:
                    fn = fn + 1 # Increment false negative by 1
                else:
                    tn = tn + 1 # Else increment true negative by 1
            
            answerIndex = answerIndex + 1
                
        return OrderedDict(zip(['Neither','Only1','Only2','Both'] , (tn,fp,fn,tp)))
    
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(allowOverlaps=True, interval=True)))
        self._addChild( RawDataStat(self._region, self._track2, TrackFormatReq(allowOverlaps=True, interval=True, val='tc')))
