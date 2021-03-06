from quick.webtools.GeneralGuiTool import GeneralGuiTool
from gold.result.HtmlCore import HtmlCore

#This is a template prototyping GUI that comes together with a corresponding web page.
#

class SmoothedTrackTool(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Create smoothing/density track"

    @staticmethod
    def getInputBoxNames(prevChoices=None):
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Genome','Input track','Smoothing type: ', 'Sliding window size: ']#, 'Create track as: ', 'Output trackname: ']


    @staticmethod    
    def getOptionsBox1():
        "Returns a list of options to be displayed in the first options box"
        #return ['testMit','hg18']
        return '__genome__'

    #@staticmethod    
    #def getOptionsBox2(prevChoices):
    #    "Returns a list of options to be displayed in the first options box"
    #    if prevChoices[0] == 'testMit':
    #        return ['somePoints','someSegments','function']
    #    else:
    #        return ['Virus','Genes','Melting']

    @staticmethod    
    def getOptionsBox2(prevChoices):
        return '__track__'
    
    @classmethod    
    def getOptionsBox3(cls, prevChoices):
        tf = cls._getBasicTrackFormat(prevChoices)[-1]
        if tf != '' and tf.split()[-1] == 'points':
            return ['Point density in window', 'Number of points in window']
        elif tf != '' and tf.split()[-1] == 'segments':
            return ['Coverage proportion in window', 'Density of segments in window (based on number of segments)', 'Number of segments in window']
        elif tf == 'function':
            return ['Mean function value in window', 'Maximum function value in window', 'Minimum function value in window']
        else:
            return None
            #assert False, 'TF: '+tf
        
    @staticmethod    
    def getOptionsBox4(prevChoices):
        return '21' if SmoothedTrackTool._isValidTrack(prevChoices) else None

    #@staticmethod
    #def getOptionsBox5(prevChoices):
    #    return ['History element', 'HyperBrowser track'] if SmoothedTrackTool._isValidTrack(prevChoices) else None
    #
    #@staticmethod
    #def getOptionsBox6(prevChoices):
    #    return '' if prevChoices[4] == 'HyperBrowser track' else None

    @staticmethod
    def getDemoSelections():
        #return ['testMit','someSegments', 'Coverage proportion in window', '21', 'History element', '']
        return ['phagelambda','Sequence:Nmers:aca', 'Point density in window', '21']
        
    @classmethod    
    def execute(cls, choices, galaxyFn=None, username=''):
        '''Is called when execute-button is pushed by web-user.
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history.
        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).
        choices is a list of selections made by web-user in each options box.
        '''        
        genome, inTrackName, tf = cls._getBasicTrackFormat(choices)
        statistic = choices[2]
        winSize = int(choices[3])
        
        #print 'Format: ', tf
        
        if tf.split()[-1] == 'points':
            if statistic == 'Point density in window':
                func = lambda tv: len(tv.startsAsNumpyArray())*1.0/len(tv)
            elif statistic == 'Number of points in window':
                func = lambda tv: len(tv.startsAsNumpyArray())

        elif tf.split()[-1] == 'segments':
            if statistic == 'Coverage proportion in window':
                func = lambda tv: sum(len(x) for x in tv)*1.0/len(tv)
            elif statistic == 'Density of segments in window (based on number of segments)':
                func = lambda tv: len(tv.startsAsNumpyArray())*1.0/len(tv)
            elif statistic == 'Number of segments in window':
                func = lambda tv: len(tv.startsAsNumpyArray())
                
        elif tf == 'function':
            if statistic == 'Mean function value in window':
                func = lambda tv: tv.valsAsNumpyArray().sum()/len(tv)
            elif statistic == 'Maximum function value in window':
                func = lambda tv: tv.valsAsNumpyArray().max()
            elif statistic == 'Minimum function value in window':
                func = lambda tv: tv.valsAsNumpyArray().min()
        else:
            raise
        #if choices[4] == 'HyperBrowser track':
        #    outTrackName = choices[5]
        #else:
        outTrackName = 'galaxy:hbfunction:%s:Create smoothing or density track' % galaxyFn
        
        from quick.application.GalaxyInterface import GalaxyInterface
        print GalaxyInterface.getHbFunctionOutputBegin(galaxyFn, withDebug=True)
        
        #print 'cleaning..'
        #print 'inTrackName: ', inTrackName 
        #inTrackName = GalaxyInterface._cleanUpTracks([inTrackName], genome, True)[0]
        #print 'creating..'
        GalaxyInterface.createCustomTrack(genome, inTrackName, outTrackName, winSize, func, username)
        
        infoMsg = 'A custom track has been created by applying the function "%s" on elements of the track "%s" in a sliding window of size %i along the genome "%s".' % (statistic, ':'.join(inTrackName), winSize, genome)
        print GalaxyInterface.getHbFunctionOutputEnd(infoMsg, withDebug=True)
        
    #@staticmethod    
    #def _getBasicTrackFormat(choices):
    #    genome = choices[0]
    #    #if genome == 'testMit':
    #    tn = choices[1].split(':')
    #    #print 'SPLITTED: ',tn
    #    #else:
    #    #    if choices[1] == 'Genes':
    #    #        tn = 'Genes_and_gene_subsets:Genes:Ensembl'.replace('_',' ').split(':')
    #    #    elif choices[1] == 'Virus':
    #    #        tn = 'Phenotype_and_disease_associations:Assorted_experiments:Virus_integration,_Derse_et_al._(2007):HPV'.replace('_',' ').split(':')
    #    #    elif choices[1] == 'Melting':
    #    #        tn = 'DNA_structure:Melting:Meltmap'.replace('_',' ').split(':')
    #    from quick.application.GalaxyInterface import GalaxyInterface
    #    if GalaxyInterface.isNmerTrackName(genome, tn):
    #        tfName = 'Unmarked points'
    #    else:
    #        tfName = TrackInfo(genome, tn).trackFormatName
    #    return genome, tn, (tfName.lower().split()[-1] if tfName is not '' else '')

    @staticmethod
    def isPublic():
        return True

    @staticmethod
    def getToolDescription():
        from gold.result.HtmlCore import HtmlCore
        core = HtmlCore()
        core.paragraph('Create density distribution or smoothed version of any track, based on a sliding window across the genome.')
        core.divider()
        core.paragraph('The available density/smoothing options will depend on the type of the selected track of interest. For instance, it gives meaning to compute the density along the genome of a point track, but for a function track it instead gives meaning to smooth function values in a sliding window. For segments, it may be meaningful to consider either the count or coverage of segments along the genome.')
        return str(core)
             
    @staticmethod    
    def validateAndReturnErrors(choices):
        if not SmoothedTrackTool._isValidTrack(choices):
            return ''
        
        try:
            winSize = int(choices[3])
        except Exception, e:
            return 'Choose a valid number as the window size. Current: %s' % choices[3]
            
        if winSize % 2 == 0:
            return 'The window size must be an odd number. Current: %i' % winSize
        
        
    #@staticmethod
    #def getToolIllustration():
    #    return None
    #
    #@staticmethod
    #def isDebugMode():
    #    return True
    
    @staticmethod    
    def getOutputFormat(choices=None):
        return 'hbfunction'
    
