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
from galaxy import eggs
import pkg_resources
pkg_resources.require("matplotlib")

import matplotlib
from numpy import *
from pylab import *
from quick.util.StaticFile import GalaxyRunSpecificFile

'''
Handles the creation of statistic tables, graphs and plots based on a benchmark result.
'''
class StatisticPlot():
    
    '''
    Creates a ROC Curve based on a given benchmark result using matplotlib, 
    and saves it as a png picture file.
    
    PARAMATERS
    
    setId:           integer which identifies which test set we are evaluating
    algorithmNames:  list of strings containing names of the algorithms to be evaluated
    totalPositives:  float telling us the total number of positive answers
    totalNegatives:  float telling us the total number of negative answers
    rocResults:      list containing the roc marks from the roc statistic
    galaxyFn:        string containing the galaxy file name
    
    RETURNS
    
    A string with a link pointing to the ROC Curve picture file
    '''
    def createROCCurve(self, setId, algorithmNames, 
                       totalPositives, totalNegatives, rocResults, galaxyFn):
        
        colors = ['b', 'r', 'g', 'c', 'm', 'y']
        
        for i in range(0, len(algorithmNames)):
            algorithmName = algorithmNames[i]
            rocResult = rocResults[i]
            
            # Check if the result is ROC Curve compatible
            if not (rocResult == None or rocResult['Result'] == []):
                markList = rocResult['Result']
                rocMarks = [x[2] for x in reversed(sorted(markList))]
            
                nTrue = 0.0
                nFalse = 0.0
                sensitivity = [0.0]
                specificity = [0.0]
                
                area = 0.0
                
                # Sum the roc marks, calculate area, sensitivity and specificity
                for mark in rocMarks:
                    if mark == 1:
                        nTrue = nTrue + 1
                    elif mark == 0:
                        nFalse = nFalse + 1
                        area += (nTrue/ totalPositives) * (1.0/totalNegatives)

                    sensitivity.append(nTrue/totalPositives)
                    specificity.append(nFalse/totalNegatives)
                
                # Algorithm name handling
                if algorithmName == 'gtrack':
                    algorithmName = 'algorithm%d' % i
                
                label = '%s (%f AUC)' % (algorithmName, area)
                
                plot(specificity, sensitivity, color=colors[i], linestyle='-', label=label)
            
            # In case of too many benchmark results, break
            if i == len(colors):
                break
        
        xlabel("1 - Specificity")
        ylabel("Sensitivity")
        ylim([-0.01, 1.01])
        xlim([-0.01, 1.01])

        title('ROC curve')

        ax = subplot(1,1, 1)
        plot([0, 1], [0, 1], color='k', linestyle='--')
        plots, labels = ax.get_legend_handles_labels()
        
        legend(plots, labels, loc=4)
        
        statPlot = GalaxyRunSpecificFile(['rocPlot%d.png' % setId], galaxyFn)
        savefig(statPlot.getDiskPath(True))
        close()

        return statPlot.getLink('ROC Curve')

    '''
    Measures different binary classification statistics based on a benchmark result.
    The results are saved in a html table and a matplotlib bar chart. 
    
    PARAMETERS
    
    setId:           integer which identifies which test set we are evaluating
    algorithmNames:  list of strings containing names of the algorithms to be evaluated
    overlapResults:  list containing the result from the overlap statistic
    galaxyFn:        string containing the galaxy file name
    linkName:        string specifying the name of the output link
    
    RETURNS
    
    A string with a link pointing to the html page containing the statistical results
    '''
    def createBinaryClassificationStatistics(self, setId, 
                algorithmNames, overlapResults, galaxyFn, linkName):
        
        bars = []
        labels = ['SN', 'SP', 'ACC', 'PPV', 'NPV', 'PC', 'CC', 'ASP']
        colors = ['b', 'r', 'g', 'c', 'm','y']
        width = 0.1
        nMeasurements = len(labels)
        xlocations = arange(nMeasurements)+0.2
        statTable = GalaxyRunSpecificFile(['statTable%d.html' % setId], galaxyFn)
        statTableFile = statTable.getFile('w')
        
        # Writes the top column of the table
        statTableFile.write('<table border="1"><tr><td></td>')
        
        for label in labels:
            statTableFile.write('<td>%s</td>' % label)
        
        statTableFile.write('</tr>')
        
        for i in range(0, len(overlapResults)):
            overlapResult = overlapResults[i]
            
            tn = long(overlapResult['Neither'])
            fp = long(overlapResult['Only1'])
            fn = long(overlapResult['Only2'])
            tp = long(overlapResult['Both'])
            
            # Calculate statistics
            if tp+fn == 0:
                sensitivity = 0.0
            else:
                sensitivity = tp/float(tp+fn)
            
            if tn+fp == 0:
                specificity = 0.0
            else:
                specificity = tn/float(tn+fp)
            
            if tp+fp+fn+tn == 0:
                accuracy = 0.0
            else:
                accuracy = (tp+tn)/float(tp+fp+fn+tn)
            
            if tp+fp == 0:
                PPV = 0.0
            else:
                PPV = tp/float(tp+fp)
            
            if tn+fn == 0:
                NPV = 0.0
            else:
                NPV = tn/float(tn+fn)
            
            if tp+fn+fp == 0:
                PC = 0.0
            else:
                PC = tp/float(tp+fn+fp)
                
            if (tp+fp)*(fp+tn)*(tn+fn)*(fn+tp) == 0:
                CC = 0.0
            else:
                CC = (tp*tn-fp*fn)/float(math.sqrt((tp+fp)*(fp+tn)*(tn+fn)*(fn+tp)))
            
            ASP = (sensitivity+PPV)/2.0
            
            dataElements = [sensitivity, specificity, accuracy, PPV, NPV, PC, CC, ASP]
            
            # Algorithm name handling
            if algorithmNames[i] == 'gtrack':
                algorithmNames[i] = 'algorithm%d' % i
            
            # Add a new bar to the statistic plot
            bars.append(bar(xlocations+(width*i), dataElements, width=width, color=colors[i]))
            
            # Write a new column to the statistic table
            statTableFile.write('<tr><td>%s</td>' % algorithmNames[i])
            
            for dataElement in dataElements:
                statTableFile.write('<td>%.3f</td>' % float(dataElement))
            
            statTableFile.write('</tr>')
            
            # In case of too many benchmark results, break
            if i == len(colors):
                break
        
        statTableFile.write('</table>')
        
        # Create the bar chart
        xticks(xlocations+width, labels)
        title("Benchmark results")
        legend(bars, algorithmNames)
        ylim([0.0, 1.0])
        statPlot = GalaxyRunSpecificFile(['statisticPlot%d.png' % setId], galaxyFn)
        savefig(statPlot.getDiskPath(True))
        
        statTableFile.write('</br></br><img src="statisticPlot%d.png">' % setId)
        close()
        
        # Write explanations for the different measurements used.
        statTableFile.write('</br><ul>')
        statTableFile.write('<li><b>SN - Sensitivity:</b> Also called TP rate or recall. This measurement tell us that given a positive answer, what are the probability the test will also give a positive answer.')
        statTableFile.write('<li><b>SP - Specificity:</b> Also called FP rate. This measurement tell us that given a negative answer, what are the probability the test will produce a negative answer.')
        statTableFile.write('<li><b>ACC - Accuracy:</b> Shows the overall accuracy of the test. Meaning given any result, what is the probability its correct.')
        statTableFile.write('<li><b>PPV - Positive Predictive Value:</b> Also known as precision. This measurement gives us the probability that a positive test is correct.')
        statTableFile.write('<li><b>NPV - Negative Predictive Value:</b> This measurement gives us the probability that a negative test is correct.')
        statTableFile.write('<li><b>PC - Performance Coefficient: </b>')
        statTableFile.write('<li><b>CC - Correlation Coefficient:</b> This measure shows the overall quality of a result, where 1 means a perfect prediction, 0 a total random prediction, and -1 means a total opposite of the answer.')
        statTableFile.write('<li><b>ASP - Average Site Performance:</b>')
        statTableFile.write('</ul>')
        
        statTableFile.close()
        
        return statTable.getLink(linkName)
    
    '''
    Do some measurement for the function statistic, and creates a matplotlib bar chart.
    
    PARAMETERS
    
    algorithmNames:   list of strings containing names of the algorithms to be evaluated
    statisticResults: list containing the result from the statistic
    galaxyFn:         string containing the galaxy file name
    linkName:         string specifying the name of the output link
    
    RETURNS
    
    A string with a link pointing to the html page containing the statistical results
    '''
    def createFunctionAnalysisStatistic(self, 
            algorithmNames, statisticResults, galaxyFn, linkName):

        bars = []
        labels = ['AVWA', 'AVOA', 'Difference']
        colors = ['b', 'r', 'g', 'c', 'm','y']
        width = 0.05
        nMeasurements = len(labels)
        xlocations = arange(nMeasurements)+0.1
        statTable = GalaxyRunSpecificFile(['statTable.html'], galaxyFn)
        statTableFile = statTable.getFile('w')
        
        # Writes the top column of the table
        statTableFile.write('<table border="1"><tr><td></td>')

        for label in labels:
            statTableFile.write('<td>%s</td>' % label)
        
        statTableFile.write('</tr>')
        
        for i in range(len(statisticResults)):
            result = statisticResults[i]
            result = result['Result']
            
            nNucleotidesWithinAnswer = result[0]
            nNucleotidesOutsideAnswer = result[1]
            sumValuesWithinAnswer = result[2]
            sumValuesOutsideAnswer = result[3]
            
            averageValuesWithinAnswer = sumValuesWithinAnswer/nNucleotidesWithinAnswer
            averageValuesOutsideAnswer = sumValuesOutsideAnswer/nNucleotidesOutsideAnswer
            difference = averageValuesWithinAnswer - averageValuesOutsideAnswer
            
            dataElements = [averageValuesWithinAnswer, averageValuesOutsideAnswer, difference]
            
            # Algorithm name handling
            if algorithmNames[i] == 'gtrack':
                algorithmNames[i] = 'algorithm%d' % i
            
            # Add a new bar to the statistic plot
            bars.append(bar(xlocations+(width*i), dataElements, width=width, color=colors[i]))
            
            # Write a new column to the statistic table
            statTableFile.write('<tr><td>%s</td>' % algorithmNames[i])
            
            for dataElement in dataElements:
                statTableFile.write('<td>%.3f</td>' % float(dataElement))
            
            statTableFile.write('</tr>')
            
            
            # In case of too many benchmark results, break
            if i == len(colors):
                break
            
        statTableFile.write('</table>')
        
        # Create the bar chart
        xticks(xlocations+width, labels)
        title("Benchmark results")
        legend(bars, algorithmNames)
        ylim([0.0, 1.0])
        statPlot = GalaxyRunSpecificFile(['statisticPlot.png'], galaxyFn)
        savefig(statPlot.getDiskPath(True))
        
        statTableFile.write('</br></br><img src="statisticPlot.png">')
        close()
        
        statTableFile.write('</br><ul>')
        statTableFile.write('<li><b>AVWA - Average Value Within Answer</b> Calculates how high the algorithm scores within an answer segment. High means good!')
        statTableFile.write('<li><b>AVOA - Average Value Outside Answer</b> Calculates how high it scores outside the answer. Low means good!')
        statTableFile.write('<li><b>Difference</b> The difference of the measurements above. Higher is better!')
        statTableFile.write('</ul>')
        
        statTableFile.close()
        
        return statTable.getLink(linkName)
    
    '''
    
    PARAMETERS
    
    algorithmNames:     list of strings containing names of the algorithms to be evaluated
    probabilityResults: dictionary
    galaxyFn:           string containing the galaxy file name
    
    RETURNS
    
    Returns a list of strings containing links to the image files, one for each algorithm
    '''
    def createScoreDistributionStatistic(self,
                algorithmNames, probabilityResults, galaxyFn):
        
        bottomPlot = arange(0, 1.01, 0.01)
        index = 0
        
        links = []
        
        for result in probabilityResults:
            
            result = result['Result']
            
            totalAnswers = result[0]
            totalValues = result[1]
            answerValueCount = result[2]
            functionValueCount = result[3]
            
            functionPlot = []
            answerPlot = []
            
            for i in range(len(answerValueCount)):
                functionPlot.append(float(functionValueCount[i])/totalValues)
                answerPlot.append(float(answerValueCount[i])/totalAnswers)
            
            
            xlabel("Score")
            ylabel("Percentage count")
            xlim([0.0, 1.0])
            title('Score distribution statistic')
            plot(bottomPlot, functionPlot, color='r', linestyle='-', label='Function')
            plot(bottomPlot, answerPlot, color='g', linestyle='-', label='Answer')
            ax = subplot(1,1, 1)
            
            plots, labels = ax.get_legend_handles_labels()
        
            legend(plots, labels, loc=2)
        
            statPlot = GalaxyRunSpecificFile(['probPlot%d.png' % index], galaxyFn)
            savefig(statPlot.getDiskPath(True))
            close()
            
            links.append(statPlot.getLink('Score distribution statistic %s' % algorithmNames[index]))
            
            index = index + 1
            
        return links
    