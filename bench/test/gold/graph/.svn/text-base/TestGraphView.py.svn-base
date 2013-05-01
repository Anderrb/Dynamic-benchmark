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

# NB: TrackFormat == TrackFormat is not tested

import unittest
import numpy as np
from collections import OrderedDict
from gold.graph.GraphView import GraphView, LazyProtoGraphView
from gold.graph.Edge import Edge
from test.gold.track.common.SampleTrackView import SampleTV
from test.util.Asserts import TestCaseWithImprovedAsserts

class TestGraphView(TestCaseWithImprovedAsserts):
    def setUp(self):
        self.emptyTv = SampleTV(starts=[], ids=[], edges=[], anchor = [10,100])
        self.emptyPgv = LazyProtoGraphView.createInstanceFromTrackView(self.emptyTv)
        self.emptyGv = self.emptyPgv.getClosedGraphVersion()

        self.emptyWtv = SampleTV(starts=[], ids=[], edges=[], weights=[], anchor = [10,100])
        self.emptyWpgv = LazyProtoGraphView.createInstanceFromTrackView(self.emptyTv)
        self.emptyWgv = self.emptyPgv.getClosedGraphVersion()

        self.tv = SampleTV(starts=[1,2,3,5], ids=list('1235'), edges=[list('236'), list('125'), [], list('26')], anchor = [10,100])
        self.pgv = LazyProtoGraphView.createInstanceFromTrackView(self.tv)
        self.gv = self.pgv.getClosedGraphVersion()

        self.wtv = SampleTV(starts=[1,2,3,5], ids=list('1235'), edges=[list('236'), list('125'), [], list('26')], weights=[[1,2,3],[4,5,6],[],[7,8]], anchor = [10,100])
        self.wpgv = LazyProtoGraphView.createInstanceFromTrackView(self.wtv)
        self.wgv = self.wpgv.getClosedGraphVersion()

        self.uwtv = SampleTV(starts=[1,2,3,5], ids=list('1235'), edges=[list('256'), list('15'), [], list('126')], weights=[[1,2,3],[1,4],[],[2,4,5]], anchor = [10,100])
        self.uwpgv = LazyProtoGraphView.createInstanceFromTrackView(self.uwtv, isDirected=False)
        self.uwgv = self.uwpgv.getClosedGraphVersion()
        
    def testNodeAccessAndIteration(self):
        self.assertRaises( KeyError, self.emptyGv.getNode, '3' )
        nodes = set( self.emptyGv.getNodeIter() )
        self.assertEqual( set(), nodes )
    
        self.assertEqual( self.gv.getNode('3').id(), '3')    
        nodes = set( self.gv.getNodeIter() )
        self.assertEqual( set([n.id() for n in nodes]), set(list('1235')) )

    def testEdgeIteration(self):
        edges = set( self.emptyGv.getEdgeIter() )
        self.assertEqual( edges, set() )

        #test edges on unweighted graph
        n1, n2, n3, n5 = [self.gv.getNode(i) for i in list('1235')]
        edges = set(self.gv.getEdgeIter())
        self.assertEqual( edges, set([Edge(n1,n2), Edge(n1,n3), Edge(n2,n1), Edge(n2,n2), Edge(n2,n5), Edge(n5,n2)]) )

        #test edges on weighted graph    
        n1, n2, n3, n5 = [self.wgv.getNode(i) for i in list('1235')]
        edges = set(self.wgv.getEdgeIter())
        answerEdges = set([ Edge(n1,n2,1), Edge(n1,n3,2), Edge(n2,n1,4), Edge(n2,n2,5), Edge(n2,n5,6), Edge(n5,n2,7) ])
        #self.assertEqual( [str(x) for x in edges], [str(x) for x in answerEdges])
        self.assertEqual( edges, answerEdges)
        
        #test edges on undirected weighted graph
        n1, n2, n3, n5 = [self.uwgv.getNode(i) for i in list('1235')]
        edges = set(self.uwgv.getEdgeIter())
        answerEdges = set([ Edge(n1,n2,1), Edge(n1,n5,2), Edge(n2,n5,4) ])
        #self.assertEqual( [str(x) for x in edges], [str(x) for x in answerEdges])
        self.assertEqual( edges, answerEdges)

    def testNodeNeighborIteration(self):
        n1, n2, n3, n5 = [self.gv.getNode(i) for i in list('1235')]
        #basic neighbor list
        self.assertEqual( set(n2.getNeighborIter()), set([Edge(n2,n1,None), Edge(n2,n2,None), Edge(n2,n5,None)]))

        n1, n2, n3, n5 = [self.wgv.getNode(i) for i in list('1235')]
        #basic neighbor list with weights
        self.assertEqual( set(n2.getNeighborIter()), set([Edge(n2,n1,4), Edge(n2,n2,5), Edge(n2,n5,6)]))
        
        #assert that edges to nodes outside graph gets pruned away (in lazy manner)
        self.assertEqual( set(n1.getNeighborIter()),  set([Edge(n1,n2,1), Edge(n1,n3,2)]) )
        
    def testGetNewSubGraphFromNodeIdSet(self):
        subGv = self.emptyWgv.getNewSubGraphFromNodeIdSet([])
        self.assertEqual( set(subGv.getNodeIter()), set() )
    
        subGv = self.wgv.getNewSubGraphFromNodeIdSet(list('235'))
        self.assertEqual( set([n.id() for n in subGv.getNodeIter()]), set(list('235')) )

        n2, n3, n5 = [subGv.getNode(i) for i in list('235')]
        edges = set(subGv.getEdgeIter())
        answerEdges = set([Edge(n2,n2,5), Edge(n2,n5,6), Edge(n5,n2,7), ])
        #self.assertEqual( [str(x) for x in edges], [str(x) for x in answerEdges])
        self.assertEqual( edges, answerEdges )
        
    def testGetBinaryMatrixRepresentation(self):
        self.assertListsOrDicts(OrderedDict([('Rows', np.array([], dtype='S')), \
                                             ('Cols', np.array([], dtype='S')), \
                                             ('Matrix', np.array([], dtype='bool8'))]), \
                                self.emptyWgv.getBinaryMatrixRepresentation())
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array([], dtype='S')), \
                                             ('Cols', np.array([], dtype='S')), \
                                             ('Matrix', np.array([], dtype='bool8'))]), \
                                self.emptyWgv.getBinaryMatrixRepresentation(rowsAsFromNodes=False))
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array([], dtype='S')), \
                                             ('Cols', np.array([], dtype='S')), \
                                             ('Matrix', np.array([], dtype='bool8'))]), \
                                self.emptyWgv.getBinaryMatrixRepresentation(completeMatrix=True))
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('125'))), \
                                             ('Cols', np.array(list('1235'))), \
                                             ('Matrix', np.array([[0,1,1,0], [1,1,0,1], [0,1,0,0]], dtype='bool8'))]), \
                                self.wgv.getBinaryMatrixRepresentation())

        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('1235'))), \
                                             ('Cols', np.array(list('125'))), \
                                             ('Matrix', np.array([[0,1,0], [1,1,1], [1,0,0], [0,1,0]], dtype='bool8'))]), \
                                self.wgv.getBinaryMatrixRepresentation(rowsAsFromNodes=False))
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('1235'))), \
                                             ('Cols', np.array(list('1235'))), \
                                             ('Matrix', np.array([[0,1,1,0], [1,1,0,1], [0,0,0,0], [0,1,0,0]], dtype='bool8'))]), \
                                self.wgv.getBinaryMatrixRepresentation(completeMatrix=True))

        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('1235'))), \
                                             ('Cols', np.array(list('1235'))), \
                                             ('Matrix', np.array([[0,1,0,0], [1,1,0,1], [1,0,0,0], [0,1,0,0]], dtype='bool8'))]), \
                                self.wgv.getBinaryMatrixRepresentation(completeMatrix=True, rowsAsFromNodes=False))
        
    def testGetEdgeWeightMatrixRepresentation(self):
        self.assertListsOrDicts(OrderedDict([('Rows', np.array([], dtype='S')), \
                                             ('Cols', np.array([], dtype='S')), \
                                             ('Matrix', np.array([], dtype='float64'))]), \
                                self.emptyWgv.getEdgeWeightMatrixRepresentation())
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array([], dtype='S')), \
                                             ('Cols', np.array([], dtype='S')), \
                                             ('Matrix', np.array([], dtype='float64'))]), \
                                self.emptyWgv.getEdgeWeightMatrixRepresentation(rowsAsFromNodes=False))
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array([], dtype='S')), \
                                             ('Cols', np.array([], dtype='S')), \
                                             ('Matrix', np.array([], dtype='float64'))]), \
                                self.emptyWgv.getEdgeWeightMatrixRepresentation(completeMatrix=True))
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('125'))), \
                                             ('Cols', np.array(list('1235'))), \
                                             ('Matrix', np.array([[0,1,2,0], [4,5,0,6], [0,7,0,0]], dtype='float64'))]), \
                                self.wgv.getEdgeWeightMatrixRepresentation())

        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('1235'))), \
                                             ('Cols', np.array(list('125'))), \
                                             ('Matrix', np.array([[0,4,0], [1,5,7], [2,0,0], [0,6,0]], dtype='float64'))]), \
                                self.wgv.getEdgeWeightMatrixRepresentation(rowsAsFromNodes=False))
        
        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('1235'))), \
                                             ('Cols', np.array(list('1235'))), \
                                             ('Matrix', np.array([[0,1,2,0], [4,5,0,6], [0,0,0,0], [0,7,0,0]], dtype='float64'))]), \
                                self.wgv.getEdgeWeightMatrixRepresentation(completeMatrix=True))

        self.assertListsOrDicts(OrderedDict([('Rows', np.array(list('1235'))), \
                                             ('Cols', np.array(list('1235'))), \
                                             ('Matrix', np.array([[np.nan,4,np.nan,np.nan], [1,5,np.nan,7], \
                                                                  [2,np.nan,np.nan,np.nan], [np.nan,6,np.nan,np.nan]], dtype='float64'))]), \
                                self.wgv.getEdgeWeightMatrixRepresentation(completeMatrix=True, rowsAsFromNodes=False, missingEdgeWeight=np.nan))
        
