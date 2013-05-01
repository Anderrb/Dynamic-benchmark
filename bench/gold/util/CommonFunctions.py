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
import re
import traceback
import numpy
import functools
import operator
from collections import Iterable

from config.Config import PROCESSED_DATA_PATH, DEFAULT_GENOME, \
    ORIG_DATA_PATH, OUTPUT_PRECISION, MEMOIZED_DATA_PATH, NONSTANDARD_DATA_PATH, \
    PARSING_ERROR_DATA_PATH, IS_EXPERIMENTAL_INSTALLATION
from gold.util.CustomExceptions import InvalidFormatError
from gold.util.CommonConstants import BINARY_MISSING_VAL
from quick.application.SignatureDevianceLogging import takes,returns
from third_party.decorator import decorator

def createDirPath(trackName, genome, chr=None, allowOverlaps=False, basePath=PROCESSED_DATA_PATH):
    """
    >>> createDirPath(['trackname'],'genome','chr1')
    '/100000/noOverlaps/genome/trackname/chr1'
    """
    from gold.util.CompBinManager import CompBinManager
    if len(trackName)>0 and trackName[0] == 'redirect':
        genome = trackName[1]
        chr = trackName[2]
        #trackName[3] is description
        trackName = trackName[4:]
        
    #print [basePath, str(CompBinManager.getIndexBinSize()), ('withOverlaps' if allowOverlaps else 'noOverlaps'), genome] +\
    #    list(trackName) + ([chr] if chr is not None else [])
    
    return os.sep.join( [basePath, str(CompBinManager.getIndexBinSize()), ('withOverlaps' if allowOverlaps else 'noOverlaps'), genome] +\
        list(trackName) + ([chr] if chr is not None else []) )

#def createMemoPath(trackName, genome, chr, statName):
#    return os.sep.join( [MEMOIZED_DATA_PATH, statName, str(COMP_BIN_SIZE), genome]+list(trackName)+[chr] )
def createMemoPath(region, statId, configHash, track1Hash, track2Hash):
    chr = region.chr
    genome = region.genome
    return os.sep.join( [MEMOIZED_DATA_PATH, str(len(region)), statId, genome, str(track1Hash)] + \
                        ([str(track2Hash)] if track2Hash is not None else []) + \
                        [str(configHash), chr] ).replace('-','_') #replace('-','_') because hashes can be minus, and minus sign makes problems with file handling

@takes(str,(list,tuple),(str,type(None)))
def createOrigPath(genome, trackName, fn=None):
    #print 'genome:',genome
    #print 'trackName:',trackName
    return os.sep.join([ORIG_DATA_PATH, genome] + trackName + ([fn] if fn is not None else []))

@takes(str,(list,tuple),(str,type(None)))
def createCollectedPath(genome, trackName, fn=None):
    return os.sep.join([NONSTANDARD_DATA_PATH, genome] + trackName + ([fn] if fn is not None else []))
    
@takes(str,(list,tuple),(str,type(None)))
def createParsingErrorPath(genome, trackName, fn=None):
    return os.sep.join([PARSING_ERROR_DATA_PATH, genome] + trackName + ([fn] if fn is not None else []))

@takes(str)
def getFileSuffix(fn):
    from gold.application.DataTypes import getSupportedFileSuffixes
    for suffix in getSupportedFileSuffixes():
        if '.' in suffix and fn.endswith('.' + suffix):
            return suffix
    return os.path.splitext(fn)[1].replace('.','')

def getOrigFns(genome, trackName, suffix, fileTree='standardized'):
    assert fileTree in ['standardized', 'collected', 'parsing error']
    from gold.application.LogSetup import logMessage, logging
    
    if fileTree == 'standardized':
        path = createOrigPath(genome, trackName)
    elif fileTree == 'collected':
        path = createCollectedPath(genome, trackName)
    else:
        path = createParsingErrorPath(genome, trackName)

    if not os.path.exists(path):
        if IS_EXPERIMENTAL_INSTALLATION:
            logMessage('getOrigFn - Path does not exist: ' + path, logging.WARNING)
        return []
    
    return [path + os.sep + x for x in os.listdir(path) if os.path.isfile(path + os.sep + x) \
            and x.endswith(suffix) and not x[0] in ['.','_','#'] and not x[-1] in ['~','#']]
    
def getOrigFn(genome, trackName, suffix, fileTree='standardized'):
    fns = getOrigFns(genome, trackName, suffix, fileTree=fileTree)
    if len(fns) != 1:
        if IS_EXPERIMENTAL_INSTALLATION:
            from gold.application.LogSetup import logMessage, logging
            logMessage('getOrigFn - Cannot decide among zero or several filenames: %s' % fns, logging.WARNING)
        return None
    
    return fns[0]

