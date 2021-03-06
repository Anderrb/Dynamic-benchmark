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
from gold.statistic.Statistic import Statistic, StatisticNumpyMatrixSplittable
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
from collections import OrderedDict
#from numpy import array, ix_, concatenate, apply_along_axis, fliplr, zeros, add, unique, logical_and, logical_or
import numpy

class CategoryPointCountInSegsMatrixStat(MagicStatFactory):
    pass

class CategoryPointCountInSegsMatrixStatSplittable(StatisticNumpyMatrixSplittable):
    pass
            
class CategoryPointCountInSegsMatrixStatUnsplittable(Statistic):    
    VERSION = '1.3'
    def __init__(self, region, track, track2, calcPointTotals=False, **kwArgs):
        if type(calcPointTotals) == str:
            calcPointTotals = eval(calcPointTotals)
        self._calcPointTotals = calcPointTotals
        Statistic.__init__(self, region, track, track2, calcPointTotals=calcPointTotals, **kwArgs)

    def _clusterOverlapsKeepCopies(self, ystarts, yends):
        assert len(ystarts) == len(yends)
        segments = numpy.concatenate((ystarts, yends))
        segments.shape = (2, len(ystarts))
    
        prevEl = [None]
        def firstPass(el):
            if prevEl[0] is not None and prevEl[0][1] == el[0]: # Overlap
                ret = numpy.array([prevEl[0][0], max(prevEl[0][1],el[1])])
            else:
                ret = el
            prevEl[0] = el
            return ret
        segments = numpy.apply_along_axis(firstPass, axis=0, arr=segments)
    
        prevEl = [None]
        def secondPass(el):
            if prevEl[0] is not None and prevEl[0][0] == el[0]: # Overlap after first pass
                ret = numpy.array([el[0],prevEl[0][1]])
            else:
                ret = el
            prevEl[0] = el
            return ret
        segments = numpy.fliplr(numpy.apply_along_axis(secondPass, axis=0, arr=numpy.fliplr(segments)))
        
        return segments
        
    def _compute(self):
        xTv = self._children[0].getResult()
        yTv = self._children[1].getResult()
        
        xCats = xTv.valsAsNumpyArray()
        yCats = yTv.valsAsNumpyArray()
        xUniqueCats = numpy.unique(xCats)
        yUniqueCats = numpy.unique(yCats)
        
        xNumCats = len(xUniqueCats)
        yNumCats = len(yUniqueCats)
        numBps = len(self._region)
        
        # A boolean matrix with each bp as row and each category of the point track as columns
        # True means bp is a point
        xPosMatrix = numpy.zeros(shape=(numBps,xNumCats), dtype='bool8')
        
        for i, cat in enumerate(xUniqueCats):
            xPosMatrix[(xTv.startsAsNumpyArray()[xCats==cat],i)] = True
    
        # A boolean matrix with each bp as row and each category of the segment track as columns
        # True means bp is in a segment
        yPosMatrix = numpy.zeros(shape=(numBps+1,yNumCats), dtype='int8')
    
        for i, cat in enumerate(yUniqueCats):
            yStartsForCat, yEndsForCat = self._clusterOverlapsKeepCopies(yTv.startsAsNumpyArray()[yCats==cat], \
                                                                         yTv.endsAsNumpyArray()[yCats==cat])
            yPosMatrix[(yStartsForCat,i)] += 1
            yPosMatrix[(yEndsForCat,i)] -= 1
    
        yPosMatrix= numpy.add.accumulate(yPosMatrix).astype('bool8')[:numBps]
        
        # Both matrices are concatenated side by side
        posMatrix = numpy.concatenate((xPosMatrix,yPosMatrix), axis=1)
        del xPosMatrix
        del yPosMatrix
    
        # Bps (rows) with no hits in either track1 of track2 is removed
        reducedPosMatrix = numpy.concatenate((numpy.logical_or.reduce(posMatrix[:,:xNumCats], axis=1), \
                                              numpy.logical_or.reduce(posMatrix[:,xNumCats:], axis=1)))
        reducedPosMatrix.shape = (2,len(posMatrix))
        posMatrix = posMatrix[numpy.logical_and.reduce(reducedPosMatrix)]
        del reducedPosMatrix

        if len(posMatrix) == 0:
            return None

#        print posMatrix
        
        # Result matrix
        matrix = numpy.zeros(shape=(xNumCats, yNumCats), dtype='uint32')

        def addCount(row):
            matrix[numpy.ix_(row[:xNumCats],row[xNumCats:])] += 1
            return True

        numpy.apply_along_axis(addCount, axis=1, arr=posMatrix)
        
        rows, cols = xUniqueCats, yUniqueCats
        
        if self._calcPointTotals:
            pointTotals = posMatrix.sum(axis=0)[:xNumCats]
            pointTotals.shape = [xNumCats, 1]
            matrix = numpy.concatenate((matrix, pointTotals), axis=1)
            cols = numpy.concatenate((cols, numpy.array(['Totals'])))

#        print {'Matrix':matrix, 'Rows':xUniqueCats, 'Cols':yUniqueCats}
        #print ','
        
        return {'Result': OrderedDict([('Matrix', matrix), ('Rows', rows), ('Cols', cols)])}

    
    def _createChildren(self):
        self._addChild(RawDataStat(self._region, self._track, TrackFormatReq(dense=False, interval=False, val='category', allowOverlaps=True)))
        self._addChild(RawDataStat(self._region, self._track2, TrackFormatReq(dense=False, interval=True, val='category', allowOverlaps=True)))
