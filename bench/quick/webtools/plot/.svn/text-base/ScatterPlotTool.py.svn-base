from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.util.CommonFunctions import createHyperBrowserURL
#This is a template prototyping GUI that comes together with a corresponding web page.
#

class ScatterPlotTool(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Scatter plot of track relation"

    @staticmethod
    def getInputBoxNames(prevChoices=None):
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Genome build: ', 'First track', 'Second track']

    @staticmethod    
    def getOptionsBox1():
        "Returns a list of options to be displayed in the first options box"
        return '__genome__'
    
    @staticmethod    
    def getOptionsBox2(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        return '__track__'
    
    @staticmethod    
    def getOptionsBox3(prevChoices):
        return '__track__'

    #@staticmethod    
    #def getOptionsBox4(prevChoices):
    #    return ['']
    
    @staticmethod
    def isRedirectTool():
        return True
    
    @staticmethod
    def getRedirectURL(choices):
        genome, trackName1, tf1 = ScatterPlotTool._getBasicTrackFormat(choices, 1)
        trackName2, tf2 = ScatterPlotTool._getBasicTrackFormat(choices, 2)[1:]
        
        if tf1 == 'function' and tf2 == 'function':
            analysis = 'Scatter plot (F, F)'
        elif tf1.split()[-1] in ['points', 'segments'] and tf2 == 'function':
            analysis = 'Scatter plot (P, F)'
        elif tf1 == 'function' and tf2.split()[-1] in ['points', 'segments']:
            analysis = 'Scatter plot (F, P)'
        elif tf1.split()[-1] in ['points', 'segments'] and tf2.split()[-1] in ['points', 'segments']:
            analysis = 'Scatter plot (P, P)'
        else:
            analysis = ''
        
        return createHyperBrowserURL(genome, trackName1, trackName2, analcat='Descriptive statistics', analysis=analysis)
    
    @staticmethod
    def getDemoSelections():
        return ['sacCer1','DNA structure:Melting:Melting map','Genes and gene subsets:Exons']
        
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        '''Is called when execute-button is pushed by web-user.
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history.
        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).
        choices is a list of selections made by web-user in each options box.
        '''
        print 'Executing...'

    @staticmethod
    def isPublic():
        return True
    #

    @staticmethod
    def getToolDescription():
        from gold.result.HtmlCore import HtmlCore
        core = HtmlCore()
        core.paragraph('Creates a scatter plot of the relation between two tracks in local bins along the genome.')
        core.divider()
        core.paragraph('Each point in the scatter plot is a summarized value of the two tracks (as x and y-values) in a given bin. Thus, a point corresponds to a bin, the x-axis corresponds to first track, and the y-axis corresponds to second track.')
        core.divider()
        core.paragraph('First, select a genome and two track of interest. Then a full analysis specification page appears, where one can directly start a basic analysis or specify further details on the analysis of interest.')
        return str(core)

    @staticmethod    
    def validateAndReturnErrors(choices):
        genome, trackName1, tf1 = ScatterPlotTool._getBasicTrackFormat(choices, 1)
        trackName2, tf2 = ScatterPlotTool._getBasicTrackFormat(choices, 2)[1:]
        if not (ScatterPlotTool._isValidTrack(choices, 1) and ScatterPlotTool._isValidTrack(choices, 2)):
            return ''
        if not all(x in ['points', 'valued points', 'segments', 'valued segments', 'function'] for x in [tf1, tf2]):
            return 'Basic track format must be one of (valued) points, (valued) segments or function. ' +\
                   'Current: %s (track 1), %s (track 2)' % (tf1, tf2)

    #@staticmethod
    #def getToolIllustration():
    #    return None
    #
    #@staticmethod
    #def isDebugMode():
    #    return True