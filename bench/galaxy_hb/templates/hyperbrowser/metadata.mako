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

<%inherit file="base.mako"/>
<%namespace name="functions" file="functions.mako" />

<%def name="title()">Metadata</%def>
<%def name="head()">
    <script type="text/javascript">
        <%include file="common.js"/>
    </script>
</%def>

<%!
import sys
from cgi import escape
from urllib import quote, unquote

import hyperbrowser.hyper_gui as gui

%>
<%
# reload hyper_gui.py if it was updated:
#reload(gui)

galaxy = gui.GalaxyWrapper(trans)

params = galaxy.params
#print params

genomes = hyper.getAllGenomes(galaxy.getUserName())
genome = params.get('dbkey', genomes[0][1])
genomeElement = gui.SelectElement('dbkey', genomes, genome)

#genome = 'hg18' if genome == 'hg18' else genome

track = gui.TrackWrapper('track1', hyper, [], galaxy, [], genome)
track.extraTracks = []
track.legend = 'Track'

track.fetchTracks()


if params.get('update') or params.get('update_all'):
    attrs = {}
    for p in params:
        pp = p.split('info_')
        if len(pp) == 2:
            key = pp[1]
            val = params.get(p)
            if params.get('update_' + key):
                #print 'updating ', key
                attrs[key] = True if val == 'True' else False if val == 'False' else val
    #print 'update all ', bool(params.get('update_all'))
    hyper.setTrackInfoRecord(genome, track.definition(), attrs, bool(params.get('update_all')), galaxy.getUserName())

info = ''
if track.definition():
    record = hyper.getTrackInfoRecord(genome, track.definition())
    info = hyper.getTrackInfo(genome, track.definition())
else:
    record = []
#print record

%>

<%def name="infoForm(info, hasSub)">
    %for r in info:
        <%
        val = r[2]
        if r[1]:
            name = 'info_' + r[1]
            if val == None or val == '':
                val = params.get(name, '')
                val = True if val == 'True' else False if val == 'False' else val
        checked = '' if hasSub else 'checked' if val == r[2] or (val == '' and r[3] == 'checkbox') else ''
        %>
        %if r[3] == 'textbox':
            <div><input type="checkbox" name="update_${r[1]}" ${checked}>
            <b>${r[0]}:</b><br>
            <textarea name="info_${r[1]}" rows="3" cols="200" style="${'font-style:italic' if not r[2] else ''}">${escape(val)}</textarea></div>
        %elif r[3] == 'checkbox':
            <div><input type="checkbox" name="update_${r[1]}" ${checked}>
            <b>${r[0]}: </b>
            <input type="checkbox" ${'checked' if val else ''} onchange="form['info_${r[1]}'].value=checked?'True':'False'">
            <input type="hidden" name="info_${r[1]}" value="${'True' if val else 'False'}">
            </div>
        %elif r[3] == 'text' and r[2]:
            <div><b>${r[0]}: </b>${r[2]}</div>
        %endif
    %endfor
</%def>

<form method="post" action="">
<input type="hidden" name="mako" value="${params.get('mako')}">
<div class="genome">
##    Genome build: ${genomeElement.getHTML()} ${genomeElement.getScript()}    
    ${functions.genomeChooser(galaxy, genomeElement, genome)}
</div>
<div style="clear:both;height:0"></div>

<fieldset><legend>${track.legend}</legend>

<%
    typeElement = gui.TrackSelectElement(track, 0)
    lastlevel = 0
    j = 1
%>
${typeElement.getHTML()} ${typeElement.getScript()}
    %while track.getTracksForLevel(j):
        <%
        levelElement = gui.TrackSelectElement(track, j)
        lastlevel = j
        j += 1
        %>
        <div style="margin-left:${j - 1}em">|_ ${levelElement.getHTML()} ${levelElement.getScript()}</div>
    %endwhile

    <input type="hidden" name="${track.nameMain}" value="${track.asString()}">
    %if hyper._userHasFullAccess(galaxy.getUserName()):
        %if track.valueLevel(0):
        <form name="infoform" action="">
            ${infoForm(record, track.hasSubtrack())}
            %if track.hasSubtrack():
                <input type="submit" name="update" value="Apply selected items to this category">
                <input type="submit" name="update_all" value="Apply selected items to all subtracks">
            %else:
                <input type="submit" name="update" value="Apply selected items to this track">
            %endif
        </form>
        %endif
    %else:
        ${info}
        <p>You must be one of us to update metadata</p>
    %endif

</fieldset>
</form>
<!-- ${galaxy.getUserIP()} -->