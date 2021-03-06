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
from gold.statistic.Statistic import Statistic, StatisticDynamicDictSumResSplittable
from gold.statistic.RawDataStat import RawDataStat
from gold.track.TrackFormat import TrackFormatReq
from gold.util.CustomExceptions import IncompatibleTracksError
import numpy

class BpCoverageByCatStat(MagicStatFactory):
    pass

class BpCoverageByCatStatSplittable(StatisticDynamicDictSumResSplittable):
    pass
            
class BpCoverageByCatStatUnsplittable(Statistic):
    def _compute(self):
        rawData = self._children[0].getResult()
        ends = rawData.endsAsNumpyArray()
        starts = rawData.startsAsNumpyArray()
        catSequence = rawData.valsAsNumpyArray()
        if catSequence is None:
            raise IncompatibleTracksError()
        
        catSet = numpy.unique(catSequence)
        res = {}
        for cat in catSet:
            filter = (catSequence==cat)
            if rawData.trackFormat.reprIsDense():
                res[cat] = filter.sum()
            else:
                #print 'BpCoverage..: ',ends, starts, catSequence, catSet, type(catSequence), filter
                #res[cat] = ends[filter].sum() - starts[filter].sum()
                totCoverage = ends[filter].sum() - starts[filter].sum()
                tempArray = ends[filter][:-1] - starts[filter][1:]
                totOverlap = tempArray[tempArray > 0].sum()
                res[cat] = totCoverage - totOverlap
        return res
        
    def _createChildren(self):
        self._addChild( RawDataStat(self._region, self._track, TrackFormatReq(val='category', allowOverlaps=True)) )
        