def parseDirPath(path):
    'Returns [genome, trackName, chr] from directory path'
    path = path[len(PROCESSED_DATA_PATH + os.sep):]# + str(CompBinManager.getIndexBinSize())):]
    while path[0] == os.sep:
        path = path[1:]
    path.replace(os.sep*2, os.sep)
    el = path.split(os.sep)
    return el[2], tuple(el[3:-1]), el[-1]

def extractTrackNameFromOrigPath(path):
    excludeEl = None if os.path.isdir(path) else -1
    path = path[len(ORIG_DATA_PATH):]
    path = path.replace('//','/')
    if path[0]=='/':
        path = path[1:]
    if path[-1]=='/':
        path = path[:-1]
    return path.split(os.sep)[1:excludeEl]
    
def getStringFromStrand(strand):
    if strand in (None, BINARY_MISSING_VAL):
        return '.'
    return '+' if strand else '-'

def parseRegSpec(regSpec, genome = None):
    from gold.track.GenomeRegion import GenomeRegion
    from quick.util.GenomeInfo import GenomeInfo

    class SimpleUserBinSource(list):
        pass
        
    regions = []
    allRegSpecs = regSpec.strip().split(',')
    for curRegSpec in allRegSpecs:
        regParts = curRegSpec.strip().split(':')
        if genome == None:
            genome = regParts[0]
            assert GenomeInfo(genome).isInstalled(), "Specified genome is not installed: %s" % genome
        
        if not (regParts[0]=='*' or regParts[0] in GenomeInfo.getExtendedChrList(genome)):
        #if (regParts[0]=='*' or regParts[0].startswith('chr')):
        #    if genome == None:
        #        genome = DEFAULT_GENOME
        #else:
        #    assert genome is None or genome == regParts[0], \
    
            assert regParts[0] == genome, \
                "Region specification does not start with one of '*' or correct chromosome or genome name. Region specification: %s. Genome: %s" % (curRegSpec, genome)
            #genome = regParts[0]        
            regParts = regParts[1:]
        
        if regParts[0] == '*':
            assert len(regParts) == 1, \
                "Region specification starts with '*' but continues with ':'. Region specification: %s" % curRegSpec
            assert len(allRegSpecs) == 1, \
                "Region specification is '*', but is in a list with other region specifications: %s" % regSpec
            for chr in GenomeInfo.getChrList(genome):
                regions.append(GenomeRegion(genome, chr, 0, GenomeInfo.getChrLen(genome, chr)))
        else:
            #assert(regParts[0].startswith('chr')), \
            assert regParts[0] in GenomeInfo.getExtendedChrList(genome), \
                "Region specification does not start with chromosome specification. Region specification: %s " % curRegSpec
            chr = regParts[0]
            try:
                chrLen = GenomeInfo.getChrLen(genome, chr)
            except Exception, e:
                raise InvalidFormatError("Chromosome '%s' does not exist for genome '%s'" % (chr, genome))
                
            if len(regParts)>1:
                posParts = regParts[1]
                assert '-' in posParts, \
                    "Position specification does not include character '-'. Region specification: %s " % curRegSpec
                rawStart, rawEnd = posParts.split('-')
                
                start = int(rawStart.replace('k','001').replace('m','000001'))
                end = int(rawEnd.replace('k','000').replace('m','000000')) if rawEnd != '' else chrLen
                assert start >= 1, \
                    "Start position is not positive. Region specification: %s " % curRegSpec
                assert end >= start, \
                    "End position is not larger than start position. Region specification: %s " % curRegSpec
                assert end <= chrLen, \
                    "End position is larger than chromosome size. Genome: %s. Chromosome size: %s. Region specification: %s" % (genome, chrLen, curRegSpec)
                #-1 for conversion from 1-indexing to 0-indexing end-exclusive
                start-=1
                
            else:
                start,end = 0, chrLen
            regions.append( GenomeRegion(genome, chr, start, end) )
    ubSource = SimpleUserBinSource(regions)
    ubSource.genome = genome
    return ubSource

def parseTrackNameSpec(trackNameSpec):
    return trackNameSpec.split(':')
    
