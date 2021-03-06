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
<%def name="title()">Edit file from history</%def>

<%!
import sys,os
from cgi import escape
from urllib import quote, unquote

import hyperbrowser.hyper_gui as gui


class EditModel:
    def __init__(self, transaction, hb):
        self.galaxy = gui.GalaxyWrapper(transaction)
        self.params = self.galaxy.params
        self.genomes = hb.getAllGenomes(self.galaxy.getUserName())
        
    def getGenome(self):
        return self.params.get('dbkey', self.genomes[0][1])
    genome = property(getGenome)

    def getHistoryItem(self):
        return self.params.get('historyitem')
    historyitem = property(getHistoryItem)

    def getText(self):
        return self.params.get('text')
    text = property(getText)

    def getHistoryOptions(self):
        return self.galaxy.optionsFromHistory(gui.defaultFileTypes, self.historyitem)

    def getFilePath(self):
        path = None
        if self.historyitem:
            id = self.historyitem.split(',')[1]
            path = self.galaxy.getDataFilePath(id)
        return path
    
    def getFileContent(self):
        text = ''
        if self.historyitem and self.canEditFile():
            path = self.getFilePath()
            file = open(path)
            text = file.read()
            file.close()
        return escape(text)

    def saveFileContent(self):
        if self.historyitem and self.params.get('save') and self.text:
            path = self.getFilePath()
            file = open(path, "w")
            file.write((self.text))
            file.close()
            
    def canEditFile(self):
        return self.historyitem and os.path.getsize(self.getFilePath()) < 100000
        

%>
<%

model = EditModel(trans, hyper)

model.saveFileContent()

%>
<script>
    // from http://forumsblogswikis.com/2008/07/20/how-to-insert-tabs-in-a-textarea/
      function insertAtCursor(myField, myValue)
          {
          //IE support
          if (document.selection)
              {
              myField.focus();
              sel = document.selection.createRange();
              sel.text = myValue;
              }
          //MOZILLA/NETSCAPE support
          else if (myField.selectionStart || myField.selectionStart == '0')
              {
              var startPos = myField.selectionStart;
              var endPos = myField.selectionEnd;
              restoreTop = myField.scrollTop;
              myField.value = myField.value.substring(0, startPos) + myValue + myField.value.substring(endPos, myField.value.length);
              myField.selectionStart = startPos + myValue.length;
              myField.selectionEnd = startPos + myValue.length;
              if (restoreTop>0)
                  {
                  myField.scrollTop = restoreTop;
                  }
              }
          else
              {
              myField.value += myValue;
              }
          }



function trapTab(e) {
    if (e.keyCode == 9) {
        insertAtCursor(e.target, '\t');
        e.preventDefault();
    }
}

jQuery(function () {
    $('#text').bind('keydown', trapTab);
});

</script>
<form name="form" method="post" action="">

        <fieldset><legend>History</legend>
            <select name="historyitem" id="historyitem" onchange="this.form.submit()">
            	<option value=""> - Choose from history - </option>
                ${model.getHistoryOptions()}
            </select>
        </fieldset>

        %if model.canEditFile():
        <fieldset><legend>Edit file</legend>
            <textarea id="text" name="text" cols="90" rows="25" wrap="off" style="max-width:100%">${model.getFileContent()}</textarea>
        </fieldset>
        %elif model.historyitem:
        File too big.
        %endif

    <p><input name="save" type="submit" value="Save file"></p>


</form>