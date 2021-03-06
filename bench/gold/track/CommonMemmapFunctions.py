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
import numpy

def createMemmapFileFn(path, prefix, elementDim, dataTypeDim, dataType):
    return path + os.sep + prefix + \
        ( ('.' + str( max(1, elementDim)) ) if elementDim is not None else '' ) + \
        ( ('.' + str(dataTypeDim)) if dataTypeDim > 1 or elementDim is not None else '' ) + \
        '.' + dataType.replace('|', '')

def parseMemmapFileFn(fn):
    fn = os.path.basename(fn)
    splittedFn = fn.split('.')
    prefix = splittedFn[0]
    elementDim = int(splittedFn[1]) if len(splittedFn)==4 else None
    dtypeDim = int(splittedFn[-2]) if len(splittedFn) in [3,4] else 1
    dtype = splittedFn[-1]
    return prefix, elementDim, dtypeDim, dtype
    
def findEmptyVal(valDataType):
    if any(x in valDataType for x in ['str', 'S']):
        baseVal = ''
    elif 'int' in valDataType:
        from gold.util.CommonConstants import BINARY_MISSING_VAL
        baseVal = BINARY_MISSING_VAL
    elif 'float' in valDataType:
        baseVal = numpy.nan
    elif 'bool' in valDataType:
        baseVal = False
    else:
        from gold.util.CustomExceptions import ShouldNotOccurError
        raise ShouldNotOccurError('Error: valDataType (%s) not supported.' % valDataType)
    return baseVal