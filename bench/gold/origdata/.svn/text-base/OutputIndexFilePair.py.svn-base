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

import math
from gold.origdata.OutputFile import OutputFile
from gold.util.CompBinManager import CompBinManager
#from config.Config import COMP_BIN_SIZE
from gold.origdata.GEParseFunctions import *

class OutputIndexFilePair:
    def __init__(self, path, prefixList, chrSize):
        self._path = path
        self._prefixList = prefixList
        
        self._createIndexFiles = 'start' in prefixList or 'end' in prefixList
        if not self._createIndexFiles:
            return
        
        if 'start' in self._prefixList:
            self._leftParseFunc = getStart
        else:
            self._geParseClass = GetPartitionStart()
            self._leftParseFunc = self._geParseClass.parse
        
        if 'end' in self._prefixList:
            self._rightParseFunc = getEnd
        else:
            self._rightParseFunc = getPointEnd
            
#        numIndexElements = int(math.ceil(1.0 * chrSize / CompBinManager.getCompBinSize()))
        #numIndexElements = int(math.ceil(1.0 * chrSize / COMP_BIN_SIZE))
        numIndexElements = int(math.ceil(1.0 * chrSize / CompBinManager.getIndexBinSize()))
        self._leftIndexFile = OutputFile(self._path, 'leftIndex', numIndexElements, allowAppend=False)
        self._rightIndexFile = OutputFile(self._path, 'rightIndex', numIndexElements, allowAppend=False)
        self._i = 0
        self._j = 0
        self._geCount = 0
    
    def writeElement(self, genomeElement):
        if not self._createIndexFiles:
            return
        
        left = self._leftParseFunc(genomeElement)
        right = self._rightParseFunc(genomeElement)
        
        #while right > (self._i) * CompBinManager.getCompBinSize():
#        while right > (self._i) * COMP_BIN_SIZE:
        while right > (self._i) * CompBinManager.getIndexBinSize():
            if 'start' in self._prefixList:
                self._leftIndexFile.write(self._geCount)
            else:
                if self._geCount == 0:
                    break
                self._leftIndexFile.write(self._geCount - 1)
            self._i += 1
                    
#        while left >= (self._j+1) * CompBinManager.getCompBinSize():
#        while left >= (self._j+1) * COMP_BIN_SIZE:
        while left >= (self._j+1) * CompBinManager.getIndexBinSize():
            self._rightIndexFile.write(self._geCount)
            self._j += 1
            
        self._geCount += 1
        
    def _closeIndexFile(self, index, indexFile):
        fileLenght = len(indexFile)
        while index < fileLenght:
            indexFile.write(self._geCount)
            index += 1
        indexFile.close()
    
    def close(self):
        if not self._createIndexFiles:
            return
        
        self._closeIndexFile(self._i, self._leftIndexFile)
        self._closeIndexFile(self._j, self._rightIndexFile)
        