class TestProtoGraphView(unittest.TestCase):
    def setUp(self):
        self.emptyTv = SampleTV(starts=[], ids=[], edges=[], anchor = [10,100])
        self.emptyPgv = LazyProtoGraphView.createInstanceFromTrackView(self.emptyTv)

        self.emptyTv2 = SampleTV(starts=[], ids=[], edges=[], anchor = [100,200])
        self.emptyPgv2 = LazyProtoGraphView.createInstanceFromTrackView(self.emptyTv2)
        
        self.tv = SampleTV(starts=[1,2,3,5], ids=list('1235'), edges=[list('236'), list('125'), [], list('26')], anchor = [10,100])
        self.pgv = LazyProtoGraphView.createInstanceFromTrackView(self.tv)

        self.tv2 = SampleTV(starts=[0,99], ids=list('69'), edges=[list('3'), list('6')], anchor = [100,200])
        self.pgv2 = LazyProtoGraphView.createInstanceFromTrackView(self.tv2)

    def testCreateInstanceFromTrackView(self):
        self.assertEqual( self.emptyPgv._id2index, {} )
        self.assertEqual( self.emptyPgv._isDirected, True)
        self.assertEqual( self.emptyPgv._id2nodes, {})
        
        greg = self.tv.genomeAnchor
        self.assertEqual( self.pgv._id2index, {'1':(greg,0), '2':(greg,1), '3':(greg,2), '5':(greg,3)} )
        self.assertEqual( self.pgv._isDirected, True)
        self.assertEqual( self.pgv._id2nodes, {})
        
    def testMergeProtoGraphViews(self):
        #Merging a single pgv, should give same result as the single pgv itself
        
        combinedPgv = LazyProtoGraphView.mergeProtoGraphViews([self.emptyPgv])
        self.assertEqual( combinedPgv._id2index, self.emptyPgv._id2index )
        
        combinedPgv = LazyProtoGraphView.mergeProtoGraphViews([self.pgv])
        self.assertEqual( combinedPgv._id2index, self.pgv._id2index )   

        #Merging two pgvs
        
        combinedPgv = LazyProtoGraphView.mergeProtoGraphViews([self.emptyPgv, self.emptyPgv2])
        self.assertEqual( combinedPgv._id2index,  {} )
        
        greg = self.tv.genomeAnchor
        greg2 = self.tv2.genomeAnchor
        combinedPgv = LazyProtoGraphView.mergeProtoGraphViews([self.pgv, self.pgv2])
        self.assertEqual( combinedPgv._id2index,  {'1':(greg,0), '2':(greg,1), '3':(greg,2), '5':(greg,3), '6':(greg2,0), '9':(greg2,1)} )

if __name__ == "__main__":
    unittest.main()
