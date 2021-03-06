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

from config.Config import HB_SOURCE_CODE_BASE_DIR
from gold.result.GraphicsPresenter import GraphicsPresenter, LocalResultsGraphicsData
#from gold.application.RSetup import r
from quick.util.CommonFunctions import silenceRWarnings
import shutil
import os.path

#class GwPlotPresenter(LocalResultsGraphicsData, GraphicsPresenter):
class GwPlotPresenter(GraphicsPresenter):
    name = ('gwplot', 'Plot: values per bin')
    dataPointLimits = (2,None)

    def __init__(self, results, baseDir, header, historyFilePresenter):
        GraphicsPresenter.__init__(self, results, baseDir, header)
        self._historyFilePresenter = historyFilePresenter
        silenceRWarnings()

    #def _getRawData(self, resDictKey, avoidNAs=True):
    #    return self._results.getAllValuesForResDictKey(resDictKey)
    
    #def _customRExecution(self, resDictKey, xlab, main):
    def _writeContent(self, resDictKey, fn):
        #rCode = 'ourHist <- function(ourList, xlab, main, numBins) {vec <- unlist(ourList); hist(vec, col="blue", breaks=numBins, xlab=xlab, main=main)}'
        #print (self._results.getAllValuesForResDictKey(resDictKey), xlab, main)
        PLOT_BED_FN = os.sep.join([HB_SOURCE_CODE_BASE_DIR, 'rCode', 'plotBed.r'])
        PLOT_CHR_FN = os.sep.join([HB_SOURCE_CODE_BASE_DIR, 'rCode', 'ChromosomePlot.r'])        
        forHistoryFn = self._historyFilePresenter._getFn(resDictKey)
        #outDir = self._baseDir
        outDir = os.path.split(fn)[0]
        from gold.application.RSetup import r
        r('source("%s")' % PLOT_BED_FN)
        r('source("%s")' % PLOT_CHR_FN)
        r('loadedBedData <- plot.bed("%s")' % forHistoryFn)
        resultLabel = self._results.getLabelHelpPair(resDictKey)[0]
        r('plot.chrom(segments=loadedBedData, unit="bp", dir.print="%s", ylab="%s")' % (outDir,resultLabel))
        shutil.move(outDir+ os.sep + '.pdf', fn)
        #rawData = self._getRawData(resDictKey)
        #r(rCode)(rawData, xlab, main, numBins)
        
    def _getFns(self, resDictKey):
        figFn = os.sep.join([self._baseDir, self._results.getStatClassName() + '_' + resDictKey +'_' + self.__class__.name[0]+'.pdf'])
        rawFn = self._historyFilePresenter._getFn(resDictKey)
        return [figFn, rawFn]
        #res = GraphicsPresenter._getFns(self, resDictKey)
        #res[0] = res[0].replace('.png', '.pdf')
        #return res

    #def _getRawData(self, resDictKey, avoidNAs=True):
    #    return [x for x in self._results.getAllValuesForResDictKey(resDictKey) if x is not None and (type(x) is not list) and not (avoidNAs and numpy.isnan(x))]

    def _writeRawData(self, resDictKey, fn):
        pass #since it uses raw data from a file that already exists
    
    def _getDataPointCount(self, resDictKey, avoidNAs=True):
        fn = self._historyFilePresenter._getFn(resDictKey)
        return sum(1 for line in open(fn))
