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

import unittest
from quick.origdata.RegionBoundaryFilter import RegionBoundaryFilter
from quick.application.UserBinSource import GlobalBinSource
from test.gold.origdata.common.Asserts import assertDecorator
from functools import partial

class TestRegionBoundaryFilter(unittest.TestCase):
    def setUp(self):
        pass    
    
    def _assertFilter(self, filteredList, unfilteredList):
        assertDecorator(partial(RegionBoundaryFilter, regionBoundaryIter=GlobalBinSource('hg18')), \
                                self.assertEqual, filteredList, unfilteredList)
    
    def testFilter(self):
        self._assertFilter([['hg18','chr1',2,5],['hg18','chr2',3,8]], [['hg18','chr1',2,5],['hg18','chr2',3,8]])
        self._assertFilter([['hg18','chr2',3,8]], [['Test','chr1',2,5],['hg18','chr2',3,8]])
        self._assertFilter([['hg18','chr1',2,5]], [['hg18','chr1',2,5],['hg18','chrTest',3,8]])
        self._assertFilter([['hg18','chr2',3,8]], [['hg18','chr1',-2,5],['hg18','chr2',3,8]])
        
if __name__ == "__main__":
    unittest.main()