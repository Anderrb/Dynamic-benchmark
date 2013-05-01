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
#
AccuracyStat_cc = ('Correlation coefficient', 'Pearsons correlation coefficient between track1 and track2 represented as binary vectors (0 for uncovered base pairs, 1 for covered base pairs).')
AccuracyStat_hammingDistance = ('Hamming distance', 'The number of base pairs (hamming distance) having different assignment of being inside or outside segments according to track1 vs track2')
AccuracyStat_precision = ('Precision', 'Precision (TP/TP+FP), when track1 is viewed as predictions and track2 is viewed as answer')
AccuracyStat_recall = ('Recall', 'Recall (TP/TP+FN), when track1 is viewed as predictions and track2 is viewed as answer')
AssemblyGapCoverageStat_Assembly_gap_coverage = ('', '')
BasicCustomRStat_Result = ('Result', '')
BinSizeStat_Result = ('Result', '')
BpOverlapPValOneTrackFixedStat_BpsInTrack2Segments = ('Number of base pairs in track2 segments', '')
BpOverlapPValOneTrackFixedStat_P_value = ('', '')
BpOverlapPValOneTrackFixedStat_track2Coverage = ('Proportional coverage of track2', '')
BpOverlapPValOneTrackFixedStat_E_Test_statistic___ExpBpOverlap = ('E(Test statistic): Expected base pair overlap', '')
BpOverlapPValOneTrackFixedStat_track1Coverage = ('Proportional coverage of track1', '')
BpOverlapPValOneTrackFixedStat_ObsBpOverlap = ('Observed base pair overlap', '')
BpOverlapPValOneTrackFixedStat_Test_statistic__ObsBpOverlap = ('Test statistic: Observed base pair overlap', 'Test statistic: The number of base pairs covered by both tracks (i.e. their overlap at the base pair-level)')
BpOverlapPValOneTrackFixedStat_DiffFromMean = ('Difference from mean', '')
BpOverlapPValOneTrackFixedStat_NumBpInBin = ('Number of base pairs in the bin(s)', '')
BpOverlapPValStat_P_value = ('', '')
BpOverlapPValStat_track2Coverage = ('Proportional coverage of track2', '')
BpOverlapPValStat_ExpBpOverlap = ('Expected base pair overlap', '')
BpOverlapPValStat_track1Coverage = ('Proportional coverage of track1', '')
BpOverlapPValStat_NumBpInBin = ('Number of base pairs in bin', '')
BpOverlapPValStat_ObsBpOverlap = ('Observed base pair overlap', '')
BpOverlapPValStat_DiffFromMean = ('Difference from mean', '')
COMMON_Result = ('Main result', 'Main result of analysis')
COMMON_P_value = ('P-value','The probability of getting the observed value or a more extreme value under the null hypothesis')
COMMON_fdr = ('FDR-adjusted p-values','P-values adjusted by False Discovery Rate (Benjamini, Y., and Hochberg, Y., 1995)')
COMMON_Assembly_gap_coverage = ('Assembly gap coverage', 'The proportion of base pairs in each bin that are missing in the assembly that is used')
ComputeROCScoreFromRankedTargetControlMarksStat_Result = ('Result', '')
CountPointAllowingOverlapStat_Result = ('Number of track1-points (allowing overlaps)', '')
CountPointBothTracksStat_track2_count = ('Number of track2-points', '')
CountPointBothTracksStat_track1_count = ('Number of track1-points', '')
CountPointStat_Result = ('Counts', 'The number of track1-points')
CountStat_Result = ('Base pair coverage', 'The number of base pairs covered by track1')
DerivedOverlapStat_1in2 = ('Enrichment of track1 inside track2', 'The ratio of proportions of base pairs covered by track1_segments inside versus outside track2_segments')
DerivedOverlapStat_1inside2 = ('Proportion of track2_segments covered by track1', 'The proportion of the base pairs inside track2_segments that are covered by segments of track1')
DerivedOverlapStat_1outside2 = ('Proportion of regions outside track2_segments covered by track1', 'The proportion of the base pairs outside track2_segments that are covered by segments of track1')
DerivedOverlapStat_2in1 = ('Enrichment of track2 inside track1', 'The ratio of proportions of base pairs covered by track2_segments inside versus outside track1_segments')
DerivedOverlapStat_2inside1 = ('Proportion of track1_segments covered by track2', 'The proportion of the base pairs inside track1_segments that are covered by segments of track2')
DerivedOverlapStat_2outside1 = ('Proportion of regions outside track1_segments covered by track2', 'The proportion of the base pairs outside track1_segments that are covered by segments of track2')
DerivedOverlapStat_intersectionToUnionRatio = ('Ratio of bps covered by both tracks to bps covered by at least one track', 'Ratio of base pairs covered by both tracks to base pairs covered by at least one track')
DerivedPointCountsVsSegsStat_1in2 = ('Enrichment of track1_points inside track2', '')
DerivedPointCountsVsSegsStat_1inside2 = ('Proportion of track2_segments covered by track1_points', '')
DerivedPointCountsVsSegsStat_1outside2 = ('Proportion of regions outside track2_segments covered by track1_points', '')
DerivedPointCountsVsSegsStat_2in1 = ('Enrichment of track2_points inside track1', '')
DerivedPointCountsVsSegsStat_2inside1 = ('Proportion of track1_points covered by track2_segments', '')
DerivedPointCountsVsSegsStat_2outside1 = ('Proportion of all positions except track1_points covered by track2_segments', '')
DiffOfMeanInsideOutsideStat_Result = ('Difference of mean of track 2 inside track 1 vs outside', 'The difference between the mean value of track 2 inside the segments of track1 versus the rest of the bin')
DiffOfMeansAtPointsVsRemainingStat_Result = ('Difference of mean of track 2 at track 1 vs rest', 'The difference between the mean value of track 2 at the points of track 1 versus the rest of the bin')
DiffRelFreqPValStat_Result = ('P_value', '')
DiffRelFreqPValStat_P_Value = ('P_value', '')
DiffRelFreqPValStat_Test_statistic__Z_score = ('Test statistic: Z-score', 'Z-statistic based on the observed frequencies, using pooled standard deviation')
DiffRelFreqPValStat_EstDiff = ('Estimated diff. of relative frequency', 'The estimated difference of relative frequency between track 1 and track 2')
DiffRelFreqPValStat_SEDiff = ('Pooled std. dev.', 'The pooled standard deviation')
DiffRelFreqPValStat_CountTrack1 = ('Number of track1-points', '')
DiffRelFreqPValStat_CountTrack2 = ('Number of track2-points', '')
ExtractMarksStat_Result = ('', '')
FreqPerCatDistributionStat_Result = ('Category distribution', 'The distribution of the number of elements from each category of track1')
FunctionCorrelationPvalStat_Test_statistic__pearson = ('Test statistic: T-distributed measure based on Pearson correlation', 'The test statistic is as in the method cor.test in R')
FunctionCorrelationPvalStat_Test_statistic__kendall = ('Test statistic: Rank measure based on Kendall correlation (tau)', 'The test statistic is as in the method cor.test in R')
FunctionCorrelationPvalStat_Test_statistic__spearman = ("Test statistic: Rank measure based on Spearman's correlation (rho)", 'The test statistic is as in the method cor.test in R')
SimpleFunctionCorrelationPvalStat_Test_statistic__pearson = FunctionCorrelationPvalStat_Test_statistic__pearson
SimpleFunctionCorrelationPvalStat_Test_statistic__kendall = FunctionCorrelationPvalStat_Test_statistic__kendall
SimpleFunctionCorrelationPvalStat_Test_statistic__spearman = FunctionCorrelationPvalStat_Test_statistic__spearman
FunctionCorrelationPvalStat_Correlation__pearson = ('Pearson correlation coefficient', '')
FunctionCorrelationPvalStat_Correlation__kendall = ('Kendall rank correlation coefficient', '')
FunctionCorrelationPvalStat_Correlation__spearman = ("Spearman's rank correlation coefficient", '')
SimpleFunctionCorrelationPvalStat_Correlation__pearson = ('Pearson correlation coefficient', '')
SimpleFunctionCorrelationPvalStat_Correlation__kendall = ('Kendall rank correlation coefficient', '')
SimpleFunctionCorrelationPvalStat_Correlation__spearman = ("Spearman's rank correlation coefficient", '')

