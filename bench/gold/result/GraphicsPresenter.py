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

from quick.util.CommonFunctions import ensurePathExists, getRelativeUrlFromWebPath, silenceRWarnings
from gold.result.HtmlCore import HtmlCore
from gold.result.Presenter import Presenter
from gold.result.Results import Results
import os
#from rpy import r, RException
#from gold.application.RSetup import r
#from rpy import RException
from subprocess import call
from gold.util.CustomExceptions import AbstractClassError 
import numpy
from gold.application.LogSetup import logging, HB_LOGGER
import traceback

class GraphicsPresenter(Presenter):
    HIGH_DEF_COLORS = False
    POINT_SIZE = 12
    LINE_HEIGHT = POINT_SIZE * 1.38 # for r.png(). Don't know why
    maxRawDataPoints = None
    #GraphicsPresenter is abstract class, the following vars will be declared in ancestors..
    #name = ('abstract','Abstract')
    #dataPointLimits = (None,None)
    #rCode = ''
    
    def __init__(self, results, baseDir, header):
        Presenter.__init__(self, results, baseDir)
        self._header = header
        self._plotResultObject = None #could be set by subclasses, but not guaranteed

    def getDescription(self):
        return self.__class__.name[1]

    def _getDataPointCount(self, resDictKey):
        raise AbstractClassError
    
    def _checkCorrectData(self, resDictKey):
        return True
    
    def getReference(self, resDictKey, imageLink=False):
        try:
            figFn, dataFn = self._getFns(resDictKey)
            robjFn = self._getResultObjectFn(resDictKey)
            if not self._checkCorrectData(resDictKey):
                return HtmlCore().textWithHelp('N/A', self.__class__.name[1] + ' is not available for this type of data.')
            dataPointCount = self._getDataPointCount(resDictKey)
            minPoints = self.__class__.dataPointLimits[0]
            maxPoints = self.__class__.dataPointLimits[1]
            if type(dataPointCount) not in [list, tuple]:
                dataPointCount = [dataPointCount]
            if minPoints != None and min(dataPointCount) < minPoints:
                return HtmlCore().textWithHelp('N/A', self.__class__.name[1] + ' is not available because there were '\
                                               +'too few data points (< %d).' % minPoints)
            elif maxPoints != None and max(dataPointCount) > maxPoints:
                return HtmlCore().textWithHelp('N/A', self.__class__.name[1] + ' is not available because there were '\
                                               +'too many data points (> %d).' % maxPoints)
            else:
                self._writeContent(resDictKey, figFn)
                self._writeResultObject(resDictKey, robjFn)
                self._writeRawData(resDictKey, dataFn)
                figUrl = getRelativeUrlFromWebPath(figFn)
                if imageLink:
                    figLink='<img src="%s" alt="Figure" width="200"/>' % figUrl
                else:
                    figLink='Figure'
                return str(HtmlCore().link(figLink, figUrl)) + '&nbsp;/&nbsp;' +\
                       (str(HtmlCore().link('R&nbsp;object', getRelativeUrlFromWebPath(robjFn))) + '&nbsp;/&nbsp;' if self._plotResultObject is not None else '') +\
                       str(HtmlCore().link('Raw&nbsp;data', getRelativeUrlFromWebPath(dataFn)))
        
        except (Exception), e: #,RException
        #except None,e:
            logging.getLogger(HB_LOGGER).warning('Error in figure generation' + str(e))
            logging.getLogger(HB_LOGGER).debug(traceback.format_exc())
        return 'Error in figure generation'

    def getPlotDimensions(self, resDictKey):
        return (600, 800)
    
    def _writeContent(self, resDictKey, fn):
        from gold.application.RSetup import r
        ensurePathExists(fn)
        silenceRWarnings()
        bmpFn = fn #+ '.png'
#        r.png(filename=bmpFn, units='px', pointsize=self.POINT_SIZE, res=72)

        width, height = self.getPlotDimensions(resDictKey)
        # pdf test:
#        self.LINE_HEIGHT = self.POINT_SIZE
#        width, height = self.getPlotDimensions(resDictKey)
#        r.pdf(bmpFn, height=height*1.0/72, width=width*1.0/72, pointsize=self.POINT_SIZE)
        if any(x > 800 for x in [width, height]):
            self.LINE_HEIGHT = self.POINT_SIZE
            width, height = self.getPlotDimensions(resDictKey)
            if self.HIGH_DEF_COLORS:
                picType = 'png16m'
            else:
                picType = 'png256'

            r.bitmap(bmpFn, height=height, width=width, units='px', type=picType, pointsize=self.POINT_SIZE)
        else:
            r.png(filename=bmpFn, height=height, width=width, units='px', pointsize=self.POINT_SIZE, res=72)
        if resDictKey is not None:
            xlab = self._results.getLabelHelpPair(resDictKey)[0]
        else:
            xlab = None
        main = self._header
        self._customRExecution(resDictKey, xlab, main)
        #r.hist( ,  )
        from gold.application.RSetup import r
        r('dev.off()')
