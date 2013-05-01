<%!
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

import sys, os, traceback, json
from cgi import escape
from urllib import quote, unquote

import hyperbrowser.hyper_gui as gui

%>
<%
params = control.params

if control.prototype.isRedirectTool() or not control.prototype.isHistoryTool():
    formAction = '?'
else:
    formAction = h.url_for('/tool_runner')

%>
<%namespace name="functions" file="functions.mako" />
<%inherit file="base.mako" />
<%def name="title()">${control.prototype.getToolName()}</%def>
<%def name="head()">
    %if control.doRedirect():
        <meta http-equiv="Refresh" content="0; url=${control.getRedirectURL()}" />
    %endif
    <script type="text/javascript">
        <%include file="common.js"/>
    </script>
    ${h.js('sorttable')}
</%def>

%if control.userHasFullAccess():

    <form method="post" action="${formAction}">

    <INPUT TYPE="HIDDEN" NAME="old_values" VALUE="${quote(json.dumps(control.oldValues))}">
    <INPUT TYPE="HIDDEN" NAME="datatype" VALUE="${control.prototype.getOutputFormat(control.choices)}">
    <INPUT TYPE="HIDDEN" NAME="mako" VALUE="generictool">
    <INPUT TYPE="HIDDEN" NAME="tool_id" VALUE="${control.toolId}">
    <INPUT TYPE="HIDDEN" NAME="tool_name" VALUE="${control.toolId}">
    <INPUT TYPE="HIDDEN" NAME="URL" VALUE="http://dummy">

    %if len(control.subClasses) > 0:
        ${functions.select('sub_class_id', control.subClasses.keys(), control.subClassId, 'Select subtool:')}
    %endif

    %for i in control.inputOrder:
        %if control.inputTypes[i] == 'select':
            ${functions.select(control.inputIds[i], control.options[i], control.displayValues[i], control.inputNames[i])}
        %elif control.inputTypes[i] == 'multi':
            ${functions.multichoice(control.inputIds[i], control.options[i], control.displayValues[i], control.inputNames[i])}
        %elif control.inputTypes[i] == 'checkbox':
            ${functions.checkbox(control.inputIds[i], control.options[i], control.displayValues[i], control.inputNames[i])}
        %elif control.inputTypes[i] == 'text':
            ${functions.textarea(control.inputIds[i], control.displayValues[i], control.inputNames[i], control.options[i][1], readonly=False, reload=control.prototype.isDynamic())}
        %elif control.inputTypes[i] == 'text_readonly':
            ${functions.textarea(control.inputIds[i], control.displayValues[i], control.inputNames[i], control.options[i][1], readonly=True)}
        %elif control.inputTypes[i] == '__password__':
            ${functions.password(control.inputIds[i], control.displayValues[i], control.inputNames[i], reload=control.prototype.isDynamic())}
        %elif control.inputTypes[i] == '__genome__':
            ${functions.genomeChooser(control)}
        %elif control.inputTypes[i] == '__track__':        
            ${functions.trackChooser(control.trackElements[control.inputIds[i]], i, params, False)}
        %elif control.inputTypes[i] == '__history__':
            ${functions.history_select(control, control.inputIds[i], control.options[i], control.displayValues[i], control.inputNames[i])}
        %elif control.inputTypes[i] == '__multihistory__':
            ${functions.multihistory(control.inputIds[i], control.options[i], control.displayValues[i], control.inputNames[i])}
        %elif control.inputTypes[i] == '__hidden__':
            <input type="hidden" name="${control.inputIds[i]}" value="${control.displayValues[i]}">
        %elif control.inputTypes[i] == 'table':
            ${control.displayValues[i]}
        %endif
    %endfor
    
    <p><input id="start" type="submit" name="start" value="Execute" ${'disabled' if not control.isValid() else ''}></p>

    </form>

    %if control.hasErrorMessage():
        <p class="errormessage">${control.errorMessage}</p>
    %endif

    %if control.params.get('start') and not control.prototype.isHistoryTool() and control.isValid():
        <p class="infomessage">${control.executeNoHistory()}</p>
    %endif


    %if control.prototype.isBatchTool() and control.isValid() and control.userIsOneOfUs():
    <p class="infomessage" onclick="$('#batchline').toggle()">
        <a href="#batchline" title="Click to show/hide">Corresponding batch run line:</a>
        <span id="batchline" style="display:none"><br>
        ${control.getBatchLine()}
        </span>
    </p>
    %endif

%else:
    ${functions.accessDenied()}
%endif

<%def name="toolHelp()">
    ${control.prototype.getToolDescription()}

    %if control.getIllustrationImage():
        %if os.path.exists(control.getIllustrationImage().getDiskPath()):
            <p><hr><img width="100%" style="max-width: 640px; width: expression(this.width > 640 ? 640: true);" src="${control.getIllustrationImage().getURL()}"></p>
        %elif control.isDebugging():
            <p class="warningmessage">No imagefile exists at: ${control.getIllustrationImage().getDiskPath()}</p>
        %endif
    %endif

    %if control.hasDemoURL():
        <hr>
        <a href="${control.getDemoURL()}">Demo</a>
    %endif

</%def>

