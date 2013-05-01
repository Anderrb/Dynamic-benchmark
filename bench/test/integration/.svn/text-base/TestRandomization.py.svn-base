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

#!/usr/bin/env python
import unittest
import os
import tempfile
from test.integration.GalaxyIntegrationTest import GalaxyIntegrationTest
import sys
import numpy

class TestRandomization(GalaxyIntegrationTest):
    def testTpReshuffledStat(self):
        self._assertRunEqual([[('DiffFromMean', 0.0), ('MeanOfNullDistr', 4.0), ('MedianOfNullDistr', 4.0), ('NumPointsTr1', 2), ('NumPointsTr2', 6), ('P-value', 0.65000000000000002), ('SdNullDistr', 1.3416407864998738), ('TSMC_TpRawOverlapStat', 4)]],\
            ["segs"],["segsLen1"],'[tails:=right-tail:][numResamplings:=20:] -> TpReshuffledStat','TestGenome:chr21:16000001-17000000','1000000')

    def testTpPointReshuffledStat(self):
        self._assertRunEqual([[('DiffFromMean', 0.40000000000000002), ('MeanOfNullDistr', 0.59999999999999998), ('MedianOfNullDistr', 1.0), ('NumPointsTr1', 2), ('NumPointsTr2', 447), ('P-value', 0.55000000000000004), ('SdNullDistr', 0.58309518948453021), ('TSMC_TpPointInSegStat', 1)], [('DiffFromMean', 0.0), ('MeanOfNullDistr', 0.0), ('MedianOfNullDistr', 0.0), ('NumPointsTr1', 0), ('NumPointsTr2', 0), ('P-value', None), ('SdNullDistr', 0.0), ('TSMC_TpPointInSegStat', 0)]],\
            ["segs"],["segsMany"],'[tails:=right-tail:][numResamplings:=20:] -> TpPointReshuffledStat','TestGenome:chr21:10000001-11000000','500000')

    def testLogSumDistReshuffledStat(self): 
        self._assertRunEqual([[('DiffFromMean', -1371.3171584747324), ('MeanOfNullDistr', 4025.7179688777478), ('MedianOfNullDistr', 3980.4040522828809), ('NumPointsTr1', 447), ('NumPointsTr2', 2), ('P-value', 1.0), ('SdNullDistr', 1249.287130026858), ('TSMC_LogSumSegSegDistStat', 2654.4008104030154)], [('DiffFromMean', 0.0), ('MeanOfNullDistr', 0.0), ('MedianOfNullDistr', 0.0), ('NumPointsTr1', 0), ('NumPointsTr2', 0), ('P-value', None), ('SdNullDistr', 0.0), ('TSMC_LogSumSegSegDistStat', 0)]],\
           ["segsMany"],["segs"],'[tails:=right-tail:][numResamplings:=20:] -> LogSumSegSegDistReshuffledStat','TestGenome:chr21:10000001-11000000','500000')

    def testSimilarSegmentsReshuffledStat(self):
        self._assertRunEqual([[('DiffFromMean', 0.0), ('MeanOfNullDistr', 0.0), ('MedianOfNullDistr', 0.0), ('NumPointsTr1', 2), ('NumPointsTr2', 447), ('P-value', 1), ('SdNullDistr', 0.0), ('TSMC_SimilarSegmentStat', 0)], [('DiffFromMean', 0.0), ('MeanOfNullDistr', 0.0), ('MedianOfNullDistr', 0.0), ('NumPointsTr1', 0), ('NumPointsTr2', 0), ('P-value', None), ('SdNullDistr', 0.0), ('TSMC_SimilarSegmentStat', 0)]],\
           ["segs"],["segsMany"],'[tails:=two-tail:] [rawStatistic:=SimilarSegmentStat] [randTrackClass:=PermutedSegsAndIntersegsTrack] [numResamplings:_Resamplings=20] -> RandomizationManagerStat','TestGenome:chr21:10000001-12000000','1000000')

    def testSegmentOverlapsHighPresReshuffledStat(self):
        self._assertRunEqual([[('DiffFromMean', 10101.099999999999), ('MeanOfNullDistr', 35630.900000000001), ('MedianOfNullDistr', 42016.0), ('NumPointsTr1', 2), ('NumPointsTr2', 447), ('P-value', 0.80000000000000004), ('SdNullDistr', 15607.104529348166), ('TSMC_TpRawOverlapStat', 45732)], [('DiffFromMean', 0.0), ('MeanOfNullDistr', 0.0), ('MedianOfNullDistr', 0.0), ('NumPointsTr1', 0), ('NumPointsTr2', 0), ('P-value', None), ('SdNullDistr', 0.0), ('TSMC_TpRawOverlapStat', 0)]],\
           ["segs"],["segsMany"],'[tails:=two-tail:] [rawStatistic:=TpRawOverlapStat] [assumptions:=_PermutedSegsAndIntersegsTrack] [numResamplings:_Resamplings=20] -> RandomizationManagerStat','TestGenome:chr21:10000001-12000000','1000000')

    def testSegmentOverlapsSegsByIntensityStat(self):
        self._assertRunEqual([[('DiffFromMean', 2.75), ('MeanOfNullDistr', 0.25), ('MedianOfNullDistr', 0.0), ('NumMoreExtremeThanObs', 0), ('NumPointsTr1', 2), ('NumPointsTr2', 5), ('NumResamplings', 20), ('P-value', 0.09523809523809523), ('SdNullDistr', 0.4330127018922193), ('TSMC_TpRawOverlapStat', 3L)], [('DiffFromMean', 0.0), ('MeanOfNullDistr', 0.0), ('MedianOfNullDistr', 0.0), ('NumMoreExtremeThanObs', 20), ('NumPointsTr1', 0), ('NumPointsTr2', 0), ('NumResamplings', 20), ('P-value', None), ('SdNullDistr', 0.0), ('TSMC_TpRawOverlapStat', 0)]], \
           ["segs"],["segsLen1"],'[tails:=two-tail:] [trackNameIntensity:=nums] [rawStatistic:=TpRawOverlapStat] [assumptions:=_SegsSampledByIntensityTrack] [numResamplings:_Resamplings=20] -> RandomizationManagerStat','TestGenome:chr21:10000001-12000000','1000000')

