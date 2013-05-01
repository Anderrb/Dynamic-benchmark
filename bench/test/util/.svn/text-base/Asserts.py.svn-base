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
import numpy
from gold.origdata.GenomeElement import GenomeElement

def AssertList(list1, list2, assertFunc=None):
    if not (len(list1) == len(list2)):
        print 'Lengths: ', len(list1), '!=', len(list2)
        print [x for x in list1], '!=', [x for x in list2]
        assert(False)
    for x,y in zip(list1, list2):
        assertFunc(x, y)

def _isListType(x):
    return type(x) == list or type(x) == tuple or isinstance(x, numpy.ndarray) or isinstance(x, dict)

def _ifDictConvertToList(d):
    return [(x, d[x]) for x in sorted(d.keys())] if isinstance(d, dict) else d

def smartRecursiveAssertList(x, y, assertEqualFunc, assertAlmostEqualFunc):
    if _isListType(x):
        if isinstance(x, numpy.ndarray):
            try:
                assertEqualFunc(x.shape, y.shape)
            except Exception, e:
                raise AssertionError(str(e) + ' on shape of lists: ' + str(x) + ' and ' + str(y))
                
            try:
                assertEqualFunc(x.dtype, y.dtype)
            except Exception, e:
                raise AssertionError(str(e) + ' on datatypes of lists: ' + str(x) + ' and ' + str(y))
        else:
            try:
                assertEqualFunc(len(x), len(y))
            except Exception, e:
                raise AssertionError(str(e) + ' on length of lists: ' + str(x) + ' and ' + str(y))

        for el1,el2 in zip(*[_ifDictConvertToList(x) for x in [x, y]]):
            smartRecursiveAssertList(el1, el2, assertEqualFunc, assertAlmostEqualFunc)
            
    else:
        try:
            assertAlmostEqualFunc(x, y)
        except TypeError:
            assertEqualFunc(x, y)

class TestCaseWithImprovedAsserts(unittest.TestCase):
    def assertEqual(self, a, b):
        if not self._assertIsNan(a, b):
            return unittest.TestCase.assertEqual(self, a, b)

    def assertAlmostEqual(self, a, b):
        if not self._assertIsNan(a, b):
            return unittest.TestCase.assertAlmostEqual(self, a, b, places=5)
    
    def assertAlmostEquals(self, a, b):
        return unittest.TestCase.assertAlmostEquals(self, a, b, places=5)
    
    def _assertIsNan(self, a, b):
        try:
            if not any(_isListType(x) for x in [a,b]):
                if numpy.isnan(a):
                    self.assertTrue(b is not None and numpy.isnan(b))
                    return True
        except (TypeError, NotImplementedError):
            pass
        return False
        
    def assertListsOrDicts(self, a, b):
        try:
            smartRecursiveAssertList(a, b, self.assertEqual, self.assertAlmostEqual)
        except Exception, e:
            print 'Error in recursive assert of %s == %s' % (a, b)
            raise e

    def assertGenomeElements(self, a, b):
        self.assertListsOrDicts(a.val, b.val)
        self.assertListsOrDicts(a.edges, b.edges)
        self.assertListsOrDicts(a.weights, b.weights)
        a.val = b.val = None
        a.edges = b.edges = None
        a.weights = b.weights = None
        
        return unittest.TestCase.assertEqual(self, a, b)
        
    def assertGenomeElementLists(self, a, b):
        self.assertEqual(sum([1 for el in a]), sum([1 for el in b]))
        
        for i, el in enumerate( b ):
            try:
                self.assertGenomeElements(a[i], el)

            except Exception, e:
                print a[i].toStr() + ' != ' + el.toStr()
                raise