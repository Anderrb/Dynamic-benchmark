import os
import urllib
import urllib2
import tarfile
import zipfile
import gzip
import sys
import shutil
from quick.util.CommonFunctions import ensurePathExists
from quick.util.GenomeInfo import GenomeInfo
from config.Config import NONSTANDARD_DATA_PATH
from quick.aux.StandardizeTrackFiles import SplitFasta
from gold.origdata.PreProcessTracksJob import PreProcessAllTracksJob
from gold.util.CommonFunctions import createOrigPath
from quick.aux.CustomFuncCatalog import createChromosomeFile, createAssemblyGapsFile
from gold.util.CustomExceptions import InvalidFormatError

class GenomeImporter:
    @classmethod
    def extractChromosomesFromGenome(cls, abbrv):
        """Method that reads all the chromosone files for one genome and picks out the Chromosone names
           it uses the constant NONSTANDARD_DATA_PATH and abbrv to find correct path.
           all files within this path is examined for chromosone names and a list of found names is returned from the method
        """
        basePath = cls.getBasePath(abbrv) + os.sep
        resultDict = {'Path':basePath, 'ContentList':[]}
        os.path.walk(basePath,cls.AddFileContentToList,resultDict)
        return resultDict['ContentList']
    
    @classmethod
    def AddFileContentToList(cls, arg, dirname, fnames ):
        
        for file in fnames:
            filePath = os.path.join(dirname, file)
            if os.path.isdir(filePath):
                pass
            else:
                faFile = open(filePath,'r')
                arg['ContentList'] += [fileString[1:].strip().split()[0] for fileString in faFile if fileString[0]=='>']
                faFile.close()
                
                #because of folderstructure dependencies i have to ensure that fasta files lies directly under the sequence folder
                #arg[Path] contains the basePath which is the sequence folder for the genome in action.
                if dirname != arg['Path']:
                    destinationPath = arg['Path']+file
                    shutil.move(filePath, destinationPath)

    
    @classmethod
    def getGenomeAbbrv(cls, fileName):
        return open(fileName, 'r').readline().split('Genome abbreviation: ')[-1].strip()
    
    @classmethod
    def downloadGenomeSequence(cls, abbrv, url):
        basePath = cls.getBasePath(abbrv)
        if os.path.exists(basePath):
            sys.stderr.write("Genome sequence path already exists: %s. Exiting..." % basePath)
            return
            
        
        fn = basePath +"/"
        
        if not url.split('.')[-1].lower() in ['fa','fasta','tar','tgz','gz','zip']:
            urlinfo = str(urllib2.urlopen(url).info())
            if urlinfo.find('filename=') >0:
                fn+= urlinfo.split('filename=')[-1].replace(';','\n').split('\n')[0].strip()
            else:
                sys.stderr.write("Not a supported file format. File must end with: fa fasta tar tgz tar.gz zip gz")
                raise InvalidFormatError
        else:
            fn+=url.split("/")[-1]
        
        ensurePathExists(fn)
        urllib.urlretrieve(url, fn)
        
        if url.lower().endswith(".fa") | url.lower().endswith(".fasta"):
            print "fasta file"
        elif url.lower().endswith(".tar") | url.lower().endswith(".tgz") | url.lower().endswith(".tar.gz"):
            print "tar file"
            te=tarfile.open(fn)
            te.extractall(path=basePath)
            te.close()
            os.remove(fn)
        elif url.lower().endswith(".zip"):
            print "zip file"
            sourceZip = zipfile.ZipFile(fn, 'r')
            sourceZip.extractall(path=basePath)
            sourceZip.close()
            os.remove(fn)
        elif url.lower().endswith(".gz"):
            print "gz file"
            f = gzip.open(fn, 'rb')
            retfn=fn[0:fn.rfind(".")]#Renames file except last part, ".gz"?
            resfile=open(retfn, "wb")
            for i in f:
                resfile.write(i)
            resfile.close()
            os.remove(fn)
        
    @classmethod
    def getBasePath(cls, abbrv):
        return os.sep.join([NONSTANDARD_DATA_PATH, abbrv] + GenomeInfo.getSequenceTrackName(abbrv))
    
    
    @classmethod     
    def createGenome(cls, genome, fullName, chromNamesDict, standardChromosomes, username=''):        
        basePath = cls.getBasePath(genome)
        trackName=GenomeInfo.getSequenceTrackName(genome)
        print("Splitting genome file into chromosomes.")
        SplitFasta.parseFiles(genome, trackName, chromNamesDict=chromNamesDict)
        print("Processing genome")
        PreProcessAllTracksJob(genome).process()
        
        #print "Writing name file.:", fullName  
        #nameFn=createOrigPath(genome,[], "_name.txt" if experimental else "#name.txt")
        #ensurePathExists(nameFn)
        #f=open(nameFn, "w")
        #f.write(fullName)
        #f.close()
        
        print("Creating chromosome file")
        createChromosomeFile(genome, ",".join(standardChromosomes))
        print("Creating assembly gaps file")
        createAssemblyGapsFile(genome)
        print("Processing genome")
        PreProcessAllTracksJob(genome).process()
        print(genome + " genome added")
    
    
"""
print "starter"
import os
os.chdir("/Users/vegard/jobb/hyperbrowser/temp")
# gzipped
GenomeImporter.downloadGenomeSequence("tullegenom", "http://hyperbrowser.uio.no/dev/static/hyperbrowser/div/testgenome/Schizosaccharomyces_pombe.EF1.dna.chromosome.I.fa.gz")
#zipped
#GenomeImporter.downloadGenomeSequence("tullegenom", "http://hyperbrowser.uio.no/dev/static/hyperbrowser/div/testgenome/zippedtest.zip")
#tar.gz
#GenomeImporter.downloadGenomeSequence("tullegenom", "http://hyperbrowser.uio.no/dev/static/hyperbrowser/div/testgenome/testgenome.tar.gz")
#tar
#GenomeImporter.downloadGenomeSequence("tullegenom", "http://hyperbrowser.uio.no/dev/static/hyperbrowser/div/testgenome/testgenometaronly.tar")
#fa
#GenomeImporter.downloadGenomeSequence("tullegenom", "http://hyperbrowser.uio.no/dev/static/hyperbrowser/div/testgenome/testgenomefastaonly.fa")

#http://hyperbrowser.uio.no/dev/static/hyperbrowser/div/testgenome/Homo_sapiens.GRCh37.61.dna.toplevel.fa.gz

print "ferdig"
http://hyperbrowser.uio.no/dev/static/hyperbrowser/div/testgenome/testnyttchrnavn.tgz
ftp://ftp.ensemblgenomes.org/pub/fungi/release-8/fasta/puccinia_graministritici/dna/Puccinia_graministritici.BROAD1.dna.toplevel.fa.gz
ftp://ftp.ensembl.org/pub/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.61.dna.toplevel.fa.gz

"""