#        call('convert ' + bmpFn + ' ' + fn, shell=True, stderr = open('/dev/null', 'w'))

    def _writeResultObject(self, resDictKey, fn):
        if self._plotResultObject is not None:
            ensurePathExists(fn)
            from gold.application.RSetup import r
            r('function(x, fn) {dput(x, fn)}')(self._plotResultObject, fn)
            #outF = open(fn,'w')
            #outF.write(str(self._plotResultObject) + os.linesep)
            #outF.close()
        
    def _writeRawData(self, resDictKey, fn):
        ensurePathExists(fn)
        outF = open(fn,'w')
        
        rawData = self._getRawData(resDictKey, False)
        if self.maxRawDataPoints is None or len(rawData) <= self.maxRawDataPoints:
            if type(rawData) in [list, tuple, numpy.ndarray] and len(rawData)>0 and type(rawData[0]) in [int,float,numpy.int32,numpy.float,numpy.float32, numpy.float64, numpy.float128, numpy.ndarray]:
                if type(rawData) == tuple:
                    for npArr in rawData:
                        print>>outF, ','.join([str(x) for x in npArr])
                else:
                    outF.write( os.linesep.join([str(x) for x in rawData]) )
            else:
                outF.write( str(rawData) )
        outF.close()
        
    def _getRawData(self, resDictKey, avoidNAs=True):
        raise AbstractClassError
    
    def _customRExecution(self, resDictKey, xlab, main):
        raise AbstractClassError
        #r('')(self._results.getAllValuesForResDictKey(resDictKey), xlab, main)

    def _getBaseFn(self, resDictKey):
        return os.sep.join([self._baseDir, self._results.getStatClassName() + '_' +\
                              (resDictKey + '_' if not resDictKey is None else '') + self.__class__.name[0]])
        
    def _getFns(self, resDictKey):
        baseFn = self._getBaseFn(resDictKey)
#        return [baseFn + '.pdf', baseFn + '.txt']
        return [baseFn + '.png', baseFn + '.txt']
        
    def _getResultObjectFn(self, resDictKey):
        return self._getBaseFn(resDictKey) + '.robj'

class GlobalResultGraphicsData(object):
    def _getRawData(self, resDictKey, avoidNAs=True):
        if self._results.getGlobalResult() is not None and self._results.getGlobalResult().get(resDictKey) is not None:
            return [x for x in self._results.getGlobalResult().get(resDictKey) if x is not None and not (avoidNAs and numpy.isnan(x))]
        else:
            return None

    def _getDataPointCount(self, resDictKey, avoidNAs=True):
        if self._results.getGlobalResult() is not None and self._results.getGlobalResult().get(resDictKey) is not None:
            return len(self._getRawData(resDictKey, avoidNAs))
        else:
            return 0

#class GlobalResultGraphicsMatrixData(object):
#    def _getRawData(self, resDictKey, avoidNAs=False):
#        assert resDictKey is None
#        assert avoidNAs == False
#        if self._results.getGlobalResult() is not None and self._results.getGlobalResult().get(resDictKey) is not None:
#            return [x for x in self._results.getGlobalResult().get(resDictKey) if x is not None and not (avoidNAs and numpy.isnan(x))]
#        else:
#            return None
        
class GlobalResultGraphicsMatrixDataFromDictOfDicts(object):
    def _getRawData(self, resDictKey, avoidNAs=False):
        assert resDictKey == None
        assert avoidNAs == False
        if not hasattr(self, '_matrixDict'):
            globalRes = self._results.getGlobalResult()
#            print globalRes
            resDictKeys = self._results.getResDictKeys()
            if globalRes is not None and any([type(x) == dict for x in globalRes.values()]):
                keys = set([])
                for resDictKey in resDictKeys:
                    if globalRes[resDictKey] is not None:
                        for key in globalRes[resDictKey].keys():
                            keys.add(key)
                keys = numpy.array([key for key in keys])
                rows = numpy.array([x for x in resDictKeys])
                matrix = []
                for row in rows:
                    matrix.append([globalRes[row].get(key) for key in keys])
                self._matrixDict = {'Matrix': numpy.array(matrix, dtype='float64'), 'Rows':rows, 'Cols':keys}
#                print self._matrixDict
            else:
                self._matrixDict = None
        return self._matrixDict

    def _getDataPointCount(self, resDictKey, avoidNAs=False):
        assert resDictKey is None
        assert avoidNAs == False
        globalRes = self._results.getGlobalResult()
        if globalRes is not None:
            matrix = self._getRawData(resDictKey, avoidNAs)['Matrix']
            return (len(matrix), len(matrix[0]))
        else:
            return (0,0)

class GlobalResultGraphicsMatrixDataFromNumpy(object):
    def _getRawData(self, resDictKey, avoidNAs=False):
        assert avoidNAs == False
        globalRes = self._results.getGlobalResult()
        if globalRes is not None and globalRes.get(resDictKey) is not None:
            return globalRes.get(resDictKey)
        else:
            return None

    def _getDataPointCount(self, resDictKey, avoidNAs=False):
        assert avoidNAs == False
        globalRes = self._results.getGlobalResult().get(resDictKey)
        if globalRes is not None:
            matrix = self._getRawData(resDictKey, avoidNAs)['Matrix']
            return (len(matrix), len(matrix[0]))
        else:
            return (0,0)

class LocalResultsGraphicsData(object):
    def _getRawData(self, resDictKey, avoidNAs=True):
        return [x for x in self._results.getAllValuesForResDictKey(resDictKey) if x is not None and (type(x) is not list) and not (avoidNAs and numpy.isnan(x))]

    def _getDataPointCount(self, resDictKey, avoidNAs=True):
        return len(self._getRawData(resDictKey, avoidNAs))
