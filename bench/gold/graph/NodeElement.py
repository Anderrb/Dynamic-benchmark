from gold.graph.Edge import Edge
from gold.track.TrackView import TrackElement, AutonomousTrackElement

class NodeElement(TrackElement):
    'A track element that also includes references to its neighbors as other NodeElements'
    def __init__(self, trackView, index, graphView):
        TrackElement.__init__(self, trackView, index=index)
        if trackView._weightsList == None:
            self.weights = self.none
        self._graphView = graphView
        self.color = None
        
    def getNeighborIter(self):
        'Allows iteration through neighbors in the form of Edge objects'
        edgeList = self.edges()
        weightList = self.weights()
        #numNeighbors = len(edgeList)
        
        for i, neighborId in enumerate(edgeList[edgeList != '']):          
            if self._graphView.hasNode(neighborId):
                toNode = self._graphView.getNode( neighborId )
                yield Edge(self, toNode, weightList[i] if (weightList is not None) else None, self._graphView.isDirected() )
    
    def __repr__(self):
        return self.id()
        
    def __hash__(self):
        return hash(self.id())
        
#class ProtoNodeElement(AutonomousTrackElement):
#    'A track element that includes neighbors in the form of IDs (strings)'
#    pass