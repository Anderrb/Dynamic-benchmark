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
from gold.statistic.Statistic import Statistic, StatisticConcatResSplittable, OnlyGloballySplittable
from gold.aux.SlidingWindow import SlidingWindow
from quick.util.GenomeInfo import GenomeInfo
from gold.track.Track import PlainTrack
from gold.track.GenomeRegion import GenomeRegion
from quick.util.Wrappers import GenomeElementTvWrapper
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
#from gold.application.RSetup import r

class SmoothedPointMarksStat(MagicStatFactory):
    pass

class SmoothedPointMarksStatSplittable(StatisticConcatResSplittable, OnlyGloballySplittable):
    pass
            
class SmoothedPointMarksStatUnsplittable(Statistic):    
    def __init__(self, region, track, track2=None, windowSize=21, windowBpSize=50000, sdOfGaussian=20000, guaranteeBpCoverByWindow='True', withOverlaps='no', **kwArgs):
        self._windowSize = int(windowSize)
        self._windowBpSize = int(windowBpSize)
        self._sdOfGaussian = int(sdOfGaussian)
        self._guaranteeBpCoverByWindow = eval(guaranteeBpCoverByWindow)
        assert( withOverlaps in ['no','yes'])
        self._withOverlaps = withOverlaps
        Statistic.__init__(self,region,track,track2,windowSize=windowSize, windowBpSize=windowBpSize, sdOfGaussian=sdOfGaussian, guaranteeBpCoverByWindow=guaranteeBpCoverByWindow, withOverlaps=withOverlaps, **kwArgs)
        
    def _compute(self):
        tv = self._children[0].getResult()
        #print 'TV: ',[x.val for x in GenomeElementTvWrapper(tv)]
        #print [x.end() for x in inTrackView]
        slidingWindows = SlidingWindow(GenomeElementTvWrapper(tv), self._windowSize)
        res = [x for x in self._weightedValForWindowsYielder(slidingWindows, self._windowSize, self._windowBpSize, self._sdOfGaussian, self._guaranteeBpCoverByWindow)]
        #print 'RES: ',res
        return res
    
    def _createChildren(self):
        rawDataStat = RawDataStat(self._region, self._track, TrackFormatReq(dense=False, interval=False, allowOverlaps = (self._withOverlaps == 'yes')))
        self._addChild(rawDataStat)

    @staticmethod
    def _weightedValForWindowsYielder(slidingWindows, windowSize, windowBpSize, sdOfGaussian, guaranteeBpCoverByWindow):
        from gold.application.RSetup import r
        mode = 'start'
        assert windowSize%2==1
        for window in slidingWindows:
            #print 'WIN: ', [x.val for x in window]
            if len(window) == windowSize:
                assert mode in ['start','full']
                mode = 'full'
                midPos = windowSize/2
            else:
                if mode == 'full':
                    mode = 'end'
                if mode == 'start':
                    midPos = len(window)-windowSize/2-1
                elif mode =='end':
                    midPos = windowSize/2

            midEl = window[midPos]
            if len(window) == windowSize:
                #print [x.start for x in window]
                #print window[0].start ,window[midPos].start
                if guaranteeBpCoverByWindow:
                    assert abs(window[0].start - window[midPos].start) > windowBpSize/2
                    assert abs(window[-1].start - window[midPos].start) > windowBpSize/2
            
            weightedValIntegral = sum( [r.dnorm(int(el.start-midEl.start),0,sdOfGaussian)*el.val for el in window if abs(el.start-midEl.start)<windowBpSize/2] )
            #weightedValIntegral = sum( [r.dnorm(el.start-midEl.start,0,2000)*el.end for el in window if abs(el.start-midEl.start)<2500] )
            normalizationIntegral = sum( [r.dnorm(int(el.start-midEl.start),0,sdOfGaussian)*1 for el in window if abs(el.start-midEl.start)<windowBpSize/2] )
            yield weightedValIntegral / normalizationIntegral



#def weightedValForWindowsYielder(slidingWindows,windowSize):
#    for window in slidingWindows:
#        midPos = len(window)/2
#        midEl = window[midPos]
#        if len(window) == windowSize:
#            #print [x.start for x in window]
#            #print window[0].start ,window[midPos].start
#            assert abs(window[0].start - window[midPos].start) > 2500
#            assert abs(window[-1].start - window[midPos].start) > 2500
#        
#        weightedValIntegral = sum( [r.dnorm(el.start-midEl.start,0,2000)*el.val for el in window if abs(el.start-midEl.start)<2500] )
#        #weightedValIntegral = sum( [r.dnorm(el.start-midEl.start,0,2000)*el.end for el in window if abs(el.start-midEl.start)<2500] )
#        normalizationIntegral = sum( [r.dnorm(el.start-midEl.start,0,2000)*1 for el in window if abs(el.start-midEl.start)<2500] )
#        yield weightedValIntegral / normalizationIntegral
#        
##PointSmoothing..:
#def smoothedPointMarks(genome, inTrackName, windowSize, chr):
#    
#    #func = lambda x: ( sum( [r.dnorm(i-len(x)/2.0,0,2000)*x[i].end for i in range(len(x)) if x[i]!=None] ) / sum( [r.dnorm(i-len(x)/2.0,0,2000)*1 for i in range(len(x)) if x[i]!=None] ) ) if len([y for y in x if y!=None])>0 else 0    
#    
#    chrReg = GenomeRegion(genome, chr, 0, GenomeInfo.getChrLen(genome,chr) )
#            #chrReg = GenomeElement(genome, chr, 0, 3000)
#    inTrackView = PlainTrack(inTrackName).getTrackView(chrReg)
#    print [x.end() for x in inTrackView]
#    slidingWindows = SlidingWindow(GenomeElementTvWrapper(inTrackView), windowSize)
#    print [x for x in weightedValForWindowsYielder(slidingWindows, windowSize)]
#    
##smoothPoints('sacCer1', ['Genes and Gene Prediction Tracks','Exons'],21,'chr1')
#
##12345678
##.-- 3,2
##-.-- 4,2
##--.-- 5,2
## --.-- 5,2
##  --.-- 5,2
##   --.- 4,2
##    --. 3,2
##1234567
##
##                if mode == 'start':
##                    midPos = len(window)-windowSize/2 -1
##                else:
##                    midPos = windowSize/2
