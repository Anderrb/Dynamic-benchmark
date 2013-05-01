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
import zipfile
import cStringIO
import time
#import zmq
#from lxml import etree

#This is a template prototyping GUI that comes together with a corresponding web page.
#

class ListStorebioProjects(GeneralGuiTool):
    
    cachedXml = ''
    nsDat="http://storebioinfo.norstore.no/service/datastorage"
    nsDat1="http://storebioinfo.norstore.no/schema/datastorage"
#    context = zmq.Context()
#    socket = context.socket(zmq.REQ)
#    socket.connect("tcp://localhost:5559")
    
    @staticmethod
    def getToolName():
        return "StoreBioInfo Integration Tools"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Username at StoreBioinfo','Password at StoreBioinfo', 'Select Operation', 'hidden', 'Select Dataset', 'Select SubType' , 'Select File', 'File Preview' ]#'hidden','Select files from zip archive'

    
    
    
    
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
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')
        '''
        return ['List Projects', 'List Datasets', 'Upload file from Dataset']
    
    
    @staticmethod    
    def getOptionsBox4(prevChoices):
        
        if prevChoices[2] == 'Upload file from Dataset':
            
            if prevChoices[3] not in [None, '']:
                return ('__hidden__', prevChoices[3])
            else:
                userName = prevChoices[0] if prevChoices[0] else ''
                pwd = prevChoices[1] if prevChoices[1] else ''
                operation = 'List Datasets'
                ListStorebioProjects.socket.send('##'.join(['username:='+userName,'password:='+pwd, 'operation:='+operation,'class:=dataStorageService']))
                #message = StoreBioTestTool.socket.recv_unicode().encode('ascii','ignore')
                #dataStorageService = WsDataStorageService(prevChoices[0], prevChoices[1])
                #return [type()]
                return ('__hidden__',  quote(ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore')))#.decode("ascii",'ignore').encode("ascii")))#.encode("ascii",'ignore')
        
    @staticmethod    
    def getOptionsBox5(prevChoices):
        '''Returns a list of options to be displayed in the first options box
        Alternatively, the following have special meaning:
        '__genome__'
        '__track__'
        ('__history__','bed','wig','...')'''
        #position 41106
        NS = ListStorebioProjects.nsDat1
        if prevChoices[2] == 'Upload file from Dataset':
            datasetList = ['--select--']
            xmlDoc =  minidom.parseString(unquote(prevChoices[3]))#.decode('ascii', 'ignore'))
            #xmlDoc = etree.fromstring(unquote(prevChoices[3]))
            #return [dataSet.findtext(NS+'Name') for dataSet in xmlDoc.iter(NS+'DataSet')]
        
            userName = prevChoices[0] if prevChoices[0] else ''
            pwd = prevChoices[1] if prevChoices[1] else ''
            operation = 'getSubTrackName'
            params = 'params:='+repr(['StoreBioInfo'])
            
            ListStorebioProjects.socket.send('##'.join(['username:='+userName,'password:='+pwd, params, 'operation:='+operation,'class:=dataStorageService']))
            responseList = eval(ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore'))
            return ['--select--']+[v[0] for v in responseList]
            
            #for dataset in xmlDoc.getElementsByTagName('DataSet'):
            #    datasetList.append(DomUtility.getNodeValue(dataset, 'Name', 'str')+',, ('+DomUtility.getNodeValue(dataset, 'Id', 'str')+')')
            #return datasetList 
        
    
    
    @staticmethod    
    def getOptionsBox6(prevChoices):
    
        if prevChoices[4] != None and prevChoices[2] == 'Upload file from Dataset' and prevChoices[-2]!='--select--':
            #NS = ListStorebioProjects.nsDat1
        
            userName = prevChoices[0] if prevChoices[0] else ''
            pwd = prevChoices[1] if prevChoices[1] else ''
            operation = 'getSubTrackName'
            params = 'params:='+repr(['StoreBioInfo', prevChoices[-2]])
            
            ListStorebioProjects.socket.send('##'.join(['username:='+userName,'password:='+pwd, params, 'operation:='+operation,'class:=dataStorageService']))
            responseList = eval(ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore'))
            return ['--select--']+[v[0] for v in responseList]
        
    @staticmethod    
    def getOptionsBox7(prevChoices):
    
        if prevChoices[4] != None and prevChoices[2] == 'Upload file from Dataset' and prevChoices[-2] and prevChoices[-2]!='--select--' :
            #NS = ListStorebioProjects.nsDat1
            
            userName = prevChoices[0] if prevChoices[0] else ''
            pwd = prevChoices[1] if prevChoices[1] else ''
            operation = 'getSubTrackName'
            params = 'params:='+repr(['StoreBioInfo', prevChoices[4], prevChoices[5]])
            
            ListStorebioProjects.socket.send('##'.join(['username:='+userName,'password:='+pwd, params, 'operation:='+operation,'class:=dataStorageService']))
            return ['--select--']+[v[0] for v in eval( ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore') )]
    
#    @staticmethod    
#    def getOptionsBox8(prevChoices):
#    
#        if prevChoices[4] != None and prevChoices[2] == 'Upload file from Dataset' and prevChoices[-2]:
#        #NS = ListStorebioProjects.nsDat1
#        return ['--select--']+[v[0] for v in eval(prevChoices[-2])]
#    
    @staticmethod    
    def getOptionsBox8(prevChoices):
    
        if prevChoices[4] != None and prevChoices[2] == 'Upload file from Dataset' and prevChoices[-2] and prevChoices[-2]!='--select--':
            userName = prevChoices[0] if prevChoices[0] else ''
            pwd = prevChoices[1] if prevChoices[1] else ''
            operation = 'GetFilePreview'
            params = 'params:='+'<#>'.join([prevChoices[4].split('(')[-1][:-1], repr([prevChoices[5], prevChoices[6].split(',')[0]]) ])
            ListStorebioProjects.socket.send('##'.join(['username:='+userName,'password:='+pwd, params, 'operation:='+operation,'class:=dataStorageService']))
            tmpResult = ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore')
            if tmpResult.find('<Preview>')>0:
                res = tmpResult.split('<Preview>')[1].split('</Preview>')[0]
                return (res, len(res.split('\n')), True)
        
#        
#    @staticmethod    
#    def getOptionsBox6(prevChoices):
#    def getSubTrackName(self, liste):
#        if prevChoices[4] != None and prevChoices[2] == 'Upload file from Dataset' and prevChoices[-2]!='--select--':
#        #NS = ListStorebioProjects.nsDat1
#            fileList = []
#            xmlDoc =  minidom.parseString(unquote(prevChoices[3]).decode('ascii', 'ignore'))#unquote()
#            #xmlDoc = etree.fromstring(unquote(prevChoices[3]))
#            #for dataSet in xmlDoc.iter(NS+'DataSet'):
#            #    if dataSet.findtext(NS+'Name') == prevChoices[4]:
#            #        return [x.text for x in dataSet.iter(NS+'SubEntries')]
#            for dataset in xmlDoc.getElementsByTagName('DataSet'):
#        fileList.append('heisann')
#                if DomUtility.getNodeValue(dataset, 'Name', 'str') == prevChoices[4].split(',, (')[0]:
#                    fileList = ['--select--']+[x.childNodes[0].nodeValue for x in dataset.getElementsByTagName('SubEntries')]#LocalResourceURL
#            return fileList if len(fileList)>1 else None
#        else:
#        
#        return None
    
    
    
    
    
#    @staticmethod    
#    def getOptionsBox7(prevChoices):
#        if prevChoices[-2] != None and prevChoices[2] == 'Upload file from Dataset'and prevChoices[-2]!='--select--':
#            
#            datasetId = prevChoices[4].split('(')[-1][:-1]
#            subList = [{'Subtype':prevChoices[5].split('/')[0], 'FileToExtract':'/'.join(prevChoices[5].split('/')[1:]).split(',')[0]}]
#            paramlist = ['username:='+prevChoices[0],'password:='+prevChoices[1], 'operation:=GetFileUrlsFromDataSet','class:=dataStorageService',\
#             'params:='+'<#>'.join([ repr(datasetId), repr(subList)])]
#        ListStorebioProjects.socket.send(messageSep.join(paramlist))
#            url = ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore')
#            #dataStorageService = WsDataStorageService(prevChoices[0], prevChoices[1])
#            #url = dataStorageService.GetFileUrlsFromDataSet(datasetId, subList)[0]
#            return ('__hidden__',  quote(url))
#            
#            
#    
#    @staticmethod    
#    def getOptionsBox8(prevChoices):
#        if prevChoices[-2] != None and prevChoices[2] == 'Upload file from Dataset'and prevChoices[-3]!='--select--':
#            #return unquote(prevChoices[-2])
#            url = unquote(prevChoices[-2])
#            fileType = url.split('.')[-1] .strip()
#            if fileType == 'zip':
#                remotezip = urllib2.urlopen(url)
#                zipinmemory = cStringIO.StringIO(remotezip.read())
#                zip = zipfile.ZipFile(zipinmemory)
#                return {v:False for v in zip.namelist()}
            
    
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
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history. If getOutputFormat is anything else than HTML, the output should be written to the file with path galaxyFn.gtr
        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).
        choices is a list of selections made by web-user in each options box.
        '''
        
        start = time.time()
        outputFile=open(galaxyFn,"w")
        params = ['username:='+choices[0],'password:='+choices[1], 'operation:='+choices[2]]

        if choices[2] == 'List Projects':
            params += ['class:=userMngtService']
            ListStorebioProjects.socket.send(messageSep.join(params))
            message = ListStorebioProjects.socket.recv_unicode().encode('utf-8')#, 'ignore'
            if message == 'something went wrong...':
                return None
            else:
                print>>outputFile, ListStorebioProjects.ParseProjectListXmlDoc(minidom.parseString(message))
            #print>>outputFile, message
            
            #userMngtService = WsUserMgntService(choices[0], choices[1])
            #print>>outputFile, 'after userMngtService = WsUserMgntService(c....:  ', time.time()-start
            #print>>outputFile, userMngtService.ListProjects()
            #print>>outputFile, 'after userMngtService.ListProjects():   ', time.time()-start
        elif choices[2] == 'Upload file from Dataset':
            outputFile=open(galaxyFn,"w")
            
            datasetId = choices[4].split('(')[-1].split(')')[0].strip()
            subList = [{'Subtype': choices[5], 'FileToExtract': choices[6].split(',')[0].strip()}]#
            paramlist = ['username:='+choices[0],'password:='+choices[1], 'operation:=GetFileUrlsFromDataSet','class:=dataStorageService',\
                'params:='+'<#>'.join([ repr(datasetId), repr(subList)])]
            ListStorebioProjects.socket.send(messageSep.join(paramlist))
            url = ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore')
                
            #url = unquote(choices[6])
            #List = dataStorageService.GetFileUrlsFromDataSet(datasetId, subList)
            
            fileType = url.split('.')[-1].strip()
                
            if fileType == 'zip':
                validFiles = [k for k,v in choices[7].items() if v]
                
                remotezip = urllib2.urlopen(url)
                zipinmemory = cStringIO.StringIO(remotezip.read())
                zip = zipfile.ZipFile(zipinmemory)
                
                for fn in zip.namelist():
                    if fn in validFiles:
                        print>>outputFile, zip.read(fn)
                        print>>outputFile, "\n\n\n\n\n\n\n"
            else:
                print>>outputFile, urllib2.urlopen(url).read()
                    
                
            
        else:
            params += ['class:=dataStorageService']
            ListStorebioProjects.socket.send(messageSep.join(params))
            message = ListStorebioProjects.socket.recv_unicode().encode('ascii','ignore')
            print>>outputFile, ListStorebioProjects.ParseDatasetsXmlDoc(minidom.parseString(message))
            #dataStorageService = WsDataStorageService(choices[0], choices[1])
            #print>>outputFile, 'after dataStorageService = WsDataStorageService(....:  ', time.time()-start
            #dataStorageService.ListDataSetTypes()
            #xmlDoc = dataStorageService.ListDataSetsForUser(choices[0]).encode('ascii','ignore')
            #print xmlDoc
            #print>>outputFile, 'after dataStorageService.ListDataSetsForUser(choices[0]):  ', time.time()-start
            #print>>outputFile, 'after ListStorebioProjects.ParseDatasetsXmlDoc(xmlDoc):  ', time.time()-start
        outputFile.close()
    
    
    @staticmethod
    def ParseProjectListXmlDoc(xmlDoc):  
        ProjectsList = []
        wsXmlParser = ParseXml()
        for project in  xmlDoc.getElementsByTagName('Project'):
            
            ProjectsList.append(wsXmlParser.ParseProjectXml(project))
        
        
        tableList = []
        for project in ProjectsList:
            tablestr = '<table>'
            keys = ['Name','Description','Creater','Created','Quota','DiskUsage']
            for key in keys:
                if key in project:
                    if key == 'Quota':
                        tablestr+= '<tr><td>%s: </td><td> </td><td>%s</td></tr>' % (key, project[key][key])
                    else:
                        tablestr+= '<tr><td>%s: </td><td> </td><td>%s</td></tr>' % (key, project[key])
            tablestr += '</table>'
            if 'ProjectMembers' in project:
                tablestr+= '<table><tr><td>ProjectMembers: </td><td> </td><td>Username </td><td>Roles </td><td> </td></tr>'
                for member in project['ProjectMembers']:
                    tablestr+= '<tr><td> </td><td> </td><td>'+member['Username']+'</td><td>'+member['Roles']+'</td><td> </td></tr>'
                tablestr += '</table>'
            tablestr += '<br/><br/>'
            tableList.append(tablestr)
        
        return '\n'.join(tableList)
    
    @staticmethod
    def ParseDatasetsXmlDoc(xmlDoc):
        core = HtmlCore()
        core.tableHeader(['Dataset Name', 'Description', 'Created', 'Owner', 'Size', 'Qty files in Dataset', 'State'], sortable=True)
        for dataset in xmlDoc.getElementsByTagName('DataSet'):
            datasetName =  DomUtility.getNodeValue(dataset, 'Name', 'str')
            owner = DomUtility.getNodeValue(dataset, 'Owner', 'str')
            dateCreated = DomUtility.getNodeValue(dataset, 'Created', 'date')
            size = sum([int(size.childNodes[0].nodeValue)  for size in dataset.getElementsByTagName('Size')])
            description = DomUtility.getNodeValue(dataset, 'Description', 'str')
            numOfFilesInDataset = len(dataset.getElementsByTagName('Resource'))
            state = DomUtility.getNodeValue(dataset, 'State', 'str')
            core.tableLine([datasetName, description, dateCreated, owner, str(size), str(numOfFilesInDataset), state])
        
        return str(core)
            



    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        return
        if len(choices[1])>0:
            try:
                userMngtService = WsUserMgntService(choices[0], choices[1])
                return None
            except:
                return 'Invalid Username/Password combination!!'
        else:
            return ''
    
    @staticmethod
    def isPublic():
        return False
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
    
    @staticmethod    
    def getOutputFormat(choices=None):
        '''The format of the history element with the output of the tool.
        Note that html output shows print statements, but that text-based output
        (e.g. bed) only shows text written to the galaxyFn file.
        '''
        if choices[2] in ['List Projects', 'List Datasets']:
            return 'html'
        returnType = 'txt'
        #if choices[7]:
        #    itemTab = [k for k,v in choices[7].items() if v]
        #    if itemTab:
        #        returnType = getFileSuffix(itemTab[0])
        return returnType
    
