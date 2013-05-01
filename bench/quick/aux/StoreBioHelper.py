from galaxy import eggs
import pkg_resources
pkg_resources.require('pyzmq')
import zmq
messageSep = '##'
from gold.application.LogSetup import logMessage

def getSBFnAndHBTrackAndFn(trackNameTuple):
    subtype = trackNameTuple[2]
    fileName = '/'.join(trackNameTuple[3:]).replace(',FOLDER','').split(',')[0]
    if fileName =='':
        return '',''
    hbFileName = fileName.split('/')[-1]
    hbTrackName = ['Track', subtype] +fileName.split('/')[:-1]+ [hbFileName.split('.')[0]]
    return fileName, hbTrackName, hbFileName

def getUrlToSBFile(trackNameTuple, userName, pwd):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    
    trackNameTuple[-1] = trackNameTuple[-1].split(',')[0]
    datasetId = getDatasetId(trackNameTuple[1])
    subtype = trackNameTuple[2]
    
    fileName, hbTrackName, hbFileName = getSBFnAndHBTrackAndFn(trackNameTuple)
    if fileName == '':
        return '','',''
    subList = [{'Subtype':subtype, 'FileToExtract':fileName}]#
    paramlist = ['username:='+userName,'password:='+pwd, 'operation:=GetFileUrlsFromDataSet','class:=dataStorageService','params:='+'<#>'.join([ repr(datasetId), repr(subList)])]
    socket.send(messageSep.join(paramlist))
    url = socket.recv_unicode().encode('ascii','ignore')
    
    return url, hbFileName, hbTrackName



def getDatasetId(datasetStr):
    return datasetStr.split('(')[-1].split(')')[0].strip()

def getPreviewFile(trackNameTuple, userName, pwd):
    logMessage('trackNameTuple :=  '+ repr(trackNameTuple))
    if trackNameTuple[-1].find(',FOLDER')>0:
        return None
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    
    trackNameTuple[-1] = trackNameTuple[-1].split(',')[0]
    datasetId = getDatasetId(trackNameTuple[1])
    subtype = trackNameTuple[2]
    fileName = '/'.join(trackNameTuple[3:]).replace(',FOLDER','').split(',')[0]
    if fileName =='':
        return None
    subList = [subtype, fileName]
    paramlist = ['params:='+'<#>'.join([ datasetId, repr(subList)]), 'operation:=GetFilePreviewFromPublicDataset','class:=dataStorageServicePub']
    socket.send(messageSep.join(paramlist))
    filePreview = socket.recv_unicode().encode('ascii','ignore')
    #startIndex, endIndex = filePreview.find('<Preview>')+9,  filePreview.rfind('</Preview>')
    #filePreview = filePreview[startIndex:endIndex]
    from tempfile import NamedTemporaryFile
    tempfile = NamedTemporaryFile()
    tempfile.write(filePreview)
    logMessage('fileName :=  '+fileName)
    logMessage('NamedTemporaryFile :=  '+tempfile.name)
    logMessage('FilePreview :=  '+ filePreview)
    return tempfile

#refusjon@norwegian.no