from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.util.StaticFile import RunSpecificPickleFile
from quick.application.ExternalTrackManager import ExternalTrackManager
#This is a template prototyping GUI that comes together with a corresponding web page.
#

class DownloadHistoryItems(GeneralGuiTool):
  
    @staticmethod
    def getToolName():
        return "Download History items locally"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        #can have two syntaxes: either a list of stings or a list of tuples where each tuple has two items(Name of box on webPage, name of getOptionsBox)
        return ['Select Histories','Question','Answer']

    @staticmethod    
    def getOptionsBox1():
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return ('__history__',) #gives all history elements
#        return '__multihistory__',
    
        
    @staticmethod    
    def getOptionsBox2(prevChoices):
        try:
            historyInputTN = prevChoices[0].split(':') #from history
            historyGalaxyFn = ExternalTrackManager.extractFnFromGalaxyTN( historyInputTN) #same as galaxyFn in execute of create benchmark..
            randomStatic = RunSpecificPickleFile(historyGalaxyFn) #finds path to static file created for a previous history element, and directs to a pickle file
            myInfo = randomStatic.loadPickledObject()
        
            return [myInfo[0]]
        except:
            return None

    @staticmethod    
    def getOptionsBox3(prevChoices):
        if prevChoices[1] is not None:
            return ''

    #@staticmethod
    #def getDemoSelections():
    #    return ['testChoice1','..']
        
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        historyInputTN = choices[0].split(':') #from history
        historyGalaxyFn = ExternalTrackManager.extractFnFromGalaxyTN( historyInputTN) #same as galaxyFn in execute of create benchmark..
        randomStatic = RunSpecificPickleFile(historyGalaxyFn) #finds path to static file created for a previous history element, and directs to a pickle file
        myInfo = randomStatic.loadPickledObject()

        if myInfo[1] == choices[2]:
            print "Your answer was correct!"
        else:
            print "You answered %s but the right answer was %s" % (myInfo[1], choices[2])

#        galaxyTnList = [unquote(v).split(':') for v in choices[0].values() if v]
#        for galaxyTn in galaxyTnList:
#            fnSource = ExternalTrackManager.extractFnFromGalaxyTN(galaxyTn)
#            
    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        return None
    
    #@staticmethod
    #def isPublic():
    #    return False
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