HigherFunctionInSegsPValStat_P_value = ('', '')
HigherFunctionInSegsPValStat_Test_statistic__T_score = ('Test statistic: T score', 'The student T score on the difference between the mean value of track 2 inside the segments of track 1 versus the rest of the bin')
HigherFunctionInSegsPValStat_meanInside = ('Mean of track 2 inside track 1-segments', 'The mean value of track 2 inside the segments of track 1')
HigherFunctionInSegsPValStat_meanOutside = ('Mean of track 2 outside track 1-segments', 'The mean value of track 2 outside the segments of track 1')
HigherFunctionInSegsPValStat_diffOfMeanInsideOutside = ('Difference of mean of track 2 inside track 1 vs outside', 'The difference between the mean value of track 2 inside the segments of track1 versus the rest of the bin')
HigherFunctionInSegsPValStat_varInside = ('Variance of track 2 inside track 1-segments', 'The variance of track 2 values inside the segments of track 1')
HigherFunctionInSegsPValStat_varOutside = ('Variance of track 2 outside track 1-segments', 'The variance of track 2 values outside the segments of track 1')
LogSumDistReshuffledStat_Result = ('Result', '')
LogSumDistStat_Result = ('Result', '')
LogSumSegDistReshuffledStat_meanOfNull = ('', '')
LogSumSegDistReshuffledStat_p_value = ('', '')
LogSumSegDistReshuffledStat_testStatistic = ('', '')
LogSumSegDistReshuffledStat_z_value = ('', '')
LogMeanDistStat_Result = ('Average log-distance', 'The average log-distance between each point in track 1 and its nearest point in track 2')
LogMeanSegDistStat_Result = ('Average log-distance', 'The average log-distance between each point in track 1 and its nearest segment in track 2')
LogSumSegDistStat_Result = ('Result', '')
MarksListStat_Result = ('Marks', 'The distribution of marks of track1-elements')
MarksSortedByFunctionValueStat_Result = ('Result', '')
MarksSortedBySegmentOverlapStat_Result = ('Result', '')
MeanAtPointsStat_Result = ('Mean of track 2 at track 1-points', 'The mean value of track 2 at the points of track 1')
MeanDistStat_Result = ('Average distance', 'The average distance between each point in track 1 and its nearest point in track 2')
MeanSegDistStat_Result = ('Average distance', 'The average distance between each point in track 1 and its nearest segment in track 2')
MeanInsideStat_Result = ('Mean of track 2 inside track 1-segments', 'The mean value of track 2 inside the segments of track 1')
MeanInsideOutsideTwoTailRandStat_Result = ('Result', '')
MeanMarkStat_Result = ('', '')
MeanStat_Result = ('Mean', 'Mean value of track1')
MeasureGraphDensity3dStat_WeightedEdges = ('Weighted edges','Total number of edges with a nonzero weight for track 1')
MeasureGraphDensity3dStat_totEdges = ('Total edges','Total number of edges for track 1')
MeasureGraphDensity3dStat_Density = ('Density rate','Density ratio of the graph (under 0.5 means the graph is sparse)')
MinAndMaxStat_max = ('Max', 'Maximum value of track1')
MinAndMaxStat_min = ('Min', 'Minimum value of track1')
NearestPointDistPValStat_P_value = ('', '')
NearestPointDistsStat_Result = ('Point distances', 'The distribution of distances from each track1-point to nearest track2-point')
NearestPointMarkDiffStat_Result = ('Result', 'The sum of squared difference between the mark of each point of track 1 and the corresponding mark of the nearest point of track 2')
NearestSegmentDistsStat_Result = ('Segment distances', 'The distribution of distances from each track1-segment to nearest track2-segment (seg-seg-dists)')
NearestSegmentDistsStat_SegLengths = ('Segment lengths', 'The length from each track1-segment')
NearestSegmentDistsStat_FromNames = ('Name of each track1-segment', 'The name of each track1-segment')
NearestSegmentDistsStat_ToNames = ('Name of nearest track2-segment', 'The name of the nearest track2-segment for each track1-segment')
NearestSegmentDistsStat_FromIds = ('Id of each track1-segment', 'The id of each track1-segment')
NearestSegmentDistsStat_ToIds = ('Id of nearest track2-segment', 'The id of the nearest track2-segment for each track1-segment')
NearestSegmentFromPointDistsStat_Result = ('Distances', 'The distribution of distances from each track1-point to nearest track2-segment (seg-seg-dists)')
NearestSegmentFromPointDistsStat_FromNames = ('Name of each track1-point', 'The name of each track1-point')
NearestSegmentFromPointDistsStat_ToNames = ('Name of nearest track2-segment', 'The name of the nearest track2-segment for each track1-point')
NearestSegmentFromPointDistsStat_FromIds = ('Id of each track1-point', 'The id of each track1-point')
NearestSegmentFromPointDistsStat_ToIds = ('Id of nearest track2-segment', 'The id of the nearest track2-segment for each track1-point')
PointCountInSegsPvalStat_Test_statistic__PointsInside = ('Test statistic: Number of track1-points inside track2-segments', 'The number of points of track 1 falling within the segments of track 2')
PointCountInSegsPvalStat_E_Test_statistic___ExpPointsInside = ('E(Test statistic): Expected number of track1-points inside track2-segments', 'The expected number of points of track 1 falling within the segments of track 2')
PointCountInSegsPvalStat_DiffFromExpected = ('Difference from expected', 'The difference between actual number of points of track 1 falling within the segments of track 2, and expected number')
PointCountInSegsPvalStat_PointsTotal = ('Total number of track1-points', '')
PointCountInSegsPvalStat_SegCoverage = ('Proportion of base pairs covered by track2-segments', 'The proportion of all base pairs that are covered by the segments of track 2')
PointCountInsideSegsStat_Result = ('Number of track1-points inside track2-segments', 'The number of points of track 1 falling within the segments of track 2')
PointCountPerSegStat_Result = ('', '')
PointCountsVsSegsStat_Both = ('track1-points inside track2', 'The number of track1 falling inside track2.')
#PointCountsVsSegsStat_Neither = ('Base pairs uncovered', 'The number of base pairs not covered by points of track1 or segments of track2. Warning: A somewhat fishy number..')
PointCountsVsSegsStat_Only1 = ('track1-points outside track2', 'The number of track1 falling outside track2')
#PointCountsVsSegsStat_Only2 = ('Base pairs covered by track2', 'The number of base pairs covered only by track2')
PropPointCountsVsSegsStat_Both = ('track1-points inside track2', 'The number of track1 falling inside track2.')
PropPointCountsVsSegsStat_BothProp = ('Proportion of track1-points inside track2', 'The proportion of track1 falling inside track2.')
PropPointCountsVsSegsStat_Only1 = ('track1-points outside track2', 'The number of track1 falling outside track2')
PropPointCountsVsSegsStat_Only1Prop = ('Proportion of track1-points outside track2', 'The proportion of track1 falling outside track2')
PropPointCountsVsSegsStat_SegCoverage = ('Proportion of base pairs covered by track2-segments', 'The proportion of all base pairs that are covered by the segments of track 2')
PropPointCountsAllowOverlapsVsSegsStat_Both = ('track1-points inside track2', 'The number of track1 falling inside track2.')
PropPointCountsAllowOverlapsVsSegsStat_BothProp = ('Proportion of track1-points inside track2', 'The proportion of track1 falling inside track2.')
PropPointCountsAllowOverlapsVsSegsStat_Only1 = ('track1-points outside track2', 'The number of track1 falling outside track2')
PropPointCountsAllowOverlapsVsSegsStat_Only1Prop = ('Proportion of track1-points outside track2', 'The proportion of track1 falling outside track2')
PropPointCountsAllowOverlapsVsSegsStat_SegCoverage = ('Proportion of base pairs covered by track2-segments', 'The proportion of all base pairs that are covered by the segments of track 2')
PointFreqInSegsVsSegMarksStat_Test_statistic__ObservedTau = ("Test statistic: Kendall's tau", 'Kendall rank correlation coefficient between the mark of a segment of track 2 and the number of points of track 1 inside that segment')
PointFreqInSegsVsSegMarksStat_NumberOfSegments = ('Number of segments of track 2', '')
PointFreqInSegsVsSegMarksStat_AverageNumberOfPointsInSegments = ('Avg. number of track1-points in track2-segments', 'The average number of track1-points that fall inside each track2-segments')
PointFreqStat_Result = ('Frequency', 'The frequency of track1-points (per base pair)')
PointPositioningPValStat_Test_statistic__W12 = ('Test statistic: Test statistic: Wilcoxon', 'For each segment of track 2, the relative position of each point of track 1 within the segment. The relative position is given the value -1 near the end of the segment and 0 near the middle of the segment. The test statistic is a Wilcoxon statistic based on a ranking of these relative positions.')
PointPositioningPValStat_Test_statistic__W34 = ('Test statistic: Wilcoxon', 'For each segment of track 2, the relative position of each point of track 1 within the segment. The relative position is given the value -1 near the upstream end of the segment and 1 near the downstream end of the segment. The test statistic is a Wilcoxon statistic based on a ranking of these relative positions')
PointPositioningPValStat_Test_statistic__W5 = ('Test statistic: Kolmogorov-Smirnov')
PointPositioningPValStat_N = ('Number of observations', 'The number of points of track 1 inside segments of track 2')
PointPositionsInSegsStat_Result = ('Result', '')
ProportionCountStat_Result = ('Proportional coverage', 'The proportion of base pairs covered by track1')
ProportionOverlapStat_Both = ('Base pairs covered by both', 'The number of base pairs covered by both tracks (i.e. their overlap at the base pair level)')
ProportionOverlapStat_BothProp = ('Proportion of base pairs covered by both', 'The proportion of base pairs covered by both tracks (i.e. their overlap at the base pair level)')
ProportionOverlapStat_Neither = ('Base pairs uncovered', 'The number of base pairs not covered by any of the two tracks')
ProportionOverlapStat_NeitherProp = ('Proportion of base pairs uncovered', 'The proportion of base pairs not covered by any of the two tracks')
ProportionOverlapStat_Only1 = ('Base pairs covered by only track1', 'The number of base pairs covered by only track1')
ProportionOverlapStat_Only1Prop = ('Proportion of base pairs covered by only track1', 'The proportion of base pairs covered by only track1')
ProportionOverlapStat_Only2 = ('Base pairs covered by only track2', 'The number of base pairs covered by only track2')
ProportionOverlapStat_Only2Prop = ('Proportion of base pairs covered by only track2', 'The proportion of base pairs covered by only track2')
ROCScoreFuncValBasedStat_Result = ('Result', '')
ROCScoreOverlapBasedStat_Result = ('Result', '')
RandomizationManagerStat_P_value = ('', '')
RandomizationManagerStat_MeanOfNullDistr = ('Mean of null distribution', '')
RandomizationManagerStat_TestStatistic = ('Test statistic', '')
RandomizationManagerStat_NumPointsTr1 = ('Number of elements in track 1', '')
RandomizationManagerStat_MedianOfNullDistr = ('Median of null distribution', '')
RandomizationManagerStat_SdNullDistr = ('Standard deviation of null distribution', '')
RandomizationManagerStat_DiffFromMean = ('Difference from mean', '')
RandomizationManagerStat_NumPointsTr2 = ('Number of elements in track 2', '')
RandomizationManagerStat_NumResamplings = ('Number of Monte Carlo samples', '')
RandomizationManagerStat_NumMoreExtremeThanObs = ('Number of Monte Carlo samples with extreme test statistic', 'Number of Monte Carlo samples where the value of the test statistic is as least as extreme as the observed value')
RawDataStat_Result = ('Result', '')
RawOverlapStat_Both = ('Base pairs covered by both', 'The number of base pairs covered by both tracks (i.e. their overlap at the base pair level)')
RawOverlapStat_Neither = ('Base pairs uncovered', 'The number of base pairs not covered by any of the two tracks')
RawOverlapStat_Only1 = ('Base pairs covered by only track1', 'The number of base pairs covered by only track1')
RawOverlapStat_Only2 = ('Base pairs covered by only track2', 'The number of base pairs covered by only track2')
SegmentLengthsStat_Result = ('Lengths', 'Distribution of lengths of each track1-segment')
SegmentLengthsStat_Names = ('Names', 'The name of each track1-segment')
SegmentLengthsStat_Ids = ('Ids', 'The id of each track1-segment')
SegmentDistancesStat_Result = ('Distances', 'Distribution of distances between neighboring track1-segments')
SegmentDistancesStat_LeftNames = ('Names to the left', 'The name of the track1-segment to the left of each gap')
SegmentDistancesStat_RightNames = ('Names to the right', 'The name of the track1-segment to the right of each gap')
SegmentDistancesStat_LeftIds = ('Ids to the left', 'The id of the track1-segment to the left of each gap')
SegmentDistancesStat_RightIds = ('Ids to the right', 'The id of the track1-segment to the right of each gap')
SimpleSimilarSegmentStat_Result = ('Fraction of segments that are similar', 'The fraction of track 1 and track 2 segments in the bin that is similar to a segment in the other track, where two segments are similar if the length of each segment divided by the total length of the two segments is larger than a specified threshold level')
SmoothedPointMarksStat_Result = ('Smoothed marks', 'Point marks smoothed by gaussian window also including neighbouring point marks')
StdDevStat_Result = ('Std. dev', 'The standard deviation of values of track1')
SumAtPointsStat_Result = ('', '')
SumInsideStat_Result = ('Result', '')
SumOfBpProductsStat_Result = ('Result', '')
SumOfSquaresInsideStat_Result = ('Result', '')
SumOfSquaresStat_Result = ('Result', '')
SumStat_Result = ('Sum', 'Sum of values of track1')
TpPointInSegStat_Both = ('Both', '')
TpPointInSegStat_Result = ('Result', '')
TpPointReshuffledStat_Result = ('Result', '')
TpPointReshuffledStat_meanOfNull = ('', '')
TpPointReshuffledStat_p_value = ('', '')
TpPointReshuffledStat_testStatistic = ('', '')
TpPointReshuffledStat_z_value = ('', '')
TpRawOverlapStat_Both = ('Both', '')
TpRawOverlapStat_Result = ('Result', '')
TpReshuffledStat_Result = ('Result', '')
TpReshuffledStat_meanOfNull = ('', '')
TpReshuffledStat_p_value = ('', '')
TpReshuffledStat_testStatistic = ('', '')
TpReshuffledStat_z_value = ('', '')
VarianceStat_Result = ('Variance', 'The variance of values of track1')
DivergentRowsInCategoryMatrixStat_simpleRatioRankedRowsMostCaseToLeastCase = ('Rows ranked by effect size','The rows of the contingency table ranked by effect size, from high to low. (effect equal to (o_ij-e_ij)/e_ij, with o and e according to note on test)')
DivergentRowsInCategoryMatrixStat_P_value = ('','')
DivergentRowsInCategoryMatrixStat_RankedRowsMoreInCase = ('Rows high in case','The rows of the contingency table with higher than expected values in case-columns. Ranked by their terms in the chi-square statistic, from high to low.')
DivergentRowsInCategoryMatrixStat_RankedRowsLessInCase = ('Rows low in case','The rows of the contingency table with higher than expected values in case-columns. Ranked by their terms in the chi-square statistic, from high to low.')
DivergentRowsInCategoryMatrixStat_Matrix = ('Full contingency table','')
DivergentRowsInCategoryMatrixStat_Rows = ('Rows','')
DivergentRowsInCategoryMatrixStat_Cols = ('Columns','')
TpRawSegsOverlapStat_Result = ('Observed base pair overlap', 'The number of base pairs that are inside segments of both tracks')
GenericResultsCombinerStat_AvgSegLenStat= ('Average segment length', '')
GenericResultsCombinerStat_CountElementStat = ('Number of track elements','')
GenericResultsCombinerStat_ProportionCountStat = ('Proportion of genome covered','')
SegmentOverviewWithoutOverlapStat_AvgSegLenStat= ('Average length of track elements (with overlaps clustered)', 'Average length of track elements, where any overlapping track elements are clustered to a single element.')
SegmentOverviewWithoutOverlapStat_CountElementStat = ('Number of track elements (with overlaps clustered)','The number of track elements, where any overlapping track elements are clustered to a single element. ')
SegmentOverviewWithoutOverlapStat_ProportionCountStat = ('Proportion of analysis region covered','The proportion of the analysis region (a bin or a union of bins) that is covered by track 1 elements.')

