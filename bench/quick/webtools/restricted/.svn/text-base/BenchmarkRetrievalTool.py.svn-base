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
from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.util.StaticFile import RunSpecificPickleFile
import pkg_resources
from quick.util.BenchmarkUtil import BenchmarkUtil
pkg_resources.require('PIL')
from quick.application.ExternalTrackManager import ExternalTrackManager
import sys

'''
This tool is used to retrieve a test set from a benchmark history object
'''
class BenchmarkRetrievalTool(GeneralGuiTool):
    
    @staticmethod
    def getToolName():
        return "Benchmark retrieval tool"

    @staticmethod
    def getInputBoxNames():
        '''
        Specifies a list of headers for the input boxes, and implicitly also the
        number of input boxes to display on the page. The returned list can have
        two syntaxes:
        
            1) A list of strings denoting the headers for the input boxes in
               numerical order.
            2) A list of tuples of strings, where each tuple has
               two items: a header and a key.
        
        The contents of each input box must be defined by the function
        getOptionsBoxK, where K is either a number in the range of 1 to the
        number of boxes (case 1), or the specified key (case 2).
        '''
        return ['Select benchmark:'] #Alternatively: [ ('box1','1'), ('box2','2') ]
    
    @staticmethod    
    def getOptionsBox1():
        return ('__history__','bench')
   
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        '''
        Is called when execute-button is pushed by web-user. Should print
        output as HTML to standard out, which will be directed to a results page
        in Galaxy history. If getOutputFormat is anything else than HTML, the
        output should be written to the file with path galaxyFn. If needed,
        StaticFile can be used to get a path where additional files can be put
        (e.g. generated image files). choices is a list of selections made by
        web-user in each options box.
        '''
        
        # Retrieve the pickled benchmark object from history
        try:
            historyInputTN = choices[0].split(':')
            #same as galaxyFn in execute of create benchmark..
            historyGalaxyFn = ExternalTrackManager.extractFnFromGalaxyTN(historyInputTN) 
            #finds path to static file created for a previous history element, and directs to a pickle file
            randomStatic = RunSpecificPickleFile(historyGalaxyFn) 
            benchmarkSpecification = randomStatic.loadPickledObject()
        except:
            return None
        
        genome = benchmarkSpecification[0]
        benchmarkLevel = benchmarkSpecification[2]
        regionTrackName = benchmarkSpecification[3]
        benchmarkUtil = BenchmarkUtil(galaxyFn, genome)
        
        if benchmarkLevel == 'Base pair probability level':
            return benchmarkUtil.retrieveFeatureTrack(genome, galaxyFn, regionTrackName, benchmarkSpecification[5])
        elif type(regionTrackName) is str: # If string, we're dealing with a single track so just retrieve it
            return benchmarkUtil.retrieveTrack(regionTrackName, galaxyFn)
        elif type(regionTrackName) is list: # If list, we're dealing with a benchmark suite which will have to be zipped
            print benchmarkUtil.retrieveBenchmarkSuiteAsZipFile(regionTrackName)
        else:
            raise Exception('Invalid benchmark')