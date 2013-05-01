from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.aux.TrackIntersection import GeneIntersection
from quick.application.ProcTrackOptions import ProcTrackOptions
from quick.util.GenomeInfo import GenomeInfo

#This is a template prototyping GUI that comes together with a corresponding web page.
#

class ExtractIntersectingGenesTool(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Extract IDs of intersecting genes"

    @staticmethod
    def getInputBoxNames(prevChoices=None):
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Genome','Track of interest','Gene source', 'Flank size']


    @staticmethod    
    def getOptionsBox1():
        "Returns a list of options to be displayed in the first options box"
        return '__genome__'
    
    @staticmethod    
    def getOptionsBox2(prevChoices):
        "Returns a list of options to be displayed in the first options box"
        genome = prevChoices[0]    
        return '__track__' #+ genome
    
    @staticmethod    
    def getOptionsBox3(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        return ['Ensembl']

    @staticmethod    
    def getOptionsBox4(prevChoices):
        return ['0','500','2000','10000']
    
    @staticmethod
    def getDemoSelections():
        return ['hg18','DNA variation:SNPs:HapMap','Ensembl','0']

    #@staticmethod    
    #def getOptionsBox3(prevChoices):
    #    return ['']

    #@staticmethod    
    #def getOptionsBox4(prevChoices):
    #    return ['']
        
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        '''Is called when execute-button is pushed by web-user.
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history.
        If needed, can call _getStaticPath to get a path where additional files can be put (e.g. generated image files)
        choices is a list of selections made by web-user in each options box.
        '''
        #print 'choices: ', choices
        genome = choices[0]
        queryTrackStr = choices[1]
        queryTrack = queryTrackStr.split(':')
        
        geneSource = choices[2]
        upFlankSize = downFlankSize = int(choices[3])
        geneIntersection = GeneIntersection(genome, geneSource, queryTrack, galaxyFn)
        geneIntersection.expandReferenceTrack(upFlankSize, downFlankSize)
        expansionStr = ', after expansion,' if not (upFlankSize == downFlankSize == 0) else ''                
        print '<p>There are %i %s-genes that%s intersect elements from your query track (%s).</p>' % (geneIntersection.getNumberOfIntersectedBins(), geneSource, expansionStr, queryTrackStr)
        
        idFileNamer = geneIntersection.getGeneIdStaticFileWithContent()
        print '<p>', idFileNamer.getLink('Download list'), ' of all %s IDs intersecting query track.</p>' % (geneSource)

        regFileNamer = geneIntersection.getIntersectedRegionsStaticFileWithContent()
        print '<p>', regFileNamer.getLink('Download bed-file'), ' of all %s gene regions intersecting query track.</p>' % (geneSource)
        
    #@staticmethod    
    #def _getStaticPath(galaxyId):
    #    return '/'.join([STATIC_PATH, galaxyId])
    
    @staticmethod
    def isPublic():
        return True
    
       
    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (also if the text isempty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        genome, tn, tf = ExtractIntersectingGenesTool._getBasicTrackFormat(choices)
        geneRegsTrackName = GenomeInfo.getStdGeneRegsTn(genome)
        
        if not ExtractIntersectingGenesTool._isValidTrack(choices):
            return ""
            return "The selected track (%s) is not valid." % ':'.join(tn)        
        
        if tf.split()[-1] not in ['points', 'segments']:
            return "The track format of the selected track must be either points or segments. Currently: %s" % tf
        
        if not ProcTrackOptions.isValidTrack(genome, geneRegsTrackName, True):
            return "The track used for gene ids (%s) is not valid. This is an internal error." % ':'.join(geneRegsTrackName)        
        
    
    @staticmethod
    def getToolDescription():
        return '''
        <p>This tool finds the IDs of genes intersecting with the selected track.</p>
        <ul>
        <li>Select a track. The format of the track should be either 'points' or 'segments'.
        <li>Select the gene source from which to fetch the IDs
        <li>If you want to expand the segments of the track before intersection, select the flank size.
        <li>Click "Execute"
        </ul>
        '''
        
    #@staticmethod
    #def getToolIllustration():
    #    return None
    #
    #@staticmethod
    #def isDebugMode():
    #    return True