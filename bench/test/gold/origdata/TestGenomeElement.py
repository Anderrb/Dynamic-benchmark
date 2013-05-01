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
from gold.origdata.GenomeElement import GenomeElement
from collections import OrderedDict

class TestGenomeElement(unittest.TestCase):
    def setUp(self):
        pass
    
    def testAssignAndRetrieve(self):
        e = GenomeElement('hg18', start=5, val=1.0, extra={'a':1,'b':2}, orderedExtraKeys=['a','b'])
        self.assertEqual(e.genome, 'hg18')
        self.assertEqual(e.chr, None)
        self.assertEqual(e.start, 5)
        self.assertEqual(e.end, None)
        self.assertEqual(e.val, 1.0)
        self.assertEqual(e.strand, None)
        self.assertEqual(e.a, 1)
        self.assertEqual(e.b, 2)
        self.assertEqual(e.extra, {'a':1,'b':2})
        self.assertEqual(e.orderedExtraKeys, ['a', 'b'])
        
        e = GenomeElement('hg18', a=1)
        e.b = 2
        self.assertEqual(e.genome, 'hg18')
        self.assertEqual(e.a, 1)
        self.assertEqual(e.b, 2)
        self.assertEqual(e.extra, {'a':1,'b':2})
        self.assertEqual(e.orderedExtraKeys, ['a', 'b'])
        
        self.assertRaises(AttributeError, lambda : e.nonExisting)
        
        #self.assertEqual(e.get('start'), e.start)
        #self.assertEqual(e.get('end'), e.end)

    def testContains(self):
        self.assertTrue(GenomeElement('hg18','chr1',10,100).contains( \
                        GenomeElement('hg18','chr1',10,100)))
        
        self.assertTrue(GenomeElement('hg18','chr1',10,100).contains( \
                        GenomeElement('hg18','chr1',20,80)))
        
        self.assertFalse(GenomeElement('hg18','chr1',10,100).contains( \
                        GenomeElement('hg18','chr1',10,101)))
        
        self.assertFalse(GenomeElement('hg18','chr1',10,100).contains( \
                        GenomeElement('hg18','chr1',9,100)))
        
        self.assertFalse(GenomeElement('hg18','chr1',10,100).contains( \
                        GenomeElement('hg18','chr1',9,101)))
        
        self.assertFalse(GenomeElement('hg18','chr1',10,100).contains( \
                        GenomeElement('hg18','chr1',0,10)))

        self.assertFalse(GenomeElement('hg18','chr1',10,100).contains( \
                        GenomeElement('hg18','chr2',20,80)))

    def testOverlaps(self):
        self.assertTrue(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr1',10,100)))
        
        self.assertTrue(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr1',20,80)))
        
        self.assertTrue(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr1',10,101)))
        
        self.assertTrue(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr1',9,100)))
        
        self.assertTrue(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr1',9,101)))
        
        self.assertFalse(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr1',0,10)))

        self.assertFalse(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr1',100,110)))

        self.assertFalse(GenomeElement('hg18','chr1',10,100).overlaps( \
                        GenomeElement('hg18','chr2',20,80)))

    def testExclude(self):
        self.assertEqual([GenomeElement('hg18','chr1',100,200)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',90,100) ))
        self.assertEqual([GenomeElement('hg18','chr1',100,200)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',200,210) ))
        self.assertEqual([GenomeElement('hg18','chr1',100,200)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr2',100,110) ))

        self.assertEqual([GenomeElement('hg18','chr1',110,200)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',100,110) ))
        self.assertEqual([GenomeElement('hg18','chr1',110,200)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',90,110) ))
        
        self.assertEqual([GenomeElement('hg18','chr1',100,190)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',190,200) ))
        self.assertEqual([GenomeElement('hg18','chr1',100,190)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',190,210) ))
        
        self.assertEqual([],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',90,210) ))
        
        self.assertEqual([GenomeElement('hg18','chr1',100,140), GenomeElement('hg18','chr1',160,200)],\
                         GenomeElement('hg18','chr1',100,200).exclude( GenomeElement('hg18','chr1',140,160) ))

    def testExtend(self):
        self.assertEqual(GenomeElement('hg18','chr1',100,200),\
                         GenomeElement('hg18','chr1',100,200).extend( 0 ))

        self.assertEqual(GenomeElement('hg18','chr1',0,200),\
                         GenomeElement('hg18','chr1',100,200).extend( -100 ))
        self.assertEqual(GenomeElement('hg18','chr1',-100,200),\
                         GenomeElement('hg18','chr1',100,200).extend( -200, ensureValidity=False ))
        self.assertEqual(GenomeElement('hg18','chr1',0,200),\
                         GenomeElement('hg18','chr1',100,200).extend( -200, ensureValidity=True ))

        self.assertEqual(GenomeElement('hg18','chr1',100,300),\
                         GenomeElement('hg18','chr1',100,200).extend( 100 ))
        self.assertEqual(GenomeElement('hg18','chr1',100,250000200),\
                         GenomeElement('hg18','chr1',100,200).extend( 250000000, ensureValidity=False ))
        self.assertEqual(GenomeElement('hg18','chr1',100,247249719),\
                         GenomeElement('hg18','chr1',100,200).extend( 250000000, ensureValidity=True ))        

    def testEqual(self):
        self.assertEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                         GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('NCBI46','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr2',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',20,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',10,110,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',10,100,6,True,'id',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',10,100,5,False,'id',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',10,100,5,True,'id4',['id2','id3'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id4'],[5,6],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,7],extra={'source':'source'}))

        self.assertNotEqual(GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source'}),
                            GenomeElement('hg18','chr1',10,100,5,True,'id',['id2','id3'],[5,6],extra={'source':'source', 'other':'value'}))

if __name__ == "__main__":
    unittest.main()