def prettyPrintTrackName(trackName, shortVersion=False):
    from urllib import unquote
    if len(trackName) == 0:
        return ''
    elif len(trackName) == 1:
        return trackName[0]
    elif trackName[0] in ['galaxy','redirect','virtual']:
        return "'" + re.sub('([0-9]+) - (.+)', '\g<2> (\g<1>)', unquote(trackName[3])) + "'"
    elif trackName[0] in ['external']:
        return "'" + re.sub('[0-9]+ - ', '', unquote(trackName[4])) + "'"
    else:
        if trackName[-1]=='':
            return "'" + trackName[-2] + "'"
        return "'" + trackName[-1] + (' (' + trackName[-2] + ')' if not shortVersion else '') + "'"
        #return "'" + trackName[1] + (' (' + '-'.join(trackName[2:]) + ')' if len(trackName) > 2 else '') + "'"
        #return trackName[1] + (' (' + '-'.join(trackName[2:]) + ')' if len(trackName) > 2 else '')
    
def insertTrackNames(text, trackName1, trackName2 = None, shortVersion=False):
    PREFIX = '(the points of |points of |point of |the segments of |segments of |segment of |the function of |function of )?'
    POSTFIX = '([- ]?segments?|[- ]?points?|[- ]?function)?'
    newText = re.sub(PREFIX + '[tT](rack)? ?1' +  POSTFIX, prettyPrintTrackName(trackName1, shortVersion), text)
    if trackName2 != None:
        newText = re.sub(PREFIX + '[tT](rack)? ?2' + POSTFIX, prettyPrintTrackName(trackName2, shortVersion), newText)
    return newText

def resultsWithoutNone(li):
    for el in li:
        if el is not None:
            yield el

def smartSum(li):
    try:
        resultsWithoutNone(li).next()
    except StopIteration:
        return None
    
    return sum(resultsWithoutNone(li))

def isIter(obj):
    from numpy import memmap
    if isinstance(obj, memmap):
        return False
    return hasattr(obj, '__iter__')

def getClassName(obj):
    return obj.__class__.__name__

def strWithStdFormatting(val):
    try:
        assert val != int(val)
        integral, fractional = (('%#.' + str(OUTPUT_PRECISION) + 'g') % val).split('.')
    except:
        integral, fractional = str(val), None
        
    try:
        return '{:,}'.format(int(integral)).replace(',', ' ') + ('.' + fractional if fractional is not None else '')
    except:
        return integral

def smartStrLower(obj):    
    return str.lower(str(obj))

def splitOnWhitespaceWhileKeepingQuotes(msg):
    return re.split('\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', msg.strip())

def parseShortenedSizeSpec(spec):
    spec = spec.strip()
    if spec[-1].lower() == 'k':
        size = int(spec[0:-1]) * 1000
    elif spec[-1].lower() == 'm':
        size = int(spec[0:-1]) * 1000000
    else:
        size = int(spec)
    return size

def generateStandardizedBpSizeText(size):
    if size == 0:
        return '0 bp'
    elif size % 10**9 == 0:
        return str(size/10**9) + ' Gb'
    elif size % 10**6 == 0:
        return str(size/10**6) + ' Mb'
    elif size % 10**3 == 0:
        return str(size/10**3) + ' kb'
    else:
        return str(size) + ' bp'
    
def repackageException(fromException, toException):
    def _repackageException(func, *args, **kwArgs):
        try:        
            return func(*args, **kwArgs)
        except fromException,e:
            raise toException('Repackaged exception.., original was: ' + getClassName(e) + ' - '+str(e) + ' - ' + traceback.format_exc())
    return decorator(_repackageException)

#Repackaging can also be done manually for chunks of code by:
    #import traceback
    #from gold.util.CustomExceptions import ShouldNotOccurError
    #from gold.util.CommonFunctions import getClassName
    #try:
    #    pass #code chunk here..
    #except Exception,e:
    #    raise ShouldNotOccurError('Repackaged exception.., original was: ' + getClassName(e) + ' - '+str(e) + ' - ' + traceback.format_exc())


def quenchException(fromException, replaceVal):
    "if a certain exception occurs within method, catch this exception and instead return a given value"
    def _quenchException(func, *args, **kwArgs):
        try:        
            return func(*args, **kwArgs)
        except fromException,e:
            return replaceVal
    return decorator(_quenchException)

#Typical use, for instance
    #from gold.util.CommonFunctions import repackageException
    #from gold.util.CustomExceptions import ShouldNotOccurError
    #@repackageException(Exception, ShouldNotOccurError)

def reverseDict(mapping):
    vals = mapping.values()
    assert len(set(vals)) == len(vals) #Ensure all values are unique
    return dict((v,k) for k, v in mapping.iteritems())

def mean(l):
    return float(sum(l)) / len(l)

def product(l):
    """Product of a sequence."""
    return functools.reduce(operator.mul, l, 1)
    
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def multiReplace(str, fromList, toList):
    assert len(fromList) == len(toList)
    for i, fromStr in enumerate(fromList):
        str = str.replace(fromStr, toList[i])
    return str