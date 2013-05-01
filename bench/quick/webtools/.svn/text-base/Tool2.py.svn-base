from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.util.StaticFile import RunSpecificPickleFile

# This is a template prototyping GUI that comes together with a corresponding
# web page.

class Tool2(GeneralGuiTool):
    @staticmethod
    def getToolName():
        '''
        Specifies a header of the tool, which is displayed at the top of the
        page.
        '''
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
        return ['Genome build:','Select problem area:','Select benchmark type:','Select region file from history:','Select prediction file from history:']
    
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
        if prevChoices[1] == 'Motif discovery':
            return ['Sequence level', 'Nucleotide level']
        else:
            return ['Nucleotide level']

    @staticmethod    
    def getOptionsBox4(prevChoices):
        '''
        Region file selection
        '''
        if prevChoices[1] == 'Motif discovery':
            return ('__history__','gtrack')
        elif prevChoices[1] == 'Gene prediction':
            return ('__history__','gtrack')


    @staticmethod    
    def getOptionsBox5(prevChoices):
        '''
        Prediction file selection
        '''
        if prevChoices[1] == 'Motif discovery' and prevChoices[2] == 'Nucleotide level':
            return ('__history__','gtrack')
        elif prevChoices[1] == 'Gene prediction':
            return ('__history__','gtrack')


#    @staticmethod
#    def getDemoSelections():
#        return ['testChoice1','..']
        
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
        if choices[2] == 'Nucleotide level':
            myInfo = [choices[0], choices[1], choices[2], choices[3], choices[4]]
        else:
            myInfo = [choices[0], choices[1], choices[2], choices[3]]
            
        RunSpecificPickleFile(galaxyFn).storePickledObject(myInfo)

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
        
    #@staticmethod
    #def getSubToolClasses():
    #    '''
    #    Specifies a list of classes for subtools of the main tool. These
    #    subtools will be selectable from a selection box at the top of the page.
    #    The input boxes will change according to which subtool is selected.
    #    '''
    #    return None
    #
    #@staticmethod
    #def isPublic():
    #    '''
    #    Specifies whether the tool is accessible to all users. If False, the
    #    tool is only accessible to a restricted set of users as defined in
    #    LocalOSConfig.py.
    #    '''
    #    return False
    #
    #@staticmethod
    #def isRedirectTool():
    #    '''
    #    Specifies whether the tool should redirect to an URL when the Execute
    #    button is clicked.
    #    '''
    #    return False
    #
    #@staticmethod
    #def getRedirectURL(choices):
    #    '''
    #    This method is called to return an URL if the isRedirectTool method
    #    returns True.
    #    '''
    #    return ''
    #
    #@staticmethod
    #def isHistoryTool():
    #    '''
    #    Specifies if a History item should be created when the Execute button is
    #    clicked.
    #    '''
    #    return True
    #
    #@staticmethod
    #def isDynamic():
    #    '''
    #    Specifies whether changing the content of texboxes causes the page to
    #    reload.
    #    '''
    #    return True
    #
    #@staticmethod
    #def getResetBoxes():
    #    '''
    #    Specifies a list of input boxes which resets the subsequent stored
    #    choices previously made. The input boxes are specified by index
    #    (starting with 1) or by key.
    #    '''
    #    return []
    #
    #@staticmethod
    #def getToolDescription():
    #    '''
    #    Specifies a help text in HTML that is displayed below the tool.
    #    '''
    #    return ''
    #
    #@staticmethod
    #def getToolIllustration():
    #    '''
    #    Specifies an id used by StaticFile.py to reference an illustration file
    #    on disk. The id is a list of optional directory names followed by a file
    #    name. The base directory is STATIC_PATH as defined by AutoConfig.py. The
    #    full path is created from the base directory followed by the id.
    #    '''
    #    return None
    #
    #@classmethod
    #def isBatchTool(cls):
    #    '''
    #    Specifies if this tool could be run from batch using the batch. The
    #    batch run line can be fetched from the info box at the bottom of the
    #    tool.
    #    '''
    #    return cls.isHistoryTool()
    #
    #@staticmethod
    #def isDebugMode():
    #    '''
    #    Specifies whether debug messages are printed.
    #    '''
    #    return False
    #
    #@staticmethod    
    #def getOutputFormat(choices):
    #    '''
    #    The format of the history element with the output of the tool. Note
    #    that html output shows print statements, but that text-based output
    #    (e.g. bed) only shows text written to the galaxyFn file.In the latter
    #    case, all all print statements are redirected to the info field of the
    #    history item box.
    #    '''
    #    return 'html'