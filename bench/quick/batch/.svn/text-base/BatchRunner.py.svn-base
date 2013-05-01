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

import sys
import os

from gold.application.StatRunner import AnalysisDefJob, AssemblyGapJob
from gold.origdata.GenomeElementSource import GenomeElementSource
from gold.result.Results import Results
from gold.track.Track import Track
from gold.util.CustomExceptions import InvalidRunSpecException, IdenticalTrackNamesError

from quick.batch.SuperBatchConverter import SuperBatchConverter
from quick.application.UserBinSource import UserBinSource
from quick.util.CommonFunctions import wrapClass

from quick.application.ProcTrackOptions import ProcTrackOptions
from config.Config import DEFAULT_GENOME, DebugConfig, BATCH_COL_SEPARATOR
from quick.application.ProcTrackNameSource import ProcTrackNameSource
from gold.application.LogSetup import logMessage, logException

from gold.description.Analysis import Analysis
import time
from quick.util.CommonFunctions import convertTNstrToTNListFormat

class BatchRunner:    
    @staticmethod
    def runFromFn(batchFn, genome, fullAccess):
        return BatchRunner.runManyLines([line for line in open(batchFn, genome, fullAccess)])

    @staticmethod
    def runManyLines(batchLines, genome, fullAccess, useBatchId=True):
        #fixme: useBatchId is currently ignored! Do something with it if this was a meaningful name from a standard batch run....

        resList = []
        for line in batchLines:
            resList.append(BatchRunner.runJob(line, genome, fullAccess) ) 
        return resList
            
    @staticmethod
    def runJob(batchLine, genome, fullAccess):
        if batchLine[0] == '#' or batchLine.strip()=='':
            return
            
        from urllib import unquote
        
        #Split and check number of columns
        cols = [x for x in batchLine.strip().split(BATCH_COL_SEPARATOR)]
        if len(cols) != 6:
            results = Results(['N/A'],['N/A'],'N/A')
            #results.addResultComponent( 'Invalid',InvalidRunResultComponent('Error in batch specification. 6 columns are required, while '\
            #                            + str(len(cols)) + ' are given.'))
            results.addError(InvalidRunSpecException('Error in batch specification. 6 columns are required, while '\
                                        + str(len(cols)) + ' are given: ' + batchLine))
            return results

        #print 'COL2: ',cols[2]
        cols[2] = unquote(cols[2])
        #print 'COL2: ',cols[2]
        from quick.application.ExternalTrackManager import ExternalTrackManager
        if ExternalTrackManager.isGalaxyTrack(cols[2].split(':')):
            cols[2] = ExternalTrackManager.extractFnFromGalaxyTN(cols[2].split(':'))
            #print 'COL2: ',cols[2]
        
        try:
            from quick.application.GalaxyInterface import GalaxyInterface
            trackName1 = [unquote(x) for x in cols[3].split(':')]
            trackName2 = [unquote(x) for x in cols[4].split(':')]
            cleanedTrackName1, cleanedTrackName2 = GalaxyInterface._cleanUpTracks([trackName1, trackName2], genome, realPreProc=True)

            cleanedTrackName1 = BatchRunner._inferTrackName(':'.join(cleanedTrackName1), genome, fullAccess)
            cleanedTrackName2 = BatchRunner._inferTrackName(':'.join(cleanedTrackName2), genome, fullAccess)
            
        except (InvalidRunSpecException,IdenticalTrackNamesError), e:
            if DebugConfig.PASS_ON_BATCH_EXCEPTIONS:
                raise
            results = Results(['N/A'],['N/A'],'N/A')
            results.addError(e)
            return results

        errorResult, userBinSource = BatchRunner._constructBins(cols[1], cols[2], genome, cleanedTrackName1, cleanedTrackName2)
        if errorResult is not None:
            return errorResult
        
        statClassName, paramDict = BatchRunner._parseClassAndParams(cols[5])
                            
        #Try a full run, and return either results or an exception
        try:
            #track = Track(trackName1)
            #track2 = Track(trackName2)
            #if 'tf1' in paramDict:
            #    track.setFormatConverter(formatConverter)
            
            #results = StatRunner.run(userBinSource , Track(trackName1), Track(trackName2), \
            #                         wrapClass(STAT_CLASS_DICT[statClassName], keywords=paramDict) )
            #results = StatRunner.run(userBinSource , track, track2, \
            #                         wrapClass(STAT_CLASS_DICT[statClassName], keywords=paramDict) )
            fullRunParams = {}
            
            #if galaxyFn == None: #then this is a test
            uniqueId = time.time()
            #else:
                #uniqueId = extractIdFromGalaxyFn(galaxyFn)[1]
                
            fullRunParams["uniqueId"] = uniqueId
            
            trackNameIntensity = []
            if 'trackNameIntensity' in paramDict:
                #fullRunParams['trackNameIntensity'] = paramDict['trackNameIntensity'].replace('_',' ').split(':')
                from quick.application.GalaxyInterface import GalaxyInterface
                import re
                #trackNameIntensity = re.split(':|\|', paramDict['trackNameIntensity'])
                trackNameIntensity = convertTNstrToTNListFormat(paramDict['trackNameIntensity'])
                #print "HERE: ",trackNameIntensity
                cleanedTrackNameIntensity = GalaxyInterface._cleanUpTracks([trackNameIntensity], genome, realPreProc=True)[0]

                fullRunParams['trackNameIntensity'] = '|'.join(tuple(BatchRunner._inferTrackName(':'.join(cleanedTrackNameIntensity), genome, fullAccess))) #join by : for inferTrackName, then by '|' for further use..
                del paramDict['trackNameIntensity']
                
            analysisDefParams = [ '[' + key + '=' + value + ']' for key,value in paramDict.items()]
            analysisDef = ''.join(analysisDefParams) + '->' + statClassName

            from quick.application.GalaxyInterface import GalaxyInterface
            print 'Corresponding batch-run line:<br>' + \
                    GalaxyInterface._revEngBatchLine(trackName1, trackName2, trackNameIntensity, analysisDef, cols[1], cols[2], genome) + '<br><br>'
            
            results = AnalysisDefJob(analysisDef, cleanedTrackName1, cleanedTrackName2, userBinSource, **fullRunParams).run()
            presCollectionType = results.getPresCollectionType()

            if len(results.getResDictKeys()) > 0 and GalaxyInterface.APPEND_ASSEMBLY_GAPS and presCollectionType=='standard':
                gapRes = AssemblyGapJob(userBinSource, genome, uniqueId=uniqueId).run()
                results.includeAdditionalResults(gapRes, ensureAnalysisConsistency=False)

        except Exception, e:
            #print 'NOWAG BExc'
            results = Results(cleanedTrackName1, cleanedTrackName2, statClassName)
            results.addError(e)
            logException(e,message='Error in batch run')
            if DebugConfig.PASS_ON_BATCH_EXCEPTIONS:
                raise
            return results
        
        return results
                

    @staticmethod
    def _constructBins(regSpec, binSpec, genome, trackName1, trackName2):
        #Construct and check bins
        try:
            #userBinSource= UserBinSource(regSpec, binSpec)
            from quick.application.GalaxyInterface import GalaxyInterface
