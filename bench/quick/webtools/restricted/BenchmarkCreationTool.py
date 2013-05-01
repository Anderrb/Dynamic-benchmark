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
from quick.util.BenchmarkUtil import BenchmarkUtil

# This tool handles the creation of a benchmark pickle object,
# which can be used later for retrieving test sets and evaluation of results
class BenchmarkCreationTool(GeneralGuiTool):

    @staticmethod
    def getToolName():
        return "Benchmark creation tool"

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
        return ['Genome build:','Select problem area:','Select test set type:','Select benchmark type:','Select test set:','Select answer:', 'Select feature tracks:']
    
    @staticmethod    
    def getOptionsBox1():
        '''
        Genome build selection
        '''
        return '__genome__'
    
    @staticmethod    
    def getOptionsBox2(prevchoices):
        '''
        Problem areas selection
        '''
        return ['Motif discovery', 'Gene prediction', 'Nucleosome prediction', 'Splice site prediction']
    
    @staticmethod    
    def getOptionsBox3(prevChoices):
        '''
        Benchmark type selection
        '''
        return ['Sequence level', 'Nucleotide level', 'Base pair probability level']
    
    @staticmethod    
    def getOptionsBox4(prevChoices):
        '''
        Benchmark source selection
        '''
        if prevChoices[2] == 'Base pair probability level':
            return ['Single test set']
        else:
            return ['Single test set', 'Benchmark suite']

    @staticmethod    
    def getOptionsBox5(prevChoices):
        '''
        Region file selection
        '''
        if prevChoices[3] == 'Benchmark suite':
            return ''
        elif prevChoices[3] == 'Single test set' and prevChoices[2] == 'Nucleotide level':
            return ('__history__','gtrack', 'bed', 'blasthit')
        else:
            return ('__history__','gtrack', 'bed')

    @staticmethod    
    def getOptionsBox6(prevChoices):
        '''
        Answer file selection
        '''
        if not prevChoices[2] == 'Sequence level' and prevChoices[3] == 'Benchmark suite': 
            return ''
        elif prevChoices[2] == 'Nucleotide level' and prevChoices[3] == 'Single test set':
            return ('__history__','gtrack', 'bed', 'blasthit')
        elif prevChoices[2] == 'Base pair probability level' and prevChoices[3] == 'Single test set':
            return ('__history__','gtrack', 'bed')
    
    @staticmethod
    def getOptionsBox7(prevChoices):
        if prevChoices[2] == 'Base pair probability level':
            return '__track__'
    
    def createBinaryClassificationBenchmarkFromHistoryOnNucleotideLevel(self, choices, galaxyFn):
        genome = choices[0]
        benchmarkType = choices[1]
        benchmarkLevel = choices[2]
        
        benchmarkUtil = BenchmarkUtil(galaxyFn, genome)
        
        regionTrackName = benchmarkUtil.convertToGTrack(choices[4])[0]
        answerTrackName = benchmarkUtil.convertToGTrack(choices[5])[0]
        
        benchmarkSpecification = [genome, benchmarkType, benchmarkLevel, regionTrackName, answerTrackName]
        RunSpecificPickleFile(galaxyFn).storePickledObject(benchmarkSpecification)
    
    def createBinaryClassificationBenchmarkFromHistoryOnSequenceLevel(self, choices, galaxyFn):
        genome = choices[0]
        benchmarkType = choices[1]
        benchmarkLevel = choices[2]
        
        benchmarkUtil = BenchmarkUtil(galaxyFn, genome)
        
        regionTrackName = benchmarkUtil.convertToGTrack(choices[4])[0]
        
        benchmarkSpecification = [genome, benchmarkType, benchmarkLevel, regionTrackName]
        RunSpecificPickleFile(galaxyFn).storePickledObject(benchmarkSpecification)
    
    def createBinaryClassificationBenchmarkFromURLOnNucleotideLevel(self, choices, galaxyFn):
        genome = choices[0]
        benchmarkType = choices[1]
        benchmarkLevel = choices[2]
        
        benchmarkUtil = BenchmarkUtil(galaxyFn, genome)
        
        regionTrackNames = benchmarkUtil.downloadFileFromURL(choices[4])
        answerTrackNames = benchmarkUtil.downloadFileFromURL(choices[5])
        
        benchmarkSpecification = [genome, benchmarkType, benchmarkLevel, regionTrackNames, answerTrackNames]
        RunSpecificPickleFile(galaxyFn).storePickledObject(benchmarkSpecification)
    
    def createBinaryClassificationBenchmarkFromURLOnSequenceLevel(self, choices, galaxyFn):
        genome = choices[0]
        benchmarkType = choices[1]
        benchmarkLevel = choices[2]
        
        benchmarkUtil = BenchmarkUtil(galaxyFn, genome)
        
        regionTrackNames = benchmarkUtil.downloadFileFromURL(choices[4])
        
        benchmarkSpecification = [genome, benchmarkType, benchmarkLevel, regionTrackNames]
        RunSpecificPickleFile(galaxyFn).storePickledObject(benchmarkSpecification)
    
    def createFunctionTrackBenchmarkFromHistoryOnBPPropabilityLevel(self, choices, galaxyFn):
        genome = choices[0]
        benchmarkType = choices[1]
        benchmarkLevel = choices[2]
        featureTrack = choices[6]
        
        benchmarkUtil = BenchmarkUtil(galaxyFn, genome)
        
        regionTrackName = benchmarkUtil.convertToGTrack(choices[4])[0]
        answerTrackName = benchmarkUtil.convertToGTrack(choices[5])[0]
        
        benchmarkSpecification = [genome, benchmarkType, benchmarkLevel, regionTrackName, answerTrackName, featureTrack]
        RunSpecificPickleFile(galaxyFn).storePickledObject(benchmarkSpecification)
    
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
        
        benchmarkCreator = BenchmarkCreationTool()
        benchmarkLevel = choices[2]
        benchmarkSource = choices[3]
        
        if benchmarkLevel == 'Nucleotide level' and benchmarkSource == 'Benchmark suite':
            benchmarkCreator.createBinaryClassificationBenchmarkFromURLOnNucleotideLevel(choices, galaxyFn)
        elif benchmarkLevel == 'Nucleotide level' and benchmarkSource == 'Single test set':
            benchmarkCreator.createBinaryClassificationBenchmarkFromHistoryOnNucleotideLevel(choices, galaxyFn)
        elif benchmarkLevel == 'Sequence level' and benchmarkSource == 'Benchmark suite':
            benchmarkCreator.createBinaryClassificationBenchmarkFromURLOnSequenceLevel(choices, galaxyFn)
        elif benchmarkLevel == 'Sequence level' and benchmarkSource == 'Single test set':
            benchmarkCreator.createBinaryClassificationBenchmarkFromHistoryOnSequenceLevel(choices, galaxyFn)
        elif benchmarkLevel == 'Base pair probability level' and  benchmarkSource == 'Single test set':
            benchmarkCreator.createFunctionTrackBenchmarkFromHistoryOnBPPropabilityLevel(choices, galaxyFn)
        else:
            raise Exception('Invalid benchmark specified')

    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not
        valid, an error text explaining the problem should be returned. The GUI
        then shows this text to the user (if not empty) and greys out the
        execute button (even if the text is empty). If all parameters are valid,
        the method should return None, which enables the execute button.
        '''
        return None
    
    @staticmethod
    def getOutputFormat(choices):
        return 'bench'
        