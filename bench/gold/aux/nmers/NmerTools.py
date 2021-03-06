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

class NmerTools:
    @classmethod
    def allNmers(cls, n):
        for i in xrange(4**n):
            yield cls.intAsNmer(i, n)
        
    @staticmethod
    def nmerAsInt(nmer):
        bpDict = dict( zip('acgt', range(4)) )
        revNmer = list(reversed(nmer.lower()))
        return sum( 4**i * bpDict[revNmer[i]] for i in range(len(revNmer)) )

    @staticmethod
    def intAsNmer(val, n):
        bpRevDict = dict( zip(range(4), 'acgt') )
        nmer = ''
        while val>0:
            nmer = bpRevDict[val%4] + nmer
            val = val/4
        nmer = bpRevDict[0]*(n-len(nmer)) + nmer #pad a's to beginning..
        return nmer

    @staticmethod
    def isNmerString(nmer):
        import re
        nmer = nmer.strip()
        return re.search('[^acgtACGT]', nmer) is None
        
    @staticmethod
    def getNotNmerErrorString(nmer):
        return 'Nmer contains symbols other than a, c, g, t, A, C, G or T: ' + nmer
        
    @staticmethod
    def getNmerAndCleanedNmerTrackName(trackName):
        from copy import copy
        tn = copy(trackName)
        tn[-1] = tn[-1].lower()
        nmer = tn[-1]
        if not tn[-2].endswith('-mers'):
            tn = tn[0:-1] + [str(len(nmer))+'-mers'] + tn[-1:]
        return nmer, tn