#def testMeanInsideOutsideTwoTailRandStat(self):
    #    self._assertRunEqual([[('Result', 0.3)], [('Result', 0.0)]],\
    #       ["segsMany"],["nums"],'[tails:=two-tail:][numResamplings:=10:] -> MeanInsideOutsideTwoTailRandStat','TestGenome:chr21:10000001-10010000','5000')
    
    def testCustomRStatMC(self):
        f = tempfile.NamedTemporaryFile('w')
        f.write('#Use in Monte Carlo'+os.linesep)
        f.write('return (sum(track1[3,]) + rnorm(1) )')
        f.flush()
        fn = f.name.encode('hex_codec')
        self._assertRunEqual([[('DiffFromMean', -0.62931081227725372), ('MeanOfNullDistr', 331878.07663687039), ('MedianOfNullDistr', 331878.13514494186), ('NumPointsTr1', 5000), ('NumPointsTr2', 8), ('P-value', 0.69999999999999996), ('SdNullDistr', 1.0260116420085128), ('TSMC_BasicCustomRStat', 331877.44732605811)], [('DiffFromMean', -0.76653875393094495), ('MeanOfNullDistr', 341672.1862082592), ('MedianOfNullDistr', 341672.2768605008), ('NumPointsTr1', 5000), ('NumPointsTr2', 4), ('P-value', 0.84999999999999998), ('SdNullDistr', 0.71985332654161693), ('TSMC_BasicCustomRStat', 341671.41966950527)]],\
           ["nums"],["segsMany"],'[scriptFn:='+fn+':][tails:=right-tail:] -> CustomRStat','TestGenome:chr21:10000001-10010000','5000')
           
#    def testGenomeWideRandmizedRegionRun(self):
#        self._assertRunEqual([[('Result', 0.2)], [('Result', 0.0)], [('Result', 0.0)], [('Result', 1.0)]],\
#            ["segs"],["segsMany"],'[tails:=two-tail:][numResamplings:=5:] -> GenomeWideRandStat','TestGenome:chr21:10000000-10200000','50000')

    def runTest(self):
        #self.testSegmentOverlapsHighPresReshuffledStat()
        #self.testSimilarSegmentsReshuffledStat()
        self.testSegmentOverlapsSegsByIntensityStat()
        pass
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        TestRandomization.VERBOSE = eval(sys.argv[1])
        sys.argv = sys.argv[:-1]
    #TestRandomization().debug()
    #TestRandomization().run()
    unittest.main()
