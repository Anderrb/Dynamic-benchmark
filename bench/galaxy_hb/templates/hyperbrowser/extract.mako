<!--
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
-->

<%!
import sys
from cgi import escape
from urllib import quote, unquote

import hyperbrowser.hyper_gui as gui

class ExtractModel:
    def __init__(self, transaction, hb):
        galaxy = gui.GalaxyWrapper(transaction)
        self.params = galaxy.params
        self.genomes = [('----- Select -----', '', False)]
        self.genomes += hb.getAllGenomes(galaxy.getUserName())
        __state = self.params.get('__state')
        #if __state:
        #   self.state = pickle.loads(__state)
        
    def getGenome(self):
        return self.params.get('dbkey', self.genomes[0][1])
    genome = property(getGenome)

    def getRegion(self):
        return self.params.get('region', '*')
    region = property(getRegion)

    def getBinSize(self):
        return self.params.get('binsize', '*')
    binsize = property(getBinSize)
    
    def getMethod(self):
        return self.params.get('method', 'auto')
    method = property(getMethod)

    formAction = ''
    valid = ''
%>
<%
#reload(gui)

#print vars(trans.get_user().email)

#print sys.path

galaxy = gui.GalaxyWrapper(trans)

params = galaxy.params
#print params


model = ExtractModel(trans, hyper)

#genomes = hyper.getAllGenomes()
#genome = params.get('dbkey', genomes[0][1])
genomeElement = gui.SelectElement('dbkey', model.genomes, model.genome)
genomeElement.onChange = "resetAll();" + genomeElement.onChange 

datasets = []
try:
    datasets = galaxy.getHistory(hyper.getSupportedGalaxyFileFormats())
except:
    pass

track = gui.TrackWrapper('track1', hyper, [], galaxy, datasets, model.genome)
track.fetchTracks()
track.legend = 'Track'

#region = params.get('region', '*')
#binsize = params.get('binsize', '*')
#method = params.get('method', 'auto')

#methodOptions = [('Auto bins','auto'),('User-defined regions','binfile')]

extrOpts = []
datatype = params.get('datatype')
if track.selected():
    extrOpts = hyper.getTrackExtractionOptions(model.genome, track.definition())
    datatype = extrOpts[0][1] if datatype not in [eo[1] for eo in extrOpts] else datatype if not params.has_key('sepFilePrRegion') else 'html'

#print extrOpts

methodOptions = [('Bounding regions','__brs__'), ('Chromosomes','__chrs__'), ('Chromosome arms','__chrArms__'), ('Cytobands','__chrBands__'), ('Genes (Ensembl)','__genes__'), ('ENCODE Pilot regions','__encode__'), ('Custom specification','auto'),('Bins from history','binfile')]

%>
<%inherit file="base.mako"/>
<%namespace name="functions" file="functions.mako" />

<%def name="title()">Extract track</%def>
<%def name="head()">
    <script type="text/javascript">
        <%include file="common.js"/>
    </script>
</%def>

<form name="form" method="post" action="?">
<div class="genome">
##    Genome build: ${genomeElement.getHTML()} ${genomeElement.getScript()}    
    ${functions.genomeChooser(galaxy, genomeElement, model.genome)}
</div>
<div style="clear:both;height:0"></div>

${functions.trackChooser(track, 0, params)} 

%if track.selected() and len(extrOpts) > 0:
<fieldset><legend>Extract options</legend>

    <%include file="binoptions.mako" args="galaxy=galaxy,gui=gui,hyper=hyper,genome=model.genome,
        methodLabel='Extract in regions defined by',updateRunDescription=False,useBinSize=False,
        methodOptions=methodOptions,method=params.get('method','__chrs__'),track1=track,track2=None,extract=True"/>
    <div>
        <label>Extraction format:
        <script>
        var datatypes = new Array();
        var i = 0;
        </script>
        <select name="overlaps" id="overlaps" onchange="$('#datatype').val(datatypes[this.selectedIndex])">
            %for name,ext in extrOpts:
                <option value="${quote(name)}" ${gui.selected(params.get('overlaps'), quote(name))}>${name}</option>
                <script>datatypes[i++] = '${ext}';</script>
            %endfor
        </select>
        </label>
        <input type="hidden" name="datatype" id="datatype" value="${datatype}">
    </div>

