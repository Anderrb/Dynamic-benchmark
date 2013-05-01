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
import sys
import functools
import re
import urllib
from config.Config import STATIC_PATH, GALAXY_BASE_DIR, URL_PREFIX
from third_party.decorator import decorator
import contextlib

def ensurePathExists(fn):
    "Assumes that fn consists of a basepath (folder) and a filename, and ensures that the folder exists."
    path = os.path.split(fn)[0]
    
    if not os.path.exists(path):
        #oldMask = os.umask(0002)
        os.makedirs(path)
        #os.umask(oldMask)
        
def reloadModules():
    for module in [val for key,val in sys.modules.iteritems() \
                   if key.startswith('gold') or key.startswith('quick') or key.startswith('test')]:
        try:
            reload(module)
        except:
            print module
            
def wrapClass(origClass, keywords={}):
    #for key in keywords.keys():
    #    if re.match('^[0-9]+$',keywords[key]) is not None:
    #        keywords[key] = int(keywords[key])
    #    elif re.match('^[0-9]?[.][0-9]?$',keywords[key]) is not None and keywords[key] != '.':
    #        keywords[key] = float(keywords[key])
           
    args = []
    wrapped = functools.partial(origClass, *args, **keywords)
    functools.update_wrapper(wrapped, origClass)
    return wrapped

def extractIdFromGalaxyFn(fn):
    pathParts = fn.split(os.sep)
    assert(len(pathParts) >= 2), pathParts
    
    if fn.endswith('.dat'):
        id1 = pathParts[-2]
        id2 = re.sub('[^0-9]', '', pathParts[-1])
        id = [id1, id2]
    else:
        for i in range(len(pathParts)-2, 0, -1):
    
            if pathParts[i].isdigit():
                id = pathParts[i-1:i+1]
                assert len(id) >= 2, 'Could not extract id from galaxy filename: ' + fn
                break
#        for i in range(len(pathParts)-2, 0, -1):
#            if not pathParts[i].isdigit():
#                id = pathParts[i+1:-1]
#                assert len(id) >= 2, 'Could not extract id from galaxy filename: ' + fn
#                break
    
    return id

def getUniqueRunSpecificId(id=[]):
    return ['run_specific'] + id

def getUniqueWebPath(id=[]):
    return os.sep.join([STATIC_PATH] + getUniqueRunSpecificId(id))
 
def getLoadToGalaxyHistoryURL(fn, genome='hg18', galaxyDataType=None):
    import base64
    
    return URL_PREFIX + '/tool_runner?tool_id=file_import&dbkey=%s&runtool_btn=yes&input=' % genome\
            + base64.urlsafe_b64encode(fn) + ('&datatype='+galaxyDataType if galaxyDataType is not None else '')

def getRelativeUrlFromWebPath(webPath):
    return URL_PREFIX + webPath[len(GALAXY_BASE_DIR):]

def isFlatList(list):
    for l in list:
        if type(l) == type([]):
            return False
    return True    
    
def flattenList(list):
    "recursively flattens a nested list (does not handle dicts and sets..)"
    if isFlatList(list):
        return list
    else:
        return flattenList( reduce(lambda x,y: x+y, list ) )

def listStartsWith(a, b):
    return len(a) > len(b) and a[:len(b)] == b

def isNan(a):
    import numpy    
    
    try:
        return numpy.isnan(a)
    except (TypeError, NotImplementedError):
        return False
        
def reorderTrackNameListFromTopDownToBottomUp(trackNameSource):
    prevTns = []
    source = trackNameSource.__iter__()
    trackName = source.next()
    
    try:
        while True:
            if len(prevTns) == 0 or listStartsWith(trackName, prevTns[0]):
                prevTns.insert(0, trackName)
                trackName = source.next()
                continue
            yield prevTns.pop(0)
    
    except StopIteration:
        while len(prevTns) > 0:
            yield prevTns.pop(0)

R_ALREADY_SILENCED = False
def silenceRWarnings():
    global R_ALREADY_SILENCED
    if not R_ALREADY_SILENCED:
        from gold.application.RSetup import r
        r('sink(file("/dev/null", open="wt"), type="message")')
        R_ALREADY_SILENCED = True

R_ALREADY_SILENCED_OUTPUT = False
def silenceROutput():
    global R_ALREADY_SILENCED_OUTPUT
    if not R_ALREADY_SILENCED_OUTPUT:
        from gold.application.RSetup import r
        r('sink(file("/dev/null", open="wt"), type="output")')
        R_ALREADY_SILENCED_OUTPUT = True

def createHyperBrowserURL(genome, trackName1, trackName2=None, track1file=None, track2file=None, \
                          demoID=None, analcat=None, analysis=None, \
                          configDict=None, trackIntensity=None, method=None, region=None, \
                          binsize=None, chrs=None, chrArms=None, chrBands=None, genes=None): 
    urlParams = []
    urlParams.append( ('dbkey', genome) )
    urlParams.append( ('track1', ':'.join(trackName1)) )
    if trackName2:
        urlParams.append( ('track2', ':'.join(trackName2)) )
    if track1file:
        urlParams.append( ('track1file', track1file) )
    if track2file:
        urlParams.append( ('track2file', track2file) )
    if demoID:
        urlParams.append( ('demoID', demoID) )
    if analcat:
        urlParams.append( ('analcat', analcat) )
    if analysis:
        urlParams.append( ('analysis', analysis) )
    if configDict:
        for key, value in configDict.iteritems():
            urlParams.append( ('config_%s' % key, value) )
    if trackIntensity:
        urlParams.append( ('trackIntensity', trackIntensity) )
    if method:
        urlParams.append( ('method', method) )
    if region:
        urlParams.append( ('region', region) )
    if binsize:
        urlParams.append( ('binsize', binsize) )
    if chrs:
        urlParams.append( ('__chrs__', chrs) )
    if chrArms:
        urlParams.append( ('__chrArms__', chrArms) )
    if chrBands:
        urlParams.append( ('__chrBands__', chrBands) )
    if genes:
        urlParams.append( ('genes', genes) )
    #genes not __genes__?
    #encode?
    
    return URL_PREFIX + '/hyper?' + '&'.join([urllib.quote(key) + '=' + \
                                              urllib.quote(value) for key,value in urlParams])
    
@decorator
def obsoleteHbFunction(func, *args, **kwArgs):
    print 'Warning, this function is going to be phased out of the HB codebase..'
    return func(*args, **kwArgs)

def numAsPaddedBinary(comb, length):
    return '0'*(length-len(bin(comb)[2:]))+bin(comb)[2:]
    
@contextlib.contextmanager
def changedWorkingDir(new_dir):
    orig_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(orig_dir)
        
def convertTNstrToTNListFormat(tnStr, doUnquoting=False):
    tnList = re.split(':|\^|\|', tnStr)
    if doUnquoting:        
        tnList = [urllib.unquote(x) for x in tnList]
    return tnList