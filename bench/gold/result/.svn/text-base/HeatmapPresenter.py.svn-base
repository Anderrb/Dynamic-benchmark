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

from gold.result.GraphicsPresenter import GraphicsPresenter, GlobalResultGraphicsMatrixDataFromNumpy, GlobalResultGraphicsMatrixDataFromDictOfDicts
#from gold.application.RSetup import r
from quick.util.CommonFunctions import ensurePathExists
import os
import numpy
import math

class HeatmapPresenter(GraphicsPresenter):
    name = ('heatmap', 'Plot: heatmap')
    dataPointLimits = (2,None)
    HIGH_DEF_COLORS = True
#    MARGIN_PIXELS = 600 #30 25
#    LINE_HEIGHT = r.par('cra')[1] * r.par('cex') * r.par('lheight')
    POINT_SIZE = 12 #8
    LABEL_TEXT_SIZE = 24
    BLOCK_SIZE = 30 #10
    DEND_PIXELS_PER_HEIGHT = 20
    
    #def _getRawData(self, resDictKey, avoidNAs=True):
    #    return self._results.getAllValuesForResDictKey(resDictKey)
    def __init__(self, results, baseDir, header):
        GraphicsPresenter.__init__(self, results, baseDir, header)
        self._cex = 0
        self._marginWidth = 0
        self._marginHeigth = 0
        self._dendRows = 0
        self._dendCols = 0
        self._mapWidth = 0
        self._mapHeight = 0
        #self._matrixDictNoNan = {}
        self._returnDict = {}

    def _getMarginsInLineHeights(self):
        return (1.0 * self._marginHeight / self.LINE_HEIGHT, 1.0 * self._marginWidth / self.LINE_HEIGHT)

    def getPlotDimensions(self, resDictKey):
        matrixDict = self._getRawData(resDictKey)
        
        self._cex = 1.0 * self.LABEL_TEXT_SIZE / self.LINE_HEIGHT
        
        from gold.application.RSetup import r
        charWidthHeightRatio = r("par('cin')[1]/par('cin')[2]")
        self._marginWidth = int(matrixDict['Rows'].dtype.itemsize * charWidthHeightRatio * self.LABEL_TEXT_SIZE)
        self._marginHeight = int(matrixDict['Cols'].dtype.itemsize * charWidthHeightRatio * self.LABEL_TEXT_SIZE)
        
        numRows = len(matrixDict['Rows'])
        numCols = len(matrixDict['Cols'])
        
#        print matrixDict['Rows'].dtype.itemsize, matrixDict['Cols'].dtype.itemsize, charWidthHeightRatio, self.LABEL_TEXT_SIZE
#        print self._marginWidth, self._marginHeight, self._getMarginsInLineHeights()

        self._dendRows = self._getDendHeightInPixels(matrixDict.get('RowClust'))
        self._dendCols = self._getDendHeightInPixels(matrixDict.get('ColClust'))

        self._mapWidth = self.BLOCK_SIZE * numCols + self._marginWidth
        self._mapHeight = self.BLOCK_SIZE * numRows + self._marginHeight

        self._dendRows = min(self._dendRows, self._mapWidth)
        self._dendCols = min(self._dendCols, self._mapHeight)

        from gold.result.HtmlCore import HtmlCore
        print str(HtmlCore().styleInfoBegin(styleClass='debug'))
        print self._dendRows, self._mapWidth, \
              self._dendCols, self._mapHeight
        

#        print self._dendRows, self._mapWidth, self._dendCols, self._mapHeight

        ret = self._dendRows + self._mapWidth, \
              self._dendCols + self._mapHeight

