# Copyright (C) 2009, Geir Kjetil Sandve, Sveinung Gundersen and Morten Johansen
# This file is part of The Genomic HyperBrowser.
#
#    The Genomic HyperBrowser is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    The Genomic HyperBrowser is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with The Genomic HyperBrowser.  If not, see <http://www.gnu.org/licenses/>.
import re
from quick.util.StaticFile import GalaxyRunSpecificFile
from numpy import *

'''
Handles the conversion of different file formats to GTrack.
'''
class GTrackConverter():
    
    def __init__(self):
        self._weederPattern = re.compile(r'\s*(\d+)\s[+]\s+\[?([ACGT]+)\]?\s+(\d+)\s+[(](\d*\.\d+|\d+\.)[)]')
        self._memePattern = re.compile(r'(.*)\s+[+-]?\s+(\d+)\s+(\d*\.\d+e-\d+)\s+[ACGT]+\s+([ACGT]+)')
        self._glimmerPattern = re.compile(r'orf\d+\s+(\d+)\s+(\d+)\s+[-+]\d+\s+(\d*\.\d+|\d+\.)')
        
        self._prodigalSeqPattern = re.compile(r'.*seqhdr="(.*)";ver.*')
        self._prodigalPredPattern = re.compile(r'\s+CDS\s+.*?(\d+)\.\.<?>?(\d+).*')
        self._prodigalScorePattern = re.compile(r'.*;score=(\d*\.\d+|\d+\.)')
    
    '''
    Converts a weeder file to GTrack
    
    PARAMETERS
    
    infile:  file object for the weeder file
    outfile: file object for the GTrack file
    '''
    def _convertFromWeederToGTrack(self, infile, outfile):
        
        outfile.write('#\n# GTrack\n##Track type: valued segments\n###seqid\tstart\tend\tvalue\tstrand')
        sequenceMap = {}
        
        # Search the weeder file till you find the sequence names
        for line in infile:
            if line == 'Your sequences:\n':
                break
        
        # Retrieve the weeder identifier for each sequence, and map it to the original sequence name
        for line in infile:
            if line.startswith("Sequence"):
                content = line.split()
                sequenceMap[int(content[1])] = content[3]
            # Until there are no more sequences, just break
            elif line.startswith("**** MY ADVICE ****"):
                break
        
        # For each line in the weeder file...
        for line in infile:
            match = re.search(self._weederPattern, line)
            
            # If prediction is found, retrieve the name from the sequence map, 
            # retrieve rest of the information and write the prediction to the GTrack file
            if match:
                data = sequenceMap[int(match.group(1))]
                data = data.split(':')
                regions = data[1].split('-')
                length = len(match.group(2))
                start = int(match.group(3))+int(regions[0])
                stop = start+length
                outfile.write("\n%s\t%d\t%d\t%.2f\t%s" % (data[0][1:], start, stop, float(match.group(4)), '+'))
        
        outfile.close()
    
    '''
    Converts a MEME file to GTrack
    
    PARAMETERS
    
    infile:  file object for the MEME
    outfile: file object for the GTrack file
    '''
    def _convertFromMemeToGTrack(self, infile, outfile):
        
        outfile.write('#\n# GTrack\n#\n##track type: valued segments\n###seqid\tstart\tend\tvalue\tstrand')
        
        # For every line in the MEME file
        for line in infile:
            match = re.search(self._memePattern, line)
        
            if match:
                # If prediction is found, extract start, stop and chromosome, and save to GTrack file
                data = match.group(1).split('-')
                data = data[0].split(':')
                score = 0.000001/float(match.group(3))
                length = len(match.group(4))
                start = int(match.group(2))+int(data[1])
                stop = start+length
                
                outfile.write("\n%s\t%d\t%d\t%f\t+" % (data[0], start, stop, score))
                
        return outfile

    '''
    Converts a Glimmer file to GTrack
    
    PARAMETERS
    
    infile:  file object for the Glimmer file
    outfile: file object for the GTrack file
    '''
    def _convertFromGlimmerToGTrack(self, infile, outfile):
        
        outfile.write('#\n# GTrack\n#\n##Track type: valued segments\n###seqid\tstart\tend\tvalue\tstrand')
        
        chromosome = ''
        seqstart = 0
        
        # For every line the glimmer file...
        for line in infile:
            match = re.search(self._glimmerPattern, line)
            
            # If prediction is found, find start and end values and write to file.
            if match and not chromosome == '':
                start = int(match.group(1))+seqstart
                end = int(match.group(2))+seqstart
                
                if start < end:
                    outfile.write("\n%s\t%d\t%d\t%.2f\t%s" % (chromosome, start, end, float(match.group(3)), '+'))
                else:
                    outfile.write("\n%s\t%d\t%d\t%.2f\t%s" % (chromosome, end, start, float(match.group(3)), '-'))
                    
            else:
                # Else, we have a new sequence, and update chromosome and sequence start
                data = line.split('-')
                data = data[0].split(':')
                chromosome = data[0][1:]
                seqstart = int(data[1])
        
        outfile.close()      
    
    '''
    Converts a prodigal file to GTrack
    
    PARAMETERS
    
    infile:  file object for the Prodigal file
    outfile: file object for the GTrack file
    '''
    def _convertFromProdigalToGTrack(self, infile, outfile):
        
        outfile.write('#\n# GTrack\n#\n##Track type: valued segments\n###seqid\tstart\tend\tvalue')
        
        chromosome = ''
        seqstart = 0
        start = 0
        end = 0
        
        # For every line in the prodigal file
        for line in infile:
            seqMatch = re.search(self._prodigalSeqPattern, line)
            predMatch = re.search(self._prodigalPredPattern, line)
            scoreMatch = re.search(self._prodigalScorePattern, line)
            
            if seqMatch:
                # If sequence match, set new chromosome and sequence start
                data = seqMatch.group(1).split('-')
                data = data[0].split(':')
                chromosome = data[0]
                seqstart = int(data[1])
            elif predMatch:
                # If prediction match, update the start and end values
                start = int(predMatch.group(1))+seqstart
                end = int(predMatch.group(2))+seqstart
            elif scoreMatch:
                # If score, write the entire prediction to the GTrack file
                outfile.write("\n%s\t%d\t%d\t%.2f" % (chromosome, start, end, float(scoreMatch.group(1))))
        
        outfile.close()
    
    '''
    Converts a Genemark file to GTrack
    
    PARAMETERS
    
    infile:  file object for the Genemark file
    outfile: file object for the GTrack file
    '''
    def _convertFromGenemarkToGTrack(self, infile, outfile):
        
        outfile.write('#\n# GTrack\n#\n##track type: segments\n###seqid\tstart\tend\tstrand')
        
        # Define prediction and sequence patterns
        seqPattern = r'FASTA definition line:\s(.+)'
        seqPattern = re.compile(seqPattern)
        predPattern = r'\s+\d+\s+([+-])\s+<?>?(\d+)\s+<?>?(\d+).+'
        predPattern = re.compile(predPattern)
        
        chromosome = ''
        seqstart = 0
        
        # For every line in the Genemark file...
        for line in infile:
            seqMatch = re.search(seqPattern, line)
            predMatch = re.search(predPattern, line)
        
            if seqMatch:
                # If sequence match, set new chromosome and sequence start
                data = seqMatch.group(1).split('-')
                data = data[0].split(':')
                chromosome = data[0]
                seqstart = int(data[1])
            elif predMatch:
                # If prediction match, write the new prediction to the GTrack file
                strand = predMatch.group(1)
                start = int(predMatch.group(2))+seqstart
                end = int(predMatch.group(3))+seqstart
                outfile.write("\n%s\t%d\t%d\t%s" % (chromosome, start, end, strand))
        
        outfile.close()
       
    '''
    Converts a Blast file to GTrack
    
    PARAMETERS
    
    infile:  file object for the Blast file
    outfile: file object for the GTrack file
    ''' 
    def _convertFromBlastToGTrack(self, infile, outfile):
        
        outfile.write('#\n# GTrack\n###seqid\tstart\tend\tstrand')
        
        querypattern = r'# Query: (.*)\n'
        querypattern = re.compile(querypattern)
        seqpattern = r'(.*)\s+gi\|\d+\|ref\|NC_0000(\d+)\.\d+\|\s+\d*\.\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)\s+(\d+).+'
        seqpattern = re.compile(seqpattern)

        gene = ''

        for line in infile:
            querymatch = re.search(querypattern, line)
            seqmatch = re.search(seqpattern, line)

            if querymatch:
                gene =  querymatch.group(1)
            elif seqmatch:
                if seqmatch.group(1) == gene:
                    start = int(seqmatch.group(3))
                    end = int(seqmatch.group(4))
                    chromosome = seqmatch.group(2)
      
                    if chromosome[0] == '0':
                        chromosome = chromosome[1:]

                    if start < end:
                        outfile.write('\nchr%s\t%d\t%d\t+' % (chromosome, start, end))
                    else:
                        outfile.write('\nchr%s\t%d\t%d\t-' % (chromosome, end, start))

                    gene = ''

        outfile.close()
    
    '''
    Converts a YMF file to GTrack
    
    PARAMETERS
    
    infile:    file object for the YMF
    outfile:   file object for the GTrack file
    fastaFile: file object for a fasta file
    ''' 
    def _convertFromYMFToGTrack(self, fastaFile, infile, outfile):
        
        outfile.write('#\n# GTrack\n##Track type: valued segments\n###seqid\tstart\tend\tvalue\tstrand')

        sequenceHeaders = []
        sequences = []
        sequenceIndex = -1
        ymf = infile.readlines()
        
        # Adds the content of the fasta file into the sequences and sequenceHeaders list
        for line in fastaFile:
            
            # If its a new sequences (starting with '>'), append new header and sequence
            if line[:1] == '>':
                sequenceIndex = sequenceIndex + 1
                line = line.split(':')
                chromosome = line[0]
                regions = line[1].split('-')
                sequenceHeaders.append([chromosome, int(regions[0]), int(regions[1][:-1])])
                sequences.append('')
            else: # Else just append the sequence line with the current sequence 
                sequences[sequenceIndex] = sequences[sequenceIndex] + line[:-1]
        
        # For every line in the ymf file (except header)
        for i in range(1, len(ymf)):
            
            # If still more predictions
            if not ymf[i][:2] == ' 0':
                # Create a new pattern with the current prediction sequence
                data = ymf[i].split()
                pattern = r'(%s)' % data[0]
                pattern = re.compile(pattern, re.IGNORECASE)
                score = float(data[2])
                
                # For every sequence in the fasta file
                for j in range(0, len(sequences)):
                    # Check if the prediction sequence exists within the fasta sequence
                    match = re.search(pattern, sequences[j])
                    
                    # If yes, write the region to the GTrack file
                    if match:
                        start = int(match.start())+sequenceHeaders[j][1]
                        end = start+len(match.group(1))

                        outfile.write('\n%s\t%s\t%s\t%s\t%s' % (sequenceHeaders[j][0][1:], start, end, score, '+')) 
            else: # If no more prediction, just break
                break

        outfile.close()
        fastaFile.close()
        infile.close()
        
    def _normalizeGTrackValues(self, filepath, outfile):
        infile = open(filepath, 'r')
        
        # Copy header
        for line in infile:
            if line[0] == '#':
                outfile.write(line)
            else:
                break

        infile.close()
        infile = open(filepath, 'r')
        
        # Load values into numpy array
        vec = loadtxt(infile)
        
        # Retrieve largest and smallest values
        smallest = vec.min()
        largest = vec.max()

        diff = largest - smallest
        
        if not diff == 0.0:
            # Write normalized values to file
            for num in nditer(vec):
                outfile.write('%f\n' % ((num-smallest)/diff))
        else:
            for num in nditer(vec):
                outfile.write('%f\n' % 0.0)    
        
        infile.close()
        outfile.close()

    '''
    Converts a file of specified file format to GTrack.
    
    PARAMETERS
    
    filePath:      string containing the file path to the file which will be converted to GTrack
    fileFormat:    string containing the file format of the file specified by filePath
    galaxyFn:      string containing the galaxy file name
    fastaFilePath: string containing the file path to fasta file (needed in some cases)
    
    RETURNS
    
    A string containing the disk path the newly created GTrack file
    '''
    def convertToGTrack(self, filePath, fileFormat, galaxyFn, fastaFilePath=None, normalizeValues=False):
        
        predictionFile = open(filePath, 'r')
        
        out = GalaxyRunSpecificFile(['%smodified.gtrack' % filePath.split('/')[-1]], galaxyFn)
        gtrackFile = out.getFile('w')

        if fileFormat == 'weeder':
            self._convertFromWeederToGTrack(predictionFile, gtrackFile)
        elif fileFormat == 'meme':
            self._convertFromMemeToGTrack(predictionFile, gtrackFile)
        elif fileFormat == 'glimmer':
            self._convertFromGlimmerToGTrack(predictionFile, gtrackFile)
        elif fileFormat == 'prodigal':
            self._convertFromProdigalToGTrack(predictionFile, gtrackFile)
        elif fileFormat == 'genemark':
            self._convertFromGenemarkToGTrack(predictionFile, gtrackFile)
        elif fileFormat == 'blasthit':
            self._convertFromBlastToGTrack(predictionFile, gtrackFile)
        elif fileFormat == 'ymf':
            fastaFile = open(fastaFilePath, 'r')
            self._convertFromYMFToGTrack(fastaFile, predictionFile, gtrackFile)
        elif fileFormat == 'gtrack' and normalizeValues == True:
            self._normalizeGTrackValues(filePath, gtrackFile)
        return out.getDiskPath(True)
    