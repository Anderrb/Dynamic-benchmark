from quick.util.CommonFunctions import getUniqueWebPath, getRelativeUrlFromWebPath, extractIdFromGalaxyFn
from quick.application.SignatureDevianceLogging import takes,returns
import os

class GeneralGuiTool(object):
    # API methods

    @staticmethod
    def getSubToolClasses():
        return None
    
    @staticmethod
    def isPublic():
        return False

    @staticmethod
    def isRedirectTool():
        return False

    @staticmethod
    def isHistoryTool():
        return True

    @classmethod
    def isBatchTool(cls):
        return cls.isHistoryTool()

    @staticmethod
    def isDynamic():
        return True

    @staticmethod
    def getResetBoxes():
        return []

    @staticmethod
    def getInputBoxOrder():
        return None

    @staticmethod
    def getToolDescription():
        return ''
    
    @staticmethod
    def getToolIllustration():
        return None

    @staticmethod
    def isDebugMode():
        return False
    
    @staticmethod    
    def getOutputFormat(choices=None):
        return 'html'
    
    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        return None
    
    # Convenience methods
    
    @classmethod
    def _getPathAndUrlForFile(cls, galaxyFn, relFn):
        '''
        Gets a disk path and a URL for storing a run-specific file.
        galaxyFn is connected to the resulting history item in Galaxy,
          and is used to determine a unique disk path for this specific run.
        relFn is a relative file name (i.e. only name, not full path) that one
          wants a full disk path for, as well as a URL referring to the file.
        '''
        fullFn = cls._getDiskPathForFiles(galaxyFn) + os.sep + relFn
        url = cls._getBaseUrlForFiles(fullFn)
        return fullFn, url
        
    @staticmethod
    def _getDiskPathForFiles(galaxyFn):
        galaxyId = extractIdFromGalaxyFn(galaxyFn)
        return getUniqueWebPath(galaxyId)
    
    @staticmethod
    def _getBaseUrlForFiles(diskPath):
        return getRelativeUrlFromWebPath(diskPath)
    
    @staticmethod
    def _isValidTrack(prevChoices, tnChoiceIndex=1):
        from quick.application.GalaxyInterface import GalaxyInterface
        from quick.application.ProcTrackOptions import ProcTrackOptions
        
        genome = prevChoices[0]
        tn = prevChoices[tnChoiceIndex].split(':')
        
        return ProcTrackOptions.isValidTrack(genome, tn, True) or \
            GalaxyInterface.isNmerTrackName(genome, tn)
        
    @staticmethod
    def _checkHistoryTrack(prevChoices, historyChoiceIndex, geSourceCls, genome=None, filetype='', validateFirstLine=True):
        fileStr = filetype + ' file' if filetype else 'file'
        
        if type(historyChoiceIndex) == int:
            historyTrackName = prevChoices[historyChoiceIndex]
        else:
            historyTrackName = getattr(prevChoices, historyChoiceIndex)
        
        if historyTrackName is None:
            return 'Please select a ' + fileStr + ' from history.'
        
        if validateFirstLine:
            from quick.application.ExternalTrackManager import ExternalTrackManager
            galaxyTN = historyTrackName.split(':')
            suffix = ExternalTrackManager.extractFileSuffixFromGalaxyTN(galaxyTN)
            fn = ExternalTrackManager.extractFnFromGalaxyTN(galaxyTN)
            
            try:
                geSourceCls(fn , genome, suffix=suffix).parseFirstDataLine()
    
            except Exception, e:
                return fileStr.capitalize() + ' invalid: ' + str(e)

    @staticmethod    
    def _getBasicTrackFormat(choices, tnChoiceIndex=1):
        from quick.application.GalaxyInterface import GalaxyInterface
        from gold.description.TrackInfo import TrackInfo
        
        genome = choices[0]
        tn = choices[tnChoiceIndex].split(':')
        
        if GalaxyInterface.isNmerTrackName(genome, tn):
            tfName = 'Points'
        else:
            tfName = TrackInfo(genome, tn).trackFormatName
        
        tfName = tfName.lower()
        
        if tfName.startswith('linked '):
            tfName = tfName[7:]
            
        tfName = tfName.replace('unmarked ','')
        tfName = tfName.replace('marked','valued')
        
        return genome, tn, tfName
    
    @staticmethod
    def getNamedTuple():
        return None
    