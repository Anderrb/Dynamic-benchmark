from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.application.ExternalTrackManager import ExternalTrackManager
import math
#This is a template prototyping GUI that comes together with a corresponding web page.
#
from urllib import unquote
class CreateCategoricalTrackTool(GeneralGuiTool):
    
    hiddenOrderList = []
    
    @staticmethod
    def getToolName():
        return "Create categorical BED file"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Select history items:', 'hidden'] + ['Select history item:', 'Type in category:'] * 10
    
    @staticmethod
    def _returnColumnValue(prevChoices, index):
        
        #if isinstance(prevChoices[0], dict):
        #    return None
        
        valueList = CreateCategoricalTrackTool.hiddenOrderList #[str(k) for k,v in prevChoices[0].items() if v]#.split(':')[-1]
        paramNum = int(math.floor((index - 2) / 2))
        if len(valueList) > paramNum:
            if index % 2 == 1:
                return ''
            else:
                return (valueList[paramNum], 1, True)
        else:
            return None
    
    
    
    @staticmethod    
    def getOptionsBox1():
        return ('__multihistory__','bed','wig')
    
    
    @staticmethod    
    def getOptionsBox2(prevChoices):
        CreateCategoricalTrackTool.hiddenOrderList =[]
        if prevChoices[-1]:
            prevList = eval(prevChoices[-1])
            selectedHists = [unquote(val.split(':')[-1]) for key,val in prevChoices[0].items() if val]
            
            CreateCategoricalTrackTool.hiddenOrderList = [unquote(v) for v in prevList if v in selectedHists]
            newlySelected = list(set(selectedHists)-set(CreateCategoricalTrackTool.hiddenOrderList))
            CreateCategoricalTrackTool.hiddenOrderList+= newlySelected
            
            
        return ('__hidden__', repr(CreateCategoricalTrackTool.hiddenOrderList))
    
    @staticmethod    
    def getOptionsBox3(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 2)
    
    @staticmethod    
    def getOptionsBox4(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 3)
    
    @staticmethod    
    def getOptionsBox5(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 4)
    
    @staticmethod    
    def getOptionsBox6(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 5)
    
    @staticmethod    
    def getOptionsBox7(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 6)
    
    @staticmethod    
    def getOptionsBox8(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 7)
    
    @staticmethod    
    def getOptionsBox9(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 8)
    
    @staticmethod    
    def getOptionsBox10(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 9)
    
    @staticmethod    
    def getOptionsBox11(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 10)
    
    @staticmethod    
    def getOptionsBox12(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 11)
    
    @staticmethod    
    def getOptionsBox13(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 12)
    
    @staticmethod    
    def getOptionsBox14(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 13)
    
    @staticmethod    
    def getOptionsBox15(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 14)
    
    @staticmethod    
    def getOptionsBox16(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 15)
    
    @staticmethod    
    def getOptionsBox17(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 16)
    
    @staticmethod    
    def getOptionsBox18(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 17)
    
    @staticmethod    
    def getOptionsBox19(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 18)
    
    @staticmethod    
    def getOptionsBox20(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 19)
    
    @staticmethod    
    def getOptionsBox21(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 20)
    
    @staticmethod    
    def getOptionsBox22(prevChoices): 
        return CreateCategoricalTrackTool._returnColumnValue(prevChoices, 21)
    
        
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        outputFile=open(galaxyFn,"w")
        galaxyTnList = [v.split(':') for v in choices[0].values() if v]
        
        for ind, galaxyTn in enumerate(galaxyTnList):
            
            index = None
            for i in range(2,22,2):
                if choices[i] == unquote(galaxyTn[-1]):
                    index = i+1
                    break
                
            fnSource = ExternalTrackManager.extractFnFromGalaxyTN(galaxyTn)
            for i in open(fnSource,'r'):
                linetab = i.strip().split('\t')
                linetab.insert(3, choices[index])
                if len(linetab)>4:
                    linetab.pop(4)
                print>>outputFile, '\t'.join(linetab)
        
        outputFile.close()        

    @staticmethod
    def validateAndReturnErrors(choices):
        if not choices[0] or not any(choices[0].values()):
                return ''
        
        catList = []
        for ind, value in enumerate(CreateCategoricalTrackTool.hiddenOrderList):
            index = ind*2 +3
            if choices[index] =='':
                return 'All categories must be specified.'
            else:
                if any([x in choices[index] for x in [' ','\t']]):
                    return 'Whitespace is not allowed in categories: ' + choices[index]
                if choices[index] in catList:
                    return 'Category %s is duplicated.' % choices[index]
                catList.append(choices[index])
        return None
    
    @staticmethod
    def isPublic():
        return True
    
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
    @staticmethod    
    def getOutputFormat(inputFormat):
        return 'category.bed'
