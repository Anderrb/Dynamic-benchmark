from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.application.ExternalTrackManager import ExternalTrackManager
from quick.util.StaticFile import RunSpecificPickleFile
from quick.application.GalaxyInterface import GalaxyInterface
from quick.util.GTrackConverter import GTrackConverter
import math
from quick.util.BenchmarkEvaluation import BenchmarkEvaluation


class Tool5(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Benchmark evaluation tool"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        #can have two syntaxes: either a list of stings or a list of tuples where each tuple has two items(Name of box on webPage, name of getOptionsBox)
        return ['Select benchmark:', 'Select result files for evaluation:']

    @staticmethod    
    def getOptionsBox1():
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return ('__history__',)
    
    @staticmethod    
    def getOptionsBox2(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        return ('__multihistory__','gtrack', 'weeder', 'meme')
    
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        
        try:
            historyInputTN = choices[0].split(':') #from history
            historyGalaxyFn = ExternalTrackManager.extractFnFromGalaxyTN( historyInputTN) #same as galaxyFn in execute of create benchmark..
            randomStatic = RunSpecificPickleFile(historyGalaxyFn) #finds path to static file created for a previous history element, and directs to a pickle file
            myInfo = randomStatic.loadPickledObject()
        except:
            return None
        
        genome = myInfo[0]
        benchmarkType = myInfo[1]
        predictionTrackNames = choices[1]
        benchmarkEvaluator = BenchmarkEvaluation(galaxyFn, username, genome)
        results = []
        
        if benchmarkType == 'Motif discovery':
            benchmarkLevel = myInfo[2]
            
            if benchmarkLevel == 'Nucleotide level':
                regionTrackName = myInfo[3].split(':')
                answerTrackName = myInfo[4].split(':')
                
                results = benchmarkEvaluator.evaluateMotifDiscoveryBenchmark(benchmarkLevel, predictionTrackNames, answerTrackName, regionTrackName)
            
            elif benchmarkLevel == 'Sequence level':
                answerTrackName = myInfo[3].split(':')
                
                results = benchmarkEvaluator.evaluateMotifDiscoveryBenchmark(benchmarkLevel, predictionTrackNames, answerTrackName)
            else:
                raise TypeError('%s is not a valid Benchmark Level' % benchmarkLevel)
               
        elif benchmarkType == 'Gene prediction':
            regionTrackName = myInfo[3].split(':')
            answerTrackName = myInfo[4].split(':')
            
            results = benchmarkEvaluator.evaluateGenePredictionBenchmark(predictionTrackNames, answerTrackName, regionTrackName)
        elif benchmarkType == 'Nucleosome prediction':
            benchmarkEvaluator.evaluateNucleosomePredictionBenchmark()
        elif benchmarkType == 'Splice site prediction':
            benchmarkEvaluator.evaluateSpliceSitePredictionBenchmark()
        else:
            raise TypeError('%s is not a valid Benchmark Type' % benchmarkType) 
        
        for result in results:
            print result
        
        
    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        return None
    
    @staticmethod
    def isPublic():
        return True
    #
    #@staticmethod
    #def isRedirectTool():
    #    return False
    #
    #@staticmethod
    #def isHistoryTool():
    #    return True
    #
    #@staticmethod
    #def isDynamic():
    #    return True
    #
    #@staticmethod
    #def getResetBoxes():
    #    return []
    #
    #@staticmethod
    #def getToolDescription():
    #    return ''
    #
    #@staticmethod
    #def getToolIllustration():
    #    return None
    #
    #@staticmethod
    #def isDebugMode():
    #    return True
    #
    #@staticmethod    
    #def getOutputFormat(choices):
    #    '''The format of the history element with the output of the tool.
    #    Note that html output shows print statements, but that text-based output
    #    (e.g. bed) only shows text written to the galaxyFn file.
    #    '''
    #    return 'html'
    #
