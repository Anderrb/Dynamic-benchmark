from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.application.ExternalTrackManager import ExternalTrackManager
from gold.application.StatRunner import *
from quick.application.UserBinSource import UserBinSource
from gold.result.HtmlCore import HtmlCore

#This is a template prototyping GUI that comes together with a corresponding web page.
#

class CreateFunctionTrackAsDistanceToNearestSegments(GeneralGuiTool):
    
    @staticmethod
    def getToolName():
        return "Create function track of distance from each bp to nearest segment of selected track"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        #can have two syntaxes: either a list of stings or a list of tuples where each tuple has two items(Name of box on webPage, name of getOptionsBox)
        return ['Genome build:', 'Select track:','Select transformation:']
    
    
    @staticmethod    
    def getOptionsBox1():
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return '__genome__'
    
    @staticmethod    
    def getOptionsBox2(prevChoices):
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return '__track__'
    
    @staticmethod    
    def getOptionsBox3(prevChoices):
        return ['No transformation','Logarithmic (log10(x))', 'Fifth square root (x**0.2)']

    #@staticmethod    
    #def getOptionsBox4(prevChoices):
    #    return ['']

    #@staticmethod
    #def getDemoSelections():
    #    return ['testChoice1','..']
        
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        '''Is called when execute-button is pushed by web-user.
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history.
        If getOutputFormat is anything else than HTML, the output should be written to the file with path galaxyFn.
        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).
        choices is a list of selections made by web-user in each options box.
        '''
        genome = choices[0]
        trackName = choices[1].split(':')
        
        galaxyOutTrackName = 'galaxy:hbfunction:%s:Create function track of distance to nearest segment' % galaxyFn
        outTrackName = ExternalTrackManager.getStdTrackNameFromGalaxyTN(galaxyOutTrackName.split(':'))
        
        if choices[2] == 'No transformation':
            valTransformation = 'None'
        elif choices[2] =='Logarithmic (log10(x))':
            valTransformation = 'log10'
        elif choices[2] == 'Fifth square root (x**0.2)':
            valTransformation = 'power0.2'
        
        analysisDef ='[dataStat=MakeDistanceToNearestSegmentStat] [valTransformation=%s][outTrackName=' % valTransformation \
                     + '^'.join(outTrackName) + '] -> CreateFunctionTrackStat'
        #userBinSource, fullRunArgs = GalaxyInterface._prepareRun(trackName, None, analysisDef, '*', '*', genome)
        #
        #for el in userBinSource:
        #    print el.chr, el.start, el.end
            
        from quick.application.GalaxyInterface import GalaxyInterface

        print GalaxyInterface.getHbFunctionOutputBegin(galaxyFn, withDebug=False)
        
        GalaxyInterface.runManual([trackName], analysisDef, '*', '*', genome, username=username, printResults=False, printHtmlWarningMsgs=False)
        #job = AnalysisDefJob(analysisDef, trackName, None, userBinSource).run()
        
        print GalaxyInterface.getHbFunctionOutputEnd('A custom track has been created by finding the bp-distance to the nearest segment', withDebug=False)
        

    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        if not choices[0]:
            return 'Please select a genome'
            
        if not choices[1]:
            return 'Please select a track'
        
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
    @staticmethod    
    def getOutputFormat(choices):
        '''The format of the history element with the output of the tool.
        Note that html output shows print statements, but that text-based output
        (e.g. bed) only shows text written to the galaxyFn file.
        '''
        return 'hbfunction'