#GenericResultsCombinerStat_&&& = ('P(T1&T2&T3)', '')
#GenericResultsCombinerStat_&&&_GivenBinPresence = ('P(T1&T2&T3)', '')
#GenericResultsCombinerStat_&&* = ('P(T1&T2)*P(T3)', '')
#GenericResultsCombinerStat_&&*_GivenBinPresence = ('Sum_forEachBin( P(T1&T2)*P(T3) )', '')
#GenericResultsCombinerStat_&*& = ('P(T1&T3)*P(T2)', '')
#GenericResultsCombinerStat_&*&_GivenBinPresence = ('Sum_forEachBin( P(T1&T3)*P(T2) )', '')
#GenericResultsCombinerStat_&** = ('P(T1)*P(T2)*P(T3)', '')
#GenericResultsCombinerStat_&**_GivenBinPresence = ('Sum_forEachBin( P(T1)*P(T2)*P(T3) )', '')
#GenericResultsCombinerStat_*&& = ('P(T2&T3)*P(T1)', '')
#GenericResultsCombinerStat_*&&_GivenBinPresence = ('Sum_forEachBin( P(T2&T3)*P(T1) )', '')
#GenericResultsCombinerStat_*&* = ('P(T1)*P(T2)*P(T3)', '')
#GenericResultsCombinerStat_*&*_GivenBinPresence = ('Sum_forEachBin( P(T1)*P(T2)*P(T3) )', '')
#GenericResultsCombinerStat_**& = ('P(T1)*P(T2)*P(T3)', '')
#GenericResultsCombinerStat_**&_GivenBinPresence = ('Sum_forEachBin( P(T1)*P(T2)*P(T3) )', '')
#GenericResultsCombinerStat_*** = ('P(T1)*P(T2)*P(T3)', '')
#GenericResultsCombinerStat_***_GivenBinPresence = ('Sum_forEachBin( P(T1)*P(T2)*P(T3) )', '')
#GenericResultsCombinerStat_001 = ('Bps covered by T3', '')
#GenericResultsCombinerStat_010 = ('Bps covered by T2', '')
#GenericResultsCombinerStat_110 = ('Bps covered by T2&T3', '')
#GenericResultsCombinerStat_100 = ('Bps covered by T1', '')
#GenericResultsCombinerStat_101 = ('Bps covered by T1&T3', '')
#GenericResultsCombinerStat_110 = ('Bps covered by T1&T2', '')
#GenericResultsCombinerStat_111 = ('Bps covered by T1&T2&T3', '')