#        print self._dendRows, self.BLOCK_SIZE * numCols, self._marginWidth
#        print self._dendCols, self.BLOCK_SIZE * numRows, self._marginHeight
#        print self.LINE_HEIGHT
        print ret
        print str(HtmlCore().styleInfoEnd())
        return ret

    def _getDendHeightInPixels(self, clust):
        if clust is not None:
            maxDendHeight = dict(clust.iteritems())['height']
            from gold.application.RSetup import robjects
            if type(maxDendHeight) in (list, robjects.FloatVector):
                maxDendHeight = max(maxDendHeight)
            return max(self._marginWidth, int(maxDendHeight * self.DEND_PIXELS_PER_HEIGHT))
        else:
            return self._marginWidth


    #
    #def _getMatrixDictNoNan(self, resDictKey):
    #    if self._matrixDictNoNan.get(resDictKey) is None:
    #        matrixDict = self._getRawData(resDictKey)
    #    
    #        matrix = numpy.array(matrixDict['Matrix'])
    #        for x in range(len(matrix)):
    #            for y, val in enumerate(matrix[x]):
    #                if val is None:
    #                    matrix[x][y] = numpy.nan
    #                    
    #        nanColMask = numpy.all(numpy.isnan(matrix), axis=0)
    #        matrix = matrix.compress(numpy.logical_not(nanColMask), axis=1)
    #        colnames = numpy.array(matrixDict['Cols'])[numpy.logical_not(nanColMask)].tolist()
    #        
    #        nanRowMask = numpy.all(numpy.isnan(matrix), axis=1)
    #        matrix = matrix.compress(numpy.logical_not(nanRowMask), axis=0)
    #        rownames = numpy.array(matrixDict['Rows'])[numpy.logical_not(nanRowMask)].tolist()
    #
    #        self._matrixDictNoNan[resDictKey] = {'Matrix':matrix, 'Rows':rownames, 'Cols':colnames}
    #    return self._matrixDictNoNan[resDictKey]

    #'heatmap.2(scale(matrix), trace="none", margins=c(margins, margins), na.rm=TRUE, na.color="black", ' +\
    def _customRExecution(self, resDictKey, xlab, main):
        from gold.application.RSetup import r, robjects
        #print r.par('cra')[1] * r.par('cex') * r.par('lheight')
        #print r.par('din')
                #'{matrix <- as.vector(flatmatrix); matrix[unlist(sapply(matrix,is.null))] <- NA; matrix <- as.numeric(matrix);' +\
                #'dim(matrix) <- c(length(colnames),length(rownames)); ' +\
                #'library(flashClust); hr = flashClust(dist(matrix)); hc = flashClust(dist(t(matrix)));' +\
                # matrix = t(matrix); options(expressions=100000);' +\
                
        rCode = 'ourHeatmap <- function(matrix, rownames, colnames, rowClust, colClust, ' +\
                                        'dendrogram, dendRows, dendCols, mapHeight, mapWidth, margins, cex, col, breaks, cellnote) ' +\
                '{dimnames(matrix) <- list(rownames, colnames); sink(file("/dev/null", open="wt"), type="output"); ' +\
                'library(gplots); sink(); options(expressions=100000); ' +\
                'if (typeof(rowClust) != "logical") {class(rowClust) = "hclust"; rowClust = as.dendrogram(rowClust)}; ' +\
                'if (typeof(colClust) != "logical") {class(colClust) = "hclust"; colClust = as.dendrogram(colClust)}; ' +\
                'dim(cellnote) = rev(dim(matrix)); cellnote = t(cellnote); '+\
                'return(heatmap.2(matrix, trace="none", Rowv=rowClust, Colv=colClust, '+\
                'dendrogram=dendrogram, margins=margins, na.rm=TRUE, na.color="white", ' +\
                'col=col, breaks=breaks, lhei=c(dendCols,mapHeight), lwid=c(dendRows,mapWidth), cexRow = cex, cexCol = cex, ' +\
                'key=(min(dendCols, dendRows) >= 150), keysize=1, cellnote=cellnote, notecex=2, notecol="black"))}'
        ##, col=colorRampPalette(c("white", "yellow", "orange", "red"))
        #print (self._results.getAllValuesForResDictKey(resDictKey), xlab, main)
                #print nanColMask, nanRowMask, colnames, rownames, matrix

        matrixDict = self._getRawData(resDictKey)
        matrix, rownames, colnames, significance, rowClust, colClust = [matrixDict.get(x) for x in \
                                                          ['Matrix', 'Rows', 'Cols', 'Significance', 'RowClust', 'ColClust']]
        
        #flatmatrix = []
        #for rowNum in xrange(len(matrix)):
        #    flatmatrix += [float(x) if not numpy.isnan(x) else None for x in matrix[rowNum]]

        #mapHeight = self.MARGINS * self.LINE_HEIGHT + self.BLOCK_SIZE*len(rownames)
        #mapWidth = self.MARGINS * self.LINE_HEIGHT + self.BLOCK_SIZE*len(colnames)

        #print mapHeight, mapWidth, self._dendHeight
        #print rownames, colnames, len(flatmatrix)
        
        rowClust, colClust = [x if x is not None else False for x in [rowClust, colClust]]
        dendrogram = [["both","row"],["column","none"]][rowClust == False][colClust == False]
        
