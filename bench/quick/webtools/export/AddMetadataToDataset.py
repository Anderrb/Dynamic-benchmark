#from galaxy import eggs
#import pkg_resources
#pkg_resources.require('pyzmq')

from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.aux.WsStoreBioInfo import *
from xml.dom import minidom
from gold.result.HtmlCore import HtmlCore
from urllib import quote, unquote
from gold.util.CustomExceptions import InvalidFormatError
from gold.util.CommonFunctions import getFileSuffix
import time
#import zmq
#This is a template prototyping GUI that comes together with a corresponding web page.
#

class AddMetadataToDataset(GeneralGuiTool):
    
    #context = zmq.Context()
    #socket = context.socket(zmq.REQ)
    #socket.connect("tcp://localhost:5559")
    
    @staticmethod
    def getToolName():
        return "Add metadata to dataset"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        #can have two syntaxes: either a list of stings or a list of tuples where each tuple has two items(Name of box on webPage, name of getOptionsBox)
        return ['Username','Password', 'hidden','Select Dataset', 'Write Meta key', 'Write Meat value', 'Write Meta key', 'Write Meat value', 'Write Meta key', 'Write Meat value', 'Write Meta key', 'Write Meat value', 'Write Meta key', 'Write Meat value']
    
    @staticmethod    
    def getOptionsBox1():
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return ''
    
    @staticmethod    
    def getOptionsBox2(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        return  '__password__'
    
      
    @staticmethod    
    def getOptionsBox3(prevChoices):
        respons = prevChoices[-1]
        if prevChoices[0] and prevChoices[1] and  len(prevChoices[-1])>0:
            userName = prevChoices[0] if prevChoices[0] else ''
            pwd = prevChoices[1] if prevChoices[1] else ''
            operation = 'getSubTrackName'
            params = 'params:='+repr(['StoreBioInfo'])
                
            AddMetadataToDataset.socket.send('##'.join(['username:='+userName,'password:='+pwd, params, 'operation:='+operation,'class:=dataStorageService']))
            responseList = eval(AddMetadataToDataset.socket.recv_unicode().encode('ascii','ignore'))
            return ('__hidden__', repr([v[0] for v in responseList]))
        
        return ('__hidden__', respons)
        
    @staticmethod    
    def getOptionsBox4(prevChoices):
        if prevChoices[-2]:
            return eval(prevChoices[-2])
            
    
    
    
    
    @staticmethod    
    def getOptionsBox5(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    @staticmethod    
    def getOptionsBox6(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    @staticmethod    
    def getOptionsBox7(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    @staticmethod    
    def getOptionsBox8(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    @staticmethod    
    def getOptionsBox9(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    @staticmethod    
    def getOptionsBox10(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    @staticmethod    
    def getOptionsBox11(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    
    @staticmethod    
    def getOptionsBox12(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    
    @staticmethod    
    def getOptionsBox13(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        if prevChoices[-2]:
            return ''
    
    @staticmethod    
    def getOptionsBox14(prevChoices):
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        if prevChoices[-2]:
            return ''
        
        
    #@staticmethod    
    #def getOptionsBox3(prevChoices):
    #    return ['']

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
        
        params = ['username:='+choices[0],'password:='+choices[1], 'operation:=AddMetaDataToDataSet', 'class:=dataStorageService']
        result = []
        key = None
        for index, value in enumerate(choices[4:]):
            if index % 2 == 0:
                if value:
                    key = value
                else:
                    break
            else:
                result.append([key, value])
        print choices[3]
        datasetId = choices[3].split('(')[-1].split(')')[0]
        params.append( 'params:='+'<#>'.join([datasetId, repr(result)] ) )
        AddMetadataToDataset.socket.send('##'.join(params))
        print 'Metadata added to dataset ', choices[3]
       

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
