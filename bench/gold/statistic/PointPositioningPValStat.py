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
from gold.statistic.Statistic import Statistic
from gold.statistic.PointPositionsInSegsStat import PointPositionsInSegsStat
from gold.util.CustomExceptions import ShouldNotOccurError, NotSupportedError
from collections import OrderedDict

class PointPositioningPValStat(MagicStatFactory):
    pass

class PointPositioningPValStatUnsplittable(Statistic):
    def __init__(self, region, track, track2, tail='', **kwArgs):
        self._altHyp = tail
        if not self._altHyp in ['ha1','ha2','ha3','ha4']:
            raise NotSupportedError(self._altHyp)
        Statistic.__init__(self, region, track, track2, tail=tail, **kwArgs)

    def _checkAssumptions(self, assumptions):
        #if not assumptions == 'independentPoints':
        #    raise IncompatibleAssumptionsError
        pass

    def _computeMc(self):
        return self._children[0].getResult()
    
    def _compute(self):
        assumptions = self._kwArgs['assumptions']
        if not assumptions == 'independentPoints':
            return self._computeMc()

        allRelPositions = self._children[0].getResult()
        
        scoreList = []
        for relPos in allRelPositions:
            score = PointPositioningPValStatUnsplittable._calcScore(relPos, self._altHyp)
            if score!=0:
                #scoreList.append( (abs(score), random(), score>0) ) #random number to avoid sign bias when sorting on absolute value
                scoreList.append( (abs(score), score>0) )
        
        wPlusMinus = {True:0, False:0}
        sortedScores = sorted(scoreList)
        curValPos = 0
        while curValPos < len(sortedScores):
            higherValPos = curValPos + 1
            while higherValPos < len(sortedScores) and \
                sortedScores[higherValPos][0] - sortedScores[curValPos][0] < 1.0e-7: #almost equal, to ignore representation errors
                    higherValPos += 1
            for pos in xrange(curValPos, higherValPos):
                wPlusMinus[sortedScores[pos][1]] += (curValPos+(higherValPos-1))/2.0 +1 #higherValPos-1 since end-exclusive, +1 since ranks start from 1
            curValPos = higherValPos
            
        #w = min(wPlusMinus[True], wPlusMinus[False]) #wouldn't this make it two-tailed?
        w = wPlusMinus[True]
                
        n = len(sortedScores)
        distribution = 'N/A'
        if n<2:
            pval = None
        elif n<30:
            from gold.application.RSetup import r
            #print 'w,n: ',w,n
            pval = r.psignrank(w,n)
            distribution = 'Wilcoxon'
        else:
            from gold.application.RSetup import r
            mean = n*(n+1)/4.0
            var = n*(n+1)*(2*n+1)/24.0
            pval = r.pnorm(w, mean, var**0.5)
            distribution = 'Normal approximation'
        
        return OrderedDict([ ('P-value', pval), ('Test statistic: ' + ('W12' if self._altHyp in ['ha1', 'ha2'] else \
                             ('W34' if self._altHyp in ['ha3', 'ha4'] else 'W5')), w), ('N', n) , ('Distribution',distribution), ('altHyp',self._altHyp)]) #fixme: remove althyp from here..
    
    @staticmethod
    def _calcScore(relPos, altHyp):
        if altHyp == 'ha1':
            return 1 - 4*abs(relPos-0.5)
        if altHyp == 'ha2':
            return -1 + 4*abs(relPos-0.5)
        elif altHyp == 'ha3':
            return -1 + 2.0 * relPos
        elif altHyp == 'ha4':
            return 1 - 2.0 * relPos
        else:
            raise ShouldNotOccurError
    
    def _createChildren(self):
        from gold.statistic.RandomizationManagerStat import RandomizationManagerStat
        from gold.statistic.AvgRelPointPositioningStat import AvgRelPointPositioningStat
        assumptions = self._kwArgs['assumptions']
        if not assumptions == 'independentPoints':
            assert self._altHyp == 'ha3'
            self._addChild( RandomizationManagerStat(self._region, self._track, self._track2, AvgRelPointPositioningStat, None, self._kwArgs['assumptions'], 'less', self._kwArgs['numResamplings']) )
        else:
            self._addChild( PointPositionsInSegsStat(self._region, self._track, self._track2) )
