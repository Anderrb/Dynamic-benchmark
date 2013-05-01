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
from gold.origdata.GenomeElementSource import GenomeElementSource, BoundingRegionTuple
from gold.track.GenomeRegion import GenomeRegion
from gold.util.CustomExceptions import InvalidFormatError

class FastaGenomeElementSource(GenomeElementSource):
    _VERSION = '1.1'
    FILE_SUFFIXES = ['fasta', 'fas', 'fa']
    FILE_FORMAT_NAME = 'FASTA'
    
    _numHeaderLines = 0

    #def __new__(cls, fn, *args, **kwArgs):
    #    ob = object.__new__(cls)
    #    headerLine = open(fn).readline()
    #    assert headerLine[0] == '>'
    #    ob._chr = headerLine.split()[0][1:]
    #    return ob

    #def __getnewargs__(self):
    #    return (self._fn,)

    def __new__(cls, *args, **kwArgs):
        return object.__new__(cls)
    
    def __init__(self, *args, **kwArgs):
        GenomeElementSource.__init__(self, *args, **kwArgs)
        self._boundingRegionTuples = []
        
        if self._getFile().read(1) != '>':
            raise InvalidFormatError('FASTA file does not start with the ">" character.')
    
    def _iter(self):
        self._elCount = 0
        self._boundingRegionTuples = []
        self._genomeElement.chr = None
        return self
        
    def next(self):
        while True:
            bp = self._file.read(1)

            if bp == '>':
                self._appendBoundingRegionTuple()
                self._elCount = 0
                line = self._file.readline().rstrip()
                self._genomeElement.chr = self._checkValidChr(line.split()[0])

            elif bp == '':
                self._appendBoundingRegionTuple()
                raise StopIteration
                
            elif bp not in '\r\n':
                self._elCount += 1
                self._genomeElement.val = bp
                return self._genomeElement
    
    def _appendBoundingRegionTuple(self):
        if self._genomeElement.chr is not None:
            brRegion = GenomeRegion(self._genome, self._genomeElement.chr, 0, self._elCount)
            self._boundingRegionTuples.append(BoundingRegionTuple(brRegion, self._elCount))

    def getValDataType(self):
        return 'S1'

    def getPrefixList(self):
        return ['val']
        
    def getBoundingRegionTuples(self):
        return self._boundingRegionTuples