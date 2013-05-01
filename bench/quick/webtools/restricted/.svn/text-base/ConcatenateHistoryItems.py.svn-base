from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.application.ExternalTrackManager import ExternalTrackManager
from quick.util.StaticFile import GalaxyRunSpecificFile
from cPickle import load
import os


class ConcatenateHistoryItems(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Concatenate results of multiple history items"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        #can have two syntaxes: either a list of stings or a list of tuples where each tuple has two items(Name of box on webPage, name of getOptionsBox)
        return ['Select Histories','ResDictKey', 'Local or Global']

    @staticmethod    
    def getOptionsBox1():
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return '__multihistory__',
    
        
    @classmethod    
    def getOptionsBox2(cls, prevChoices):
        
        rsl = cls._getResultsLists(prevChoices[0])[0]
        #return rsl
        return cls._getResDictAndLocalKeys(rsl)[0]
        

    @staticmethod    
    def getOptionsBox3(prevChoices):
        return ['Local results', 'Global results']

    #@staticmethod
    #def getDemoSelections():
    #    return ['testChoice1','..']
        
    @classmethod    
    def execute(cls, choices, galaxyFn=None, username=''):
        '''Is called when execute-button is pushed by web-user.
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history.
        If getOutputFormat is anything else than HTML, the output should be written to the file with path galaxyFn.
        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).
        choices is a list of selections made by web-user in each options box.
        '''
        
        #print 'Executing...'
        
        histChoices = choices[0]
        chosenResDictKey = choices[1] #this box needs to find relevant resDictKeys probably.. or could be a simple string input..
        if choices[2] == 'Global results':
            useGlobal = True
        elif choices[2] == 'Local results':
            useGlobal = False
        else:
            raise
        print 'TEMP1'
        resultsLists, historyNames = cls._getResultsLists(histChoices)
        print 'TEMP2'
        resDictKeys, localKeys  = cls._getResDictAndLocalKeys(resultsLists)
        print 'TEMP3'
        #print resultsLists
        from collections import defaultdict
        matrix = defaultdict(dict)
        for i,resultList in enumerate(resultsLists):
            print 'Num results in history element: ', len(resultList)
            for j,oneResult in enumerate(resultList):
                print 'TEMP4'
                assert oneResult.getResDictKeys() == resDictKeys
                #print oneResult.keys(), localKeys
                #assert oneResult.keys() == localKeys
                colName = historyNames[i] + '-'+str(j)# if j>0 else ''
                if useGlobal:
                    matrix['Global result'][colName] = oneResult.getGlobalResult()[chosenResDictKey]
                else:
                    for localKey in oneResult:
                        matrix[localKey][colName] = oneResult[localKey][chosenResDictKey]
                
        seedRegion = matrix.items()[0]
        sortedColNames = sorted(seedRegion[1].keys())
        for regEntry, matVal in matrix.items():
            assert sorted(matVal.keys()) == sortedColNames, 'Incompatible resultKeys, found both %s and %s, for region entries %s and %s.' % (seedRegion[1].keys(), matVal.keys(), seedRegion[0], regEntry )
            
        print '\t'.join([' ']+sortedColNames)
        #print 'matrix: ', matrix
        for localKey in matrix:
            #print matrix[localKey].keys()
            print '\t'.join([str(localKey)]+[str(matrix[localKey].get(historyName)) for historyName in sortedColNames])
            #print '\t'.join([str(localKey)]+[str(matrix[localKey][historyName]) for historyName in matrix[localKey]])
                
    @staticmethod
    def _getResultsLists(histChoices):
        if len([x for x in histChoices.values() if x!=None])==0:
            return [],[]
        #print 'histChoices',histChoices
        #return []

        galaxyTNs = [x.split(':') for x in histChoices.values() if x!=None]
                
        galaxyFns = [ExternalTrackManager.extractFnFromGalaxyTN(tn) for tn in galaxyTNs]
        historyNames= [ExternalTrackManager.extractNameFromHistoryTN(tn) for tn in galaxyTNs]
        staticFiles = [GalaxyRunSpecificFile(['results.pickle'], gfn) for gfn in galaxyFns]
        fileSpecificFile = [GalaxyRunSpecificFile([], gfn) for gfn in galaxyFns]
        print 'Using pickles: ', [x.getDiskPath() for x in staticFiles]
        
        paths = [x.getDiskPath()+'/0' for x in fileSpecificFile]
        pngList = [[v for v in x[2] if v.find('.png')>0] for x in os.walk(paths[0])]
        
        resultsLists = [load(sf.getFile('r')) for sf in staticFiles]
        return resultsLists, historyNames
    
    @staticmethod
    def _getResDictAndLocalKeys(resultsLists):
        if len(resultsLists)==0:
            return [], []
            
        firstResultsObject = resultsLists[0][0]
        resDictKeys = firstResultsObject.getResDictKeys()
        localKeys = firstResultsObject.keys()
        return resDictKeys, localKeys

    @classmethod
    def validateAndReturnErrors(cls, choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        if len(cls._getResultsLists(choices[0])[0]) == 0:
            return 'At least one history element must be selected!'
        
        if choices[1] in [None,'']:
            return 'A ResDictKey must be selected!'
        
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
    @staticmethod
    def getResetBoxes():
        return [1]
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
