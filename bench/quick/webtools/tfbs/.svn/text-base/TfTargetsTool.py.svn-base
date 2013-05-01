from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.aux.tfbs.TfInfo import TfInfo
from quick.application.ProcTrackOptions import ProcTrackOptions
from gold.application.LogSetup import logException, logMessage

#This is a template prototyping GUI that comes together with a corresponding web page.
#

class TfTargetsTool(GeneralGuiTool):
    REGIONS_FROM_HISTORY = 'Regions from history'
    @staticmethod
    def getToolName():
        return "Find gene targets for your TF of interest"

    @staticmethod
    def getInputBoxNames(prevChoices=None):
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Type of analysis: ','Genome: ','Gene source: ','Flank size: ','TF source: ','TF of interest: ']

    @staticmethod    
    def getOptionsBox1():
        "Returns a list of options to be displayed in the first options box"
        return ['Get list of target genes for specified TF']
    
    @staticmethod    
    def getOptionsBox2(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        return ['hg18']

    @staticmethod
    def getOptionsBox3(prevChoices):
        return ['Ensembl genes']

    @staticmethod    
    def getOptionsBox4(prevChoices):
        return ['0','500','2000','10000']
    
    @classmethod
    def getOptionsBox5(cls, prevChoices):
        return TfInfo.getTfTrackNameMappings(prevChoices[1]).keys() + [cls.REGIONS_FROM_HISTORY]

    @classmethod
    #@logException
    def getOptionsBox6(cls, prevChoices):
        if prevChoices[4] == cls.REGIONS_FROM_HISTORY:
            return ('__history__','bed','bedgraph')
        else:
            tfSourceTN = TfInfo.getTfTrackNameMappings(prevChoices[1])[ prevChoices[4] ]
            genome = prevChoices[1]
            subtypes = ProcTrackOptions.getSubtypes(genome, tfSourceTN, True)
            #logMessage(str(subtypes))
            #return ['V$AHR_01']
            return subtypes
            
    @staticmethod
    def getDemoSelections():
        return ['Get list of target genes for specified TF', 'hg18', 'Ensembl genes', '0', 'UCSC tfbs conserved', 'V$AP1_C']
    
    @classmethod    
    def execute(cls, choices, galaxyFn=None, username=''):
        '''Is called when execute-button is pushed by web-user.
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history.
        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).
        choices is a list of selections made by web-user in each options box.
        '''
        #print 'Executing...'
        genome = choices[1]
        flankSize = int(choices[3])
        if choices[4]== cls.REGIONS_FROM_HISTORY:
            from quick.aux.tfbs.GeneTargetsOfTF import GeneTargetsOfRegions
            regionsTn = choices[5].split(':')
            GeneTargetsOfRegions.findGeneTargets('hg18', regionsTn, flankSize, flankSize, galaxyFn)
        else:
            tfSource= choices[4]
            tfChoice = choices[5]
            from quick.aux.tfbs.GeneTargetsOfTF import GeneTargetsOfTF
            GeneTargetsOfTF.findGeneTargets('hg18', tfSource, tfChoice, flankSize, flankSize, galaxyFn)
        
    @staticmethod
    def isPublic():
        return True

    @staticmethod
    def getToolDescription():
        return 'Returns genes assumed to be targeted by a selected TF. \
        The analysis is based on binding sites (predicted or experimentally determined) that falls in the vicinity of genes\
        (determined by flanking).'
        
    @staticmethod
    def getToolIllustration():
        return ['illustrations','tools','TfTargets.png']
        #si = StaticImage(['illustrations','Tools','TfTargets'])
        
