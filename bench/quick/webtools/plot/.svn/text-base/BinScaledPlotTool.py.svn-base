from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.util.CommonFunctions import createHyperBrowserURL
#This is a template prototyping GUI that comes together with a corresponding web page.
#

class BinScaledPlotTool(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Plot of progression pattern"

    @staticmethod
    def getInputBoxNames(prevChoices=None):
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Genome build: ', 'Track', 'Plot: ']

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
        genome, trackName, tf = BinScaledPlotTool._getBasicTrackFormat(prevChoices)
        if tf != '' and tf.split()[-1] == 'points':
            return ['Count']
        elif tf != '' and tf.split()[-1] == 'segments':
            return ['Count', 'Base pair overlap']
        elif tf == 'function':
            return ['Function values']
        else:
            return None

    #@staticmethod    
    #def getOptionsBox4(prevChoices):
    #    return ['']
    @staticmethod
    def isRedirectTool():
        return True
    
    @staticmethod
    def getRedirectURL(choices):
        genome = choices[0]
        trackName1 = choices[1].split(':')
        plot = choices[2]
        if plot == 'Count':
            analysis = 'Bin-scaled distribution (points)'
        elif plot == 'Base pair overlap':
            analysis = 'Bin-scaled distribution (segments)'
        elif plot == 'Function values':
            analysis = 'Bin-scaled distribution (function)'

        return createHyperBrowserURL(genome, trackName1, [''], analcat='Descriptive statistics', \
                                     analysis=analysis, configDict={'Resolution': '100'})
    
    @staticmethod
    def getDemoSelections():
        return ['sacCer1','Genes and gene subsets:Exons', 'Count']
        
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
        core.paragraph('Creates a plot of a common progression pattern of a track appearing across different bins. For each bin, the track values are summarized and scaled along the bin. Then, the average of such summarized and scaled values across bins are found.')
        core.paragraph('First, select a genome and a track of interest. Then a full analysis specification page appears, where one can directly start a basic analysis or specify further details on the analysis of interest. Here, you can select the bins across which the progression pattern is plotted.')
        return str(core)
    
    @staticmethod    
    def validateAndReturnErrors(choices):
        if not BinScaledPlotTool._isValidTrack(choices):
            return ''
        
        if len(choices) != 3:
            return 'Track format must be one of (valued) points, (valued) segments or function.'
                
    #    
    #@staticmethod
    #def getToolIllustration():
    #    return None
    #
    #@staticmethod
    #def isDebugMode():
    #    return True