#            from config.Config import DEFAULT_GENOME
            userBinSource = GalaxyInterface._getUserBinSource(regSpec, binSpec, genome, trackName1, trackName2)
            return [None, userBinSource]
        except Exception, e:
            #results = Results(trackName1, trackName2, statClassName)
            results = Results([],[],'')
            results.addError(InvalidRunSpecException('Error in specification of analysis region or binsize: ' + str(e)))
            logMessage('Error in specification of analysis region (' + regSpec +') or binsize: (' + binSpec + ')')
            if DebugConfig.PASS_ON_BATCH_EXCEPTIONS:
                raise
            return [results, None]

    @staticmethod
    def _parseClassAndParams(spec):        
        if '(' in spec:
            assert(spec.count('(') == spec.count(')') == 1)
            paramSpec = spec[spec.find('(')+1: spec.find(')')]
            paramDict = dict([param.split('=') for param in paramSpec.split(',')])
            return spec[0: spec.find('(')], paramDict
        else:
            return spec, {}

    @staticmethod
    def _inferTrackName(rawTN, genome, fullAccess):
        #genome = DEFAULT_GENOME
        if rawTN.lower() in ['blank','none','dummy','_',' ','']:
            return None
        
        #trackName = rawTN.replace('_',' ').split(':')
        #trackName = rawTN.split(':')
        
        trackName = convertTNstrToTNListFormat(rawTN)
        if ProcTrackOptions.isValidTrack(genome, trackName, fullAccess):
            return trackName
        else:
            raise InvalidRunSpecException('Error in trackname specification. \''\
                                          + rawTN + '\' does not match any tracknames. This may be because of limited user permissions.')

            #print 'No exact match for track name (%s). Searching for submatch in genome %s. ' % (rawTN, genome)
            #candidates = [candidate for candidate in ProcTrackNameSource(genome, fullAccess, avoidLiterature=True)\
            #    #if rawTN.lower() in (':'.join(candidate)).replace(' ','_').lower()]
            #    if rawTN.lower() in (':'.join(candidate)).lower()]
            #if len(candidates) == 0:
            #    raise InvalidRunSpecException('Error in trackname specification. \''\
            #                                  + rawTN + '\' does not match any tracknames. This may be because of limited user permissions.')
            #elif len(candidates) > 1:
            #    raise InvalidRunSpecException('Error in trackname specification. \''\
            #                                  + rawTN + '\' matches more than one trackname: \n- ' + '\n- '.join([':'.join(x) for x in candidates]))
            #else:
            #    return candidates[0]

    
class SuperBatchRunner:
    "For parsing super-batch format to standard batch format."
    @staticmethod
    def runManyLines(superLines, genome, fullAccess):
        batchLines = SuperBatchConverter.super2batch(superLines, genome)
        return BatchRunner.runManyLines(batchLines, genome, fullAccess, useBatchId=False)
#        except Exception, e:
#            results = Results(['N/A'],['N/A'],'N/A')
#            results.addError(InvalidRunSpecException('Error in batch specification: ' + str(e)))
#            return [results]


if __name__ == '__main__':
    if len(sys.argv != 3):
        print 'Syntax: BatchRunner genome batchFn'
    else:
        BatchRunner.runFromFn(sys.argv[2], sys.argv[1], fullAccess=True)