</fieldset>

<p>Separate file per region: <input type="checkbox" name="sepFilePrRegion" onclick="if (this.checked){ $('#datatype').val('html') } else {$('#datatype').val(datatypes[form['overlaps'].selectedIndex])}" value="1" ${'checked' if params.has_key('sepFilePrRegion') else ''}"> </p>

<p id="status" style="font-weight:bold">${model.valid if model.valid != True else ''}</p>

<input id="start" type="button" value="Extract track" onclick="form.action='${h.url_for("/tool_runner")}';form.submit()">
%endif

    <INPUT TYPE="HIDDEN" NAME="mako" VALUE="extract">
    <INPUT TYPE="HIDDEN" NAME="tool_id" VALUE="hb_extract_1">
    <INPUT TYPE="HIDDEN" NAME="URL" VALUE="http://dummy">
    <INPUT TYPE="HIDDEN" NAME="__state" VALUE="">

    %if params.has_key('setparams'):
    <script type="text/javascript">
      $(document).ready(function () { with (document.forms[0]) { action='?'; submit(); }});
    </script>
    %endif

</form>

<%def name="toolHelp()">
In order for any track to be analyzed by The Genomic Hyperbrowser, it needs to be preprocessed into a highly efficient
file format. A track in the preprocessed format is not, however, easily readable and editable by users. 
The <i>Extract track</i> tool easily extracts any datasets that are loaded into the system and presents it to the user
as a history element, using either the original file format of the track, or a standard format.

<hr/ class='space'>
<b>Genome build</b>
<p>Choose the Genome build for the track you want to extract. The track list will update accordingly</p>

<hr/ class='space'>
<b>Track</b>
<p>Select the track that you want to extract. The tool will not proceed until you have choosen a valid track.</p>

<hr/ class='space'>
<b>Extract options</b>
<p>Define which regions of the track you want to extract. There are several options:
<ul>
<li><i>Bounding regions:</i> The bounding regions of the selected track, if defined
<li><i>Chromosomes:</i> Any or all complete chromosomes of the genome
<li><i>Chromosome arms:</i> Any or all complete chromosome arms (excluding centromers) of the genome
<li><i>Cytobands:</i> Any or all complete cytobands of the genome
<li><i>Genes (Ensembl):</i> Any or all Ensembl genes in the genome
<li><i>Custom specification:</i> Any consecutive region of the genome, divided into equal-sized bins
<li><i>Bins from history:</i> Use the regions defined in a history element (either BED or wig-format)
</ul>
<i>All options may not be available for all genomes or tracks</i></p>
<p>N.B. Any segment that is partly inside one of the regions selected is included in the extraction.
	To extract all contents of a track, leave the extract options in their default setting (all chromosomes).</p>

<hr/ class='space'>
<b>Extraction format</b> 
<p>The file format of the extracted track. There are several options:</p>
<ul>
<li><i>Original file format:</i> Export the track in its original format (the format of the original file, before preprocessing). 
	Returns the complete contents of each line, not just the information being used by the preprocessor.
<li><i>Segments, possibly overlapping:</i> Export the track as segments in the specified format (depends on the type
	of the track). Return overlapping segment individually, if any.
<li><i>Segments, any overlaps clustered:</i> Export the track as segments in the specified format (depends on the type
	of the track). Return overlapping segment as a single cluster, if any. A cluster is defined as one segment that spans 
	from the first to the last base pair of any segments overlapping.
<li><i>Segments, any overlaps clustered:</i> Export the track as a function track (wigFixed-format). 
	N.B. The returned text file may be very large.
</ul>
<hr/ class='space'>
<b>Separate file per region</b> 
<p>If this is checked, the track is extracted in separate files per region defined. All extract files are then compressed together into one single Zip file.</p>

<hr/ class='space'>
<a href='${h.url_for("hyper?mako=extract&tool_id=hb_extract_1&setparams=1&dbkey=hg18&track1=Genes%20and%20gene%20subsets%3AGenes%3ACCDS&method=__chrs__&__chrs__=chr20,%20chr21&sepFilePrRegion=1")}'>Demo</a>

</%def>
