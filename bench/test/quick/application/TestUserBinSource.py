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
from quick.application.UserBinSource import UserBinSource

class TestUserBinSource(unittest.TestCase):
    def setUp(self):
        pass
    
    def testUserBinSource(self):
        bins = [bin for bin in UserBinSource('*','*', genome='hg18')]
        self.assertEqual(24, len(bins))
        self.assertEqual('chr22:1-49691432 (intersects centromere)', str(bins[21]))

    def runTest(self):
        self.testUserBinSource()
    
if __name__ == "__main__":
    #TestUserBinSource().debug()
    unittest.main()