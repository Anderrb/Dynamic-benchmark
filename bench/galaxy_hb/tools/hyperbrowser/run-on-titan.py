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

import sys, os, getopt,types, time, subprocess, shutil

from gold.application.GalaxyInterface import *

import hyperbrowser.hyper_gui as hg

# checks if job is running/queued on titan
def checkjob(id):
    if id and id.isdigit():
        #print 'check ',id
        #proc = subprocess.Popen(['ssh', 'titan.uio.no', 'squeue -j '+id+' >/dev/null'])
        proc = subprocess.Popen(['squeue', '-j '+id])
        proc.wait()
        #print proc.returncode
        return proc.returncode == 0
    return False

def main():
    #print "running"
    tool = sys.argv[1]
    filename = sys.argv[2]
    filename = os.path.realpath(filename)
    params = hg.fileToParams(filename)
    titan_workdir = '/xanadu/project/rrresearch/galaxy_developer/database/tmp/'
    titan_filename = titan_workdir + os.path.basename(filename)
    shutil.copy(filename, titan_filename)
    print titan_filename
    
    #os.system('ssh titan.uio.no sbatch hb-titan/batchrun.sh ' + filename)
    filename_log = titan_filename + '.log'
    filename_err = titan_filename + '.err'
    filename_done = titan_filename + '.done'
    log = open(filename_log, "w+")

    sbatch_script = '/xanadu/home/morj/hb-titan/'+tool+'.sh'
    sbatch = ['ssh', 'titan.uio.no', 'sbatch --output='+filename_log+' --error='+filename_err + ' ' + sbatch_script + ' ' + titan_filename]
    #sbatch = ['/site/bin/sbatch', '--output='+filename_log, '--error='+filename_err, sbatch_script, filename]
    print sbatch
    submitproc = subprocess.Popen(sbatch, stderr=log)
    submitproc.wait()
    
    log.seek(0)
    line = log.readline()
    log.close()
    words = line.split(' ')
    if len(words) > 4:
        job_id = words[4].strip()
    else:
        job_id = None
    print line, job_id

    time.sleep(10)
    while (not os.path.exists(filename_done)):
        time.sleep(10)
        
    #os.unlink(filename + '.done')    

    shutil.copy(titan_filename, filename)

    log = open(filename_log, "r")
    for line in log:
        print line
    log.close()

    err = open(filename_err, "r")
    for line in err:
        print >> sys.stderr, line
    err.close()
    
    
if __name__ == "__main__":
    main()

