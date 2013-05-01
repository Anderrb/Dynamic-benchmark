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

import os
from gold.origdata.GenomeElement import GenomeElement
from gold.origdata.OutputFile import OutputFile
from gold.origdata.OutputIndexFilePair import OutputIndexFilePair

class OutputDirectory:
    def __init__(self, path, prefixList, fileArraySize, chrSize, valDataType='float64', valDim=1, \
                 weightDataType='float64', weightDim=1, maxNumEdges=0, maxStrLens={}):
        self._prefixList = prefixList
        self._files = []
        if not os.path.exists(path):
            os.makedirs(path)
            
        for prefix in prefixList:
            self._files.append(OutputFile(path, prefix, fileArraySize, valDataType, valDim, weightDataType, weightDim, maxNumEdges, maxStrLens))
        if 'start' in prefixList or 'end' in prefixList:
            self._files.append(OutputIndexFilePair(path, prefixList, chrSize))
        
    def writeElement(self, genomeElement):
        for f in self._files:
            f.writeElement(genomeElement)
        
    def writeRawSlice(self, genomeElement):
        for f in self._files:
            f.writeRawSlice(genomeElement)
            
    def close(self):
        for f in self._files:
            f.close()