#        hist = numpy.histogram(matrix, bins=[-numpy.Inf,-1,0,1,numpy.Inf], new=True)[0]
        hist = numpy.histogram(matrix, bins=[-numpy.Inf,-1-1e-9,0,1+1e-9,numpy.Inf])[0]
        if hist[0] + hist[1] + hist[3] == 0: #Only counts between 0 and 1
            col = r("colorRampPalette(c('black', 'red', 'yellow'))")
#            breaks = 52
            breaks = 82
        elif hist[0] + hist[3] == 0: #Only counts between -1 and 1
            col = r("colorRampPalette(c('cyan','blue', 'black', 'red', 'yellow'))")
#            breaks = 52
            breaks = 164
        #elif hist[0] == 0: #Assume unbalanced score, most values between -1 and 0
        #    col = r("colorRampPalette(c('blue', 'black', 'red', 'yellow'))")
        #    matmax = matrix.max()
        #    breaks = r("function(matmax) {c(seq(-1.02,0.98,length=51), seq(1.02,matmax,length=26))}")(matmax)
        elif hist[0] == 0: #Only positive counts
            col = r("colorRampPalette(c('black', 'red', 'yellow'))")
            breaks = r("seq(0,5,length=164)")
        else: #Assumes normal distribution
            col = r("c('#99FFFF',colorRampPalette(c('cyan','blue', 'black', 'red', 'yellow'))(161),'#FFFF66')")
#            breaks = r("seq(-5.15,5.15,length=104)")
            breaks = r("seq(-4.075,4.075,length=164)")
#        if numpy.argmax(hist) == 1: #Adjust color palette
#            matmax = matrix.max()
#            matmin = matrix.min()
#            if matmin < -1.0:
#                breaks = numpy.arange(matmin,-1.0,(-1.0-matmin)/20)
#                withBlack = True
#            else:
#                breaks = numpy.array([])
#                withBlack = False
#            breaks = numpy.concatenate((breaks, \
#                                       numpy.arange(-1,1,1.0/20)))
#            if matmax > 1.0:
#                breaks = numpy.concatenate((breaks, \
#                                           numpy.arange(1, matmax, (matmax-1.0)/20), \
#                                           numpy.array([matmax])))
#                withWhite = True
#            else:
#                breaks = numpy.concatenate((breaks, \
#                                           numpy.array([1.0])))
#                withWhite = False
#            rFunc = '''
#function(numCols, withBlack, withWhite) {
#    cols = c("red","orange","yellow")
#    if(withBlack) {
#        cols = c("black", cols)
#    }
#    if(withWhite) {
#        cols = c(cols, "white")
#    }
#    colorRampPalette(cols)(numCols)
#}'''
#            col = r(rFunc)(len(breaks)-1, withBlack, withWhite)
#else:
#            col = 'heat.colors'
#            breaks = 80
        #print [matrix, rownames, colnames, rowClust, colClust, dendrogram, \
        #                                        self._dendRows, self._dendCols, mapHeight, mapWidth, self.MARGINS]

        cellnote = numpy.zeros(shape=matrix.shape, dtype='S1')
        if significance is not None:
            cellnote[significance] = 'o'
        
        self._returnDict[resDictKey] = r(rCode)(matrix, [x for x in rownames], [x for x in colnames], rowClust, colClust, dendrogram, \
                                                self._dendRows, self._dendCols, self._mapHeight, self._mapWidth, \
                                                robjects.FloatVector(self._getMarginsInLineHeights()), self._cex, \
                                                col, breaks, cellnote.flatten().tolist())
        #print clusteredMatrix

    def _writeRawData(self, resDictKey, fn):
        GraphicsPresenter._writeRawData(self, resDictKey, fn)
        if self._returnDict.get(resDictKey) is not None:
            ensurePathExists(fn)
            open(fn,'a').write(os.linesep + 'Return: ' + str(self._returnDict[resDictKey]))

class HeatmapFromNumpyPresenter(GlobalResultGraphicsMatrixDataFromNumpy, HeatmapPresenter):
    pass

class HeatmapFromDictOfDictsPresenter(GlobalResultGraphicsMatrixDataFromDictOfDicts, HeatmapPresenter):
    def getSingleReference(self):
        return self.getReference(resDictKey=None)
    
  
