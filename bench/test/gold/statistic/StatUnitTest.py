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

from gold.track.GenomeRegion import GenomeRegion
from gold.track.TrackView import TrackView
from gold.util.CustomExceptions import IncompatibleTracksError, NoneResultError, NoMoreUniqueValsError
from test.gold.track.common.SampleTrack import SampleTrack
from test.gold.track.common.SampleTrackWithConverters import SampleTrackWithConverters
from test.util.Asserts import TestCaseWithImprovedAsserts
from gold.util.CompBinManager import CompBinManager
import config.Config
import gold.util.CompBinManager
import numpy
import gold.statistic.ResultsMemoizer as ResultsMemoizer
from collections import OrderedDict

ResultsMemoizer.LOAD_DISK_MEMOIZATION = False
ResultsMemoizer.STORE_DISK_MEMOIZATION = False

class StatUnitTest(TestCaseWithImprovedAsserts):
    THROW_EXCEPTION = True
    
    def setUp(self):
        gold.util.CompBinManager.COMP_BIN_SIZE = 100
        self._ALLOW_COMP_BIN_SPLITTING = CompBinManager.ALLOW_COMP_BIN_SPLITTING
        CompBinManager.ALLOW_COMP_BIN_SPLITTING = True
        
    def tearDown(self):
        gold.util.CompBinManager.COMP_BIN_SIZE = config.Config.COMP_BIN_SIZE
        CompBinManager.ALLOW_COMP_BIN_SPLITTING = self._ALLOW_COMP_BIN_SPLITTING

    def _createStat(self, *args, **kwArgs):
        assert(isinstance(args[0], TrackView))
        tv1 = args[0]
        if len(args) > 1 and isinstance(args[1], TrackView):
            tv2 = args[1]
            assert(tv1.genomeAnchor == tv2.genomeAnchor)
            self.stat = self.classToCreate(kwArgs['binRegs'] if 'binRegs' in kwArgs else tv1.genomeAnchor, \
                                           SampleTrack(tv1) if kwArgs.get('testWithConverter') != True else SampleTrackWithConverters(tv1),\
                                           SampleTrack(tv2) if kwArgs.get('testWithConverter') != True else SampleTrackWithConverters(tv2),\
                                           *args[2:], **kwArgs)
        else:
            self.stat = self.classToCreate(kwArgs['binRegs'] if 'binRegs' in kwArgs else tv1.genomeAnchor, \
                                           SampleTrack(tv1) if kwArgs.get('testWithConverter') != True else SampleTrackWithConverters(tv1),\
                                           *args[1:], **kwArgs)
    
    def _assertIncompatibleTracks(self, *args, **kwArgs):
        self.assertRaises(IncompatibleTracksError, self._assertCompute, None, *args, **kwArgs)

    def _assertIterativeComputes(self, targetResultList, *args, **kwArgs):
        self._createStat(*args, **kwArgs)
        
        for i in range(len(targetResultList)):
            self._assertResult(targetResultList[i], *args, **kwArgs)
            self.stat.prepareForNewIteration()
        self.assertRaises(NoMoreUniqueValsError, self._assertResult, None, *args, **kwArgs)
        #self._assertResult(None, *args, **kwArgs)
        
    def _assertCompute(self, targetResult, *args, **kwArgs):
        self._createStat(*args, **kwArgs)
        #
        #self.stat.createChildren()
        #self.stat.compute()
        self._assertResult(targetResult, *args, **kwArgs)
        
    def _assertResult(self, targetResult, *args, **kwArgs):
        if kwArgs.has_key('assertFunc'):
            assertFunc = kwArgs['assertFunc']
        else:
            if type(targetResult) in [list, dict, tuple, numpy.ndarray, OrderedDict]:
                assertFunc = self.assertListsOrDicts
            elif type(targetResult) in [float]:
                assertFunc = self.assertAlmostEqual
            else:
                assertFunc = self.assertEqual
            
        try:
            res = self.stat.getResult()
        except NoneResultError:
            res = None

        try:
            assertFunc(targetResult, res)
        except Exception, e:
            if self.THROW_EXCEPTION:
                raise
            else:
                print 'Assert error:',e
                print ''
                print '****'
                print res
                print '****'
                print ''
                
        
    def _assertCreateChildren(self, childrenClassList, *args, **kwArgs):
        self._createStat(*args, **kwArgs)
        self.stat._createChildren()

        self.assertEqual(len(childrenClassList), len(self.stat._children))
        for i, cls in enumerate(childrenClassList):
            self.assertTrue(cls == self.stat._children[i].__class__)
            
    
