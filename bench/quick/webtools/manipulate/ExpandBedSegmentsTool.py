from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.application.GalaxyInterface import GalaxyInterface
from collections import OrderedDict
from quick.application.ExternalTrackManager import ExternalTrackManager
#This is a template prototyping GUI that comes together with a corresponding web page.
#

class ExpandBedSegmentsTool(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Expand BED segments"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        #can have two syntaxes: either a list of stings or a list of tuples where each tuple has two items(Name of box on webPage, name of getOptionsBox)
        return [('Genome build:', 'genome'), \
                ('Segment track from history (BED-format):', 'history'), \
                ('Before expanding, treat track as:', 'conversion'), \
                ('Upstream flank (in bps):', 'upstream'), \
                ('Downstream flank (in bps):', 'downstream'), \
                ('Handle segments crossing chromosome borders by:', 'chrBorderHandling')]

    @staticmethod    
    def getOptionsBoxGenome():
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return '__genome__'
    
    @staticmethod    
    def getOptionsBoxHistory(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        return ('__history__', 'bed')
    
    _TRACK_TYPE_CONVERSION_OPTIONS = \
        OrderedDict([("Original format ('Segments')", 'segments'),\
                     ("The upstream end point of every segment (converted from 'Segments')", 'upstream'),\
                     ("The middle point of every segment (converted from 'Segments')", 'middle'),\
                     ("The downstream end point of every segment (converted from 'Segments')", 'downstream')])
      
    @staticmethod    
    def getOptionsBoxConversion(prevChoices):
        if prevChoices.history:
            return ExpandBedSegmentsTool._TRACK_TYPE_CONVERSION_OPTIONS.keys()
            
    @staticmethod    
    def getOptionsBoxUpstream(prevChoices):
        if prevChoices.history:
            return '0', 1
        
    @staticmethod    
    def getOptionsBoxDownstream(prevChoices):
        if prevChoices.history:
            return '0', 1
            
    @staticmethod    
    def getOptionsBoxChrBorderHandling(prevChoices):
        if prevChoices.history:
            return ['Cropping','Removing']
            
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
        
        inFn = ExternalTrackManager.extractFnFromGalaxyTN(choices.history.split(':'))
        treatTrackAs = ExpandBedSegmentsTool._TRACK_TYPE_CONVERSION_OPTIONS[choices.conversion]
            
        GalaxyInterface.expandBedSegments(inFn, galaxyFn, choices.genome, \
                                          int(choices.upstream), int(choices.downstream), \
                                          treatTrackAs, removeChrBorderCrossing=(choices.chrBorderHandling=='Removing'))
    

    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        if not choices.history:
            return ''
    
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
    @staticmethod
    def getToolDescription():
        from gold.result.HtmlCore import HtmlCore
        core = HtmlCore()
        core.paragraph('This tool expands the segments of a file in one or both directions. '\
                       'It can also flatten a segment to its start, middle or end point before expading.')
        core.unorderedList(['Select the genome',
                            'Select the file you to expand (BED-format). ',
                            'Select whether you want to treat the track as segments, or as start, middle or end points. ',
                            'Type in the number of base pairs you want to expand the segments in upstream and downstream direction. ',
                            'Select whether you would like to remove segments that, after expansion, crosses chromosome border, or just crop them.',
                            'Click execute.' ])
        return str(core)
        return ''
        


    #
    #@staticmethod
    #def getToolIllustration():
    #    return None
    #@staticmethod
    #def isBatchTool():
    #    return False
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
        return 'bed'
    #
