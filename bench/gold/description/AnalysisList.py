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

import os
import re

from gold.application.LogSetup import logMessage, logging, runtimeLogging
from config.Config import IS_EXPERIMENTAL_INSTALLATION
REPLACE_TEMPLATES = {}
#Inside $-signs, e.g. $MCFDR$
REPLACE_TEMPLATES['$MCFDR$']=\
'''
 [numResamplings:_Minimal number of MC samples=%s100/1000/10000/50000]
 [maxSamples:_Maximal number of MC samples=Unlimited/50000/10000/1000/100%s]
 [mThreshold:_Sequential MC threshold (m)=20/10/5]
 [fdrThreshold:_MCFDR threshold on FDR=0.005/0.01/0.05/0.1/0.001]
 [fdrCriterion:=simultaneous:]
''' % ( ('10/','/10') if IS_EXPERIMENTAL_INSTALLATION else ('','') )
REPLACE_TEMPLATES['$RANDSEED$'] = '[randomSeed:_Random seed=Random/0/1/2]'
REPLACE_TEMPLATES['$EXPERIMENTAL$'] = '[isExperimental:_=True]'
REPLACE_TEMPLATES['$PUBLIC$'] = '[isExperimental:_=False]'
REPLACE_TEMPLATES['$OVERLAP_HANDLING$'] = '[withOverlaps:_Overlap handling=no:Cluster overlaps/yes:Allow overlaps]'
REPLACE_TEMPLATES['$GLOBAL_SOURCE$'] = '[globalSource:_Normalize against=chrs:Whole genome (all chromosomes)/chrarms:Genome excl centromere (all chr arms)/ensembl:Genes (All Ensembl gene regions)/userbins:Analysis domain (Union of analysis bins)]'
#[allowOverlaps:_Overlap handling=False:Cluster overlaps/True:Allow overlaps]

def replaceFromTemplate(matchobj):
    templ = matchobj.group(0) #.replace('$','')
    return REPLACE_TEMPLATES[templ]
        
#[fdrCriterion:FDR stopping criterion=simultaneous:all tests simultaneously/individual:each test individually]

#fewer/more, closer/distant,
RAW_ANALYSIS_SPECS = {}

FUNCTION_SUMMARIZERS = 'MeanStat:Mean/StdDevStat:Std dev/SumStat:Sum/BinSizeStat:Bin length'
POINTS_SUMMARIZERS = 'CountPointStat:Element count/CountPointAllowingOverlapStat:Element count (allowing overlaps)/PointFreqStat:Element frequency (count divided by bin size)/BinSizeStat:bin length'
SEGMENTS_SUMMARIZERS = 'CountStat:Bp coverage/ProportionCountStat:Proportional coverage/BinSizeStat:bin length'
VALUED_POINTS_SUMMARIZERS = 'MeanMarkStat:Mean of values/' + POINTS_SUMMARIZERS

RAW_ANALYSIS_SPECS['Hypothesis testing:P-P'] = '''
Different frequencies?:
    Where is the relative frequency of points of track 1 different from the relative frequency of points of track 2, [tail:Alternative hypothesis=more:more/less:less/different:differently] than expected by chance?
    $GLOBAL_SOURCE$
    [withOverlaps:_Overlap handling=no:Cluster overlaps/yes:Allow overlaps]
    [H0:_=The expected fraction of points of track 1 in the bin is equal to the expected fraction of points of track 2 in the bin]
    [H1_more:_=The expected fraction of points of track 1 in the bin is higher than the expected fraction of points of track 2 in the bin]
    [H1_less:_=The expected fraction of points of track 1 in the bin is smaller than the expected fraction of points of track 2 in the bin]
    [H1_different:_=The expected fraction of points of track 1 in the bin is not equal to the expected fraction of points of track 2 in the bin]
    [assumptions:_=default:Preserve the total number of points in both tracks; randomize their positions]
    -> DiffRelFreqPValStat
    
Located nearby?:
    Are the points of track 1 [tail:Alternative hypothesis=less:closer to/more:further apart from/different:either closer to or further apart from] the points of track 2 than expected by chance?
    [H0:_=The points of track 1 are located independently of the points of track 2]
    [H1_more:_=The points of track 1 are located close to the points of track 2]
    [H1_less:_=The points of track 1 are located far apart from the points of track 2]
    [H1_different:_=The locations of the points of track 1 are dependent on the locations of the points of track 2]
    [assumptions:_Null model=
        PermutedSegsAndSampledIntersegsTrack_:Preserve points of T2 and number of points of T1; randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_:Preserve points of T2 and inter-point distances of T1; randomize positions (T1) (MC)]
    $MCFDR$
    $RANDSEED$
#    [rawStatistic:=LogMeanDistStat:]
    [rawStatistic:_Test statistic=MeanDistStat:Arithmetic mean of distances/LogMeanDistStat:Geometric mean of distances]
#    [rawStatistic:_Test statistic=LogMeanDistStat:Average log-distance/MeanDistStat:Average distance]
    [distDirection:=both:]
    -> RandomizationManagerStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:S-F'] = '''
Higher values inside?:Are the values of track 2 [tail:Alternative hypothesis=more:higher/less:lower/different:different] inside the segments of track 1, than what is expected by chance?
    [H0:_=The expected value of the function of track 2 is the same in the segments of track 1 as in the rest of the bin/genome]
    [H1_more:_=The expected value of the function of track 2 is higher in the segments of track 1 than in the rest of the bin/genome]
    [H1_less:_=The expected value of the function of track 2 is lower in the segments of track 1 than in the rest of the bin/genome]
    [H1_different:_=The expected value of the function of track 2 in the segments of track 1 is different from the expected value in the rest of the bin/genome]
    [rawStatistic:=DiffOfMeanInsideOutsideStat:]
#    [rawStatistic:=MeanInsideStat:]
    [assumptions:_Null model=
#        independentFuncVals:Preserve segments (T1); draw function values independently according to normal distribution (T2)/
        PermutedSegsAndSampledIntersegsTrack_:Preserve function (T2) and segment lengths (T1); randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_:Preserve function (T2), segment lengths and inter-segment gaps (T1); randomize positions (T1) (MC)]
    $MCFDR$
    $RANDSEED$
    -> RandomizationManagerStat
#    -> HigherFunctionInSegsPValStat, RandomizationManagerStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:P-F'] = '''
Higher values at locations?:
    Are the values of track 2 [tail:Alternative hypothesis=more:higher/less:lower/different:different] at the points of track 1, than what is expected by chance?
    [H0:_=The expected value of the function of track 2 is the same at the points of track 1 as in the rest of the bin/genome]
    [H1_more:_=The expected value of the function of track 2 is higher at the points of track 1 than in the rest of the bin/genome]
    [H1_less:_=The expected value of the function of track 2 is lower at the points of track 1 than in the rest of the bin/genome]
    [H1_different:_=The expected value of the function of track 2 at the points of track 1 is different from the expected value in the rest of the bin/genome]
    [rawStatistic:=DiffOfMeansAtPointsVsRemainingStat:]
#    [rawStatistic:=MeanAtPointsStat:]
    [assumptions:_Null model=
        PermutedSegsAndSampledIntersegsTrack_:Preserve function (T2) and number of points (T1); randomize positions uniformly (T1) (MC)/
        SegsSampledByIntensityTrack_:Preserve function (T2) and number of points (T1); randomize positions by intensity (T1) (MC)]
    $MCFDR$
    $RANDSEED$
    -> RandomizationManagerStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:P-S'] = '''
Located inside?:
    Are the points of track 1 falling inside the segments of track 2, [tail:Alternative hypothesis=more:more/less:less/different:differently] than expected by chance?
    [H0:_=The points of track 1 are located independently of the segments of track 2 with respect to whether they fall inside or outside]
    [H1_more:_=The points of track 1 tend to fall inside the segments of track 2]
    [H1_less:_=The points of track 1 tend to fall outside the segments of track 2]
    [H1_different:_=The locations of the points of track 1 are dependent on the locations of the segments of track 2 with respect to whether they fall inside or outside]
    [rawStatistic:=PointCountInsideSegsStat:]
    [assumptions:_Null model=
        poissonPoints:Preserve segments (T2) and number of points (T1); randomize point positions/
        _PermutedSegsAndSampledIntersegsTrack:Preserve points (T1) and segment lengths (T2); randomize positions (T2) (MC)/
        _PermutedSegsAndIntersegsTrack:Preserve points (T1), segment lengths and inter-segment gaps (T2); randomize positions (T2) (MC)/
        PermutedSegsAndSampledIntersegsTrack_:Preserve segments (T2) and number of points (T1); randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_:Preserve segments (T2) and inter-point distances (T1); randomize positions (T1) (MC)/
        SegsSampledByIntensityTrack_:Preserve segments (T2) and number of points (T1); randomize positions by intensity (T1) (MC)]
#        RandomGenomeLocationTrack_:Preserve segments (T2); randomize points (T1) by uniform selection of bin from genome (MC)/
#        _RandomGenomeLocationTrack:Preserve points (T1); randomize segments (T2) by uniform selection of bin from genome (MC)]
    $MCFDR$
    $RANDSEED$
    [illustrationFn:=P_S_MoreInside.png:]
    -> PointCountInSegsPvalStat, RandomizationManagerStat
    
Located nonuniformly inside?:
    Do the points of track 1 tend to accumulate more
    [tail:Alternative hypothesis=ha1:towards the borders/ha2:towards the middle/ha3:towards the upstream side/ha4:towards the downstream side/less] of the segments of track 2?
#    [tail=less/more]
    [H0:_=The points of track 1 have a uniform distribution within the segments of track 2]
    [H1_less:_=The points of track 1 tend to be positioned towards the upstream side of the segments of track 2]
    [H1_more:_=The points of track 1 tend to be positioned towards the downstream side of the segments of track 2]     
    [H1_ha1:_=The points of track 1 tend to be positioned towards the borders of the segments of track 2]
    [H1_ha2:_=The points of track 1 tend to be positioned towards the middle of the segments of track 2]
    [H1_ha3:_=The points of track 1 tend to be positioned towards the upstream side of the segments of track 2]
    [H1_ha4:_=The points of track 1 tend to be positioned towards the downstream side of the segments of track 2]
    [H1_ha5:_=The points of track 1 are unequally distributed within segments of track 2]
    [assumptions:_Null model=
        independentPoints:Preserve segments (T2) and number of points (T1); randomize positions (T1)/
        PermutedSegsAndIntersegsTrack_:Preserve segments (T2), inter-point distances (T1); randomize positions (T1) (MC)/
        _PermutedSegsAndIntersegsTrack:Preserve points (T1), segment lengths and inter-segment gaps (T2); randomize positions (T2) (MC)]
    $MCFDR$
    $RANDSEED$
    [rawStatistic:=AvgRelPointPositioningStat:]
    -> PointPositioningPValStat    
#    -> PointPositioningPValStat,RandomizationManagerStat
     
Located nearby?:
    Are the points of track 1 [tail:Alternative hypothesis=less:closer to/more:further apart from/different:either closer to or further apart from] the segments of track 2 than expected by chance?
    [H0:_=The points of track 1 are located independently of the segments of track 2]
    [H1_more:_=The points of track 1 are located close to the segments of track 2]
    [H1_less:_=The points of track 1 are located far apart from the segments of track 2]
    [H1_different:_=The locations of the points of track 1 are dependent on the locations of the segments of track 2]
    [assumptions:_Null model=
        PermutedSegsAndSampledIntersegsTrack_:Preserve segments (T2) and number of points (T1); randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_:Preserve segments (T2) and inter-point distances (T1); randomize positions (T1) (MC)]
    $MCFDR$
    $RANDSEED$
#    [rawStatistic:=LogMeanSegDistStat:]
    [rawStatistic:_Test statistic=LogMeanSegDistStat:Average log-distance/MeanSegDistStat:Average distance]
    [distDirection:=both:]
    -> RandomizationManagerStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:VP-S'] = '''
Higher values inside segments?:
    Do the points of track 2 that occur inside segments of track 1 have [tail:Alternative hypothesis=more:higher/less:lower/different:different] values than points occuring outside segments of track 1?
    [H0:_=The tendency of points of track 2 to locate inside versus outside segments of track 1, is independent of the value of the points of track 2]
    [H1_more:_=Higher valued points of track 2 are located more inside segments of track 1 than lower valued points]
    [H1_less:_=Lower valued points of track 2 are located more inside segments of track 1 than higher valued points]
    [H1_different:_=Higher valued and lower valued points of track 2 have different tendencies to be located inside segments of track 1]
    [assumptions:_Null model=
    _ShuffledMarksTrack:Preserve points (T2) and segments (T1); randomize values (T2)]
    $MCFDR$
    $RANDSEED$
    [rawStatistic:=MeanInsideStat:]
    -> RandomizationManagerStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:S-S'] = '''
Similar segments?:
    Are track1-segments similar (in position and length) to track2-segments, [tail:Alternative hypothesis=more:more/less:less/different:differently] than expected by chance?
    [rawStatistic:=SimpleSimilarSegmentStat:]
    $MCFDR$
    $RANDSEED$
#    [maxAbsDifference:_Max bp difference=0/2/5/10/20/50]
#    [maxRelDifference:_Max relative difference=0.01/0.05/0.1/0.2/0.5/1]
    [H0:_=The segments of track 1 are independent of the segments of track 2 with respect to similarity (in position and length)]
    [H1_more:_=The segments of track 1 are similar (in position and length) to the segments of track 2]
    [H1_less:_=The segments of track 1 are far from similar (in position and length) to the segments of track 2]
    [H1_different:_=The segments of track 1 are dependent on the segments of track 2 with respect to similarity (in position and length).]
    [minRelSimilarity:_Relative similarity threshold=1.0/0.99/0.95/0.9/0.8/0.7/0.6/0.5/0.25/0.1]
    [assumptions:_Null model=
        PermutedSegsAndSampledIntersegsTrack_:Preserve segments (T2) and segment lengths (T1); randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_:Preserve segments (T2), segment lengths and inter-segment gaps (T1); randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_PermutedSegsAndIntersegsTrack:Preserve segment lengths and inter-segment gaps; randomize positions (T1 & T2) (MC)]
    -> RandomizationManagerStat
    
Overlap?:
    Are the segments of track 1 overlapping the segments of track 2, [tail:Alternative hypothesis=more:more/less:less/different:differently] than expected by chance?
    [H0:_=The segments of track 1 are located independently of the segments of track 2 with respect to overlap]
    [H1_more:_=The segments of track 1 tend to overlap the segments of track 2]
    [H1_less:_=The segments of track 1 tend to avoid overlapping the segments of track 2]
    [H1_different:_=The locations of the segments of track 1 are dependent on the locations of the segments of track 2 with respect to overlap]
    [assumptions:_Null model=
        Tr1IndependentBps:Preserve segments (T2) and total base pair coverage (T1); randomize base pairs independently (T1)/
        bothIndependentBps:Preserve total base pair coverage; randomize base pairs independently (T1 & T2)/
        PermutedSegsAndSampledIntersegsTrack_:Preserve segments (T2) and segment lengths (T1); randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_:Preserve segments (T2), segment lengths and inter-segment gaps (T1); randomize positions (T1) (MC)/
        PermutedSegsAndSampledIntersegsTrack_PermutedSegsAndSampledIntersegsTrack:Preserve segment lengths; randomize positions (T1 & T2) (MC)/
        PermutedSegsAndIntersegsTrack_PermutedSegsAndIntersegsTrack:Preserve segment lengths and inter-segment gaps; randomize positions (T1 & T2) (MC)]
#        _RandomGenomeLocationTrack:Preserve segments (T1); randomize segments (T2) by uniform selection of bin from genome (MC)]
    $MCFDR$
    $RANDSEED$
    [illustrationFn:=S_S_Overlap.png:]
    [rawStatistic:=TpRawSegsOverlapStat:]
    -> BpOverlapPValOneTrackFixedStat, BpOverlapPValStat, RandomizationManagerStat
     
Located nearby?:
    Are the segments of track 1 [tail:Alternative hypothesis=less:closer to/more:further apart from/different:either closer to or further apart from] the segments of track 2 than expected by chance?
    [H0:_=The segments of track 1 are located independently of the segments of track 2]
    [H1_more:_=The segments of track 1 are located close to the segments of track 2]
    [H1_less:_=The segments of track 1 are located far apart from the segments of track 2]
    [H1_different:_=The locations of the segments of track 1 are dependent on the locations of the segments of track 2]
    [assumptions:_Null model=
        PermutedSegsAndSampledIntersegsTrack_:Preserve segments (T2) and segment lengths (T1); randomize positions (T1) (MC)/
        PermutedSegsAndIntersegsTrack_:Preserve segments (T2), segment lengths and inter-segment gaps (T1); randomize positions (T1) (MC)]
    $MCFDR$
    $RANDSEED$
    [rawStatistic:_Test statistic=LogMeanSegSegDistStat:Average log-distance/MeanSegSegDistStat:Average distance]
    [distDirection:=both:]
    -> RandomizationManagerStat'''    

RAW_ANALYSIS_SPECS['Hypothesis testing:VP-VP'] = '''
Nearby values similar?:
    When track1-points and track2-point are nearby each other, are the values [tail:Alternative hypothesis=more:more/less:less/different:differently] similar than expected by chance?
    [H0:_=The value of a point in track 1 and the value of its nearest point in track 2 are independent]
    [H1_more:_=The value of a point in track 1 is more similar to the value of its nearest point in track 2]
    [H1_less:_=The value of a point in track 1 is less similar to the value of its nearest point in track 2]
    [H1_different:_=The value of a point in track 1 depends on the value of its nearest point in track 2]
    [rawStatistic:=NearestPointMarkDiffStat:]
    [assumptions:_Null model=
        _PermutedSegsAndSampledIntersegsTrack:Preserve valued points (T1), values (T2); randomize positions (T2) (MC)/
        _PermutedSegsAndIntersegsTrack:Preserve valued points (T1), values and inter-point distances (T2); randomize positions (T2) (MC)]
    $MCFDR$
    $RANDSEED$
    -> RandomizationManagerStat

# Discrete values
#
#Nearby values similar?:
#    When track1-points and track2-point are nearby each other, are the values [tail:Alternative hypothesis=different:differently] similar than expected by chance?
#    [H0:_=The value of a point in track 1 and the value of its nearest point in track 2 are independent]
#    [H1_different:_=The value of a point in track 1 depends on the value of its nearest point in track 2]]
#    [assumptions:_Null model=
#        ?]
#    ->
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:VP-VS'] = '''
#    Are the values of the points in track 1 that are inside segments of track 2 independent?
#
Categories differentially located in targets?:
    Which categories of track1-points fall more inside case than control track2-segments?
    [rawStatistic:=PointCountInsideSegsStat:]
    -> DivergentRowsInCategoryMatrixStat
Category pairs differentially co-located?:
    Which categories of track1-points fall more inside which categories of track2-segments?
    [countMethod:_Method of counting points=
        count:Simple count/
        binary:Only 1 count per bin (binary)/
        logOfCount:Sum of logarithmical value per bin]
    [normalizePointsBy:_Normalize counts=
        rowSumBalanced:Differentially in both directions/
        rowCountBalanced:Differentially for points only/
        nothing:Do not normalize]
    [distMethod:_Row or column dissimilarity measure=
        euclidean:Euclidean distance/
        euclidean_positive:Euclidean distance of positive terms only/
        manhattan:Manhattan distance/manhattan_positive:Manhattan distance of positive terms only/
        minkowski:Cubic distance (Minkowski of power 3)/
        minkowski_positive:Cubic distance of positive terms only (Minkowski of power 3)]
    [clustMethod:_Hierarchical clustering method=
        average:Average linkage/
        complete:Complete linkage (max distance)/
        single:Single linkage (min distance)/
        centroid:Centroid linkage/
        ward:Ward\'s minimum-variance method/
        diana:Divisive Analysis Clustering]
    [numClustersRows:_Number of clusters of track 1 to divide results into=1/2/3/5/10/20/30/50/100/200/300/500]
    [numClustersCols:_Number of clusters of track 2 to divide results into=1/2/3/5/10/20/30/50/100/200/300/500]
    [pValueAdjustment:_P-value adjustment=unadjusted:Unadjusted p-values/fdr:FDR-adjusted p-values]
    [threshold:_P-value threshold for significance=0.0001/0.001/0.005/0.01/0.05/0.1/0.25/0.5/0.75/1]
    [childStat:=CategoryDivergenceMatrixStat:]
    -> ClusterMatrixStat
'''

#Divergence matrix: Divergence matrix of categorical track1-points that falls inside categorical track2-segments [countMethod:_Method of counting points=count:Simple count/binary:Only 1 count per bin (binary)/logOfCount:Sum of logarithmical value per bin][normalizePointsBy:_Normalize points by=rowSum:For each point category, the sum of points inside segments over all segment categories/rowSumBalanced:For each point category, the sum of points inside segments over all segment categories (Balanced version)/rowCount:The total number of points for each point category/rowCountBalanced:The total number of points for each point category (Balanced version)/nothing:Do not normalize][distMethod:_Feature vector dissimilarity method=euclidean:Euclidean distance/euclidean_positive:Euclidean distance of positive terms only/euclidean_min_1.0:Euclidean distance of terms larger or equal to 1.0/manhattan:Manhattan distance/manhattan_positive:Manhattan distance of positive terms only/minkowski:Cubic distance (Minkowski of power 3)/minkowski_positive:Cubic distance of positive terms only (Minkowski of power 3)/spearman:Spearman rank correlation coefficient] [clustMethod:_Hierarchical clustering method=complete:Complete linkage (max distance)/single:Single linkage (min distance)/average:Average linkage/centroid:Centroid linkage/ward:Ward\'s minimum-variance method/diana:Divisive Analysis Clustering] [numClustersRows:_Number of clusters of track 1 to divide results into=1/2/3/5/10/20/30/50/100/200/300/500][numClustersCols:_Number of clusters of track 2 to divide results into=1/2/3/5/10/20/30/50/100/200/300/500][pValueAdjustment:_P-value adjustment=unadjusted:Unadjusted p-values/fdr:FDR-adjusted p-values][threshold:_P-value threshold for significance=0.0001/0.001/0.005/0.01/0.05/0.1/0.25/0.5/0.75/1][childStat:=CategoryDivergenceMatrixStat:] -> ClusterMatrixStat
#The exponent of the next power of 2 larger than the count (logarithmical)

RAW_ANALYSIS_SPECS['Hypothesis testing:P-VS'] = '''
Located in segments with high values?:
    Does the number of track1-points that fall in track2-segments depend on the value of track2-segments?
    [tail:_=different]
    [H0:_=For the segments of track 2, the value of a segment is uncorrelated with the number of points from track 1 that fall within that segment]
    [H1_different:_=For the segments of track 2, the value of a segment is correlated with the number of points from track 1 that fall within that segment]
    [assumptions:_Null model=
        permuteMarks:Preserve points (T1) and segments (T2); permute the values of T2-segments]
    [assumptions2:_Other assumptions=
        equalLength:All segments of track 2 are of the same length, or segment length considered unimportant]
    [markType:=number:]
    -> PointFreqInSegsVsSegMarksStat

Located in case segments:
    Does the number of track1-points that fall in track2-segments depend on whether the track2-segments are marked as case or control?
    [tail:_=different]
    [H0:_=For the segments of track 2, the value of a segment is uncorrelated with the number of points from track 1 that fall within that segment]
    [H1_different:_=For the segments of track 2, the value of a segment is correlated with the number of points from track 1 that fall within that segment]
    [assumptions:_Null model=
        permuteMarks:Preserve points (T1) and segments (T2); permute the values of T2-segments]
    [markType:=tc:]
    [illustrationFn:=P_VS_MoreInCase.png:]
    -> PointFreqInSegsVsSegMarksStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:F-F'] = '''
Correlated?:Are the values of track1 and track2 more [tail:Alternative hypothesis=more:positively/less:negatively/different:] correlated than expected by chance?
    [H0:_=Function values of the two tracks are uncorrelated]
    [H1_more:_=Function values of the two tracks are positively correlated]
    [H1_less:_=Function values of the two tracks are negatively correlated]
    [H1_different:_=Function values of the two tracks are correlated]]
    [assumptions:_Null model=
#        preserveBoth:Preserve both function tracks (T1 & T2) as they are/
        summarize:Preserve both function tracks (T1 & T2), but reduce the information content by summarizing over sub bins]
    [method:_Correlation method=pearson:Pearson/spearman:Spearman/kendall:Kendall]
    [numSubBins:_Number of sub bins used to summarize function values (if needed)=10/100/1000:1 000/10000:10 000/100000:100 000/1000000:1 000 000/10000000:10 000 000]
    [summarizeFunction:_Summarize function values in each sub bin by (if needed)=mean:Mean value]
    -> SimpleFunctionCorrelationPvalStat, FunctionCorrelationPvalStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:VS-S'] = '''
Preferential overlap?:
    Are the segments of track 1 marked as case overlapping unexpectedly [tail:Alternative hypothesis=more:more/less:less/different:differently] with the segments of track 2 than the segments of track 1 valued as control?
#    [H0:_=The segments of track 1 are located independently of the segments of track 2 with respect to overlap]
#    [H1_more:_=The segments of track 1 tend to overlap the segments of track 2]
#    [H1_less:_=The segments of track 1 tend to avoid overlapping the segments of track 2]
#    [H1_different:_=The locations of the segments of track 1 are dependent on the locations of the segments of track 2 with respect to overlap]
    [assumptions:_Null model=
    ShuffledMarksTrack_:Preserve segments of both tracks; randomize values of T1-segments]
    $MCFDR$
    $RANDSEED$
#    [illustrationFn:=S_S_Overlap.png:]
    [rawStatistic:=CaseVsControlOverlapDifferenceStat:]
    -> RandomizationManagerStat
'''

RAW_ANALYSIS_SPECS['Hypothesis testing:SF-S'] = '''
Higher values in segments?:
    Are the values of track 1 that falls inside segments of track 2 [tail:Alternative hypothesis=more:higher/less:lower/different:different] than expected by chance?
    [method:_Aggregate method=sum_of_sum:Sum of bp values for each segment, summed over each region/
     sum_of_mean:Mean of bp values for each segment, summed over each region/
     mean_of_mean:Mean of bp values for each segment, averaged over the regions/
     diff_of_mean:Difference of mean of bp values for each segment, inside versus outside the regions]
    [assumptions:_Null model=ShuffledMarksTrack_:Preserve segments (T2) and step lengths (T1); randomize values (T1)/
    _PermutedSegsAndSampledIntersegsTrack:Preserve step lengths and values (T1) and segment lengths of T2; randomize positions (T2) (MC)/
    _PermutedSegsAndIntersegsTrack:Preserve step lengths and values (T1), segment lengths and inter-segment gaps (T2); randomize positions (T2) (MC)]
    $EXPERIMENTAL$
    $MCFDR$
    $RANDSEED$
    [rawStatistic:=AggregateOfStepFunctionBpsVsSegmentsStat:]
    -> RandomizationManagerStat

#Higher values in segments?:
#    Are the values of track 1 in segments of track 2 [tail:Alternative hypothesis=more:higher/less:lower/different:different] than expected by chance?
##    [H0:_=The segments of track 1 are located independently of the segments of track 2 with respect to overlap]
##    [H1_more:_=The segments of track 1 tend to overlap the segments of track 2]
##    [H1_less:_=The segments of track 1 tend to avoid overlapping the segments of track 2]
##    [H1_different:_=The locations of the segments of track 1 are dependent on the locations of the segments of track 2 with respect to overlap]
#    [assumptions:_Null model=ShuffledMarksTrack_:Preserve segments (T2) and step lengths (T1); randomize values (T1)]
#    $MCFDR$
#    $RANDSEED$
##    [illustrationFn:=S_S_Overlap.png:]
#    [rawStatistic:=SumOfStepFunctionBpsInSegmentsStat:]
#    -> RandomizationManagerStat


'''

RAW_ANALYSIS_SPECS['Hypothesis testing:P'] = '''
#Frequency change?:
#    Is the absolute frequency change between bin halves (ratio) larger than expected by chance?
#    [rawStatistic:=FreqChangeRatioStat:]
#    [assumptions:_Null model=RandomGenomeLocationTrack_:Segments fetched from random genome location (MC)/
#    PermutedSegsAndSampledIntersegsTrack_:Permuted segments, sampled spaces for track (MC)]
#    [tails:=two-tail:]
#    -> RandomizationManagerStat
#Located nonuniformly inside bin?:
#   Do the points of track 1 tend to accumulate
#   [tails=less/more]
#   at the upstream end of the bin?
#   [rawStatistic:=FreqChangeRatioStat:]
#   [assumptions:_Null model=RandomGenomeLocationTrack_:Segments fetched from random genome location (MC)/
#   PermutedSegsAndSampledIntersegsTrack_:Preserve segment lengths; randomize positions (MC)]   
#    -> RandomizationManagerStat
#test3?:
#    Is the absolute frequency change between bin halves (ratio) larger than expected by chance?
#    [rawStatistic:=AvgRelPosInBinStat:]
#    [assumptions:_Null model=RandomGenomeLocationTrack_:Segments fetched from random genome location (MC)/
#    PermutedSegsAndSampledIntersegsTrack_:Preserve segment lengths; randomize positions  (MC)]
#    [tails:=two-tail:]
#    -> RandomizationManagerStat

Located nonuniformly in bin (MC)?:
 Do the points of track 1 tend to accumulate [tails=left-tail/right-tail] at the upstream end of the bin
 [assumptions:_Null model=PermutedSegsAndIntersegsTrack_:Preserve segment lengths and inter-segment gaps; randomize positions (MC)]
 [rawStatistic:=AvgRelPosInBinStat:]
 $MCFDR$
 $RANDSEED$
 $EXPERIMENTAL$
 -> RandomizationManagerStat
 
Preferentially located in bin?:
 Do the points of track 1 tend to accumulate [tail:Alternative hypothesis=more:more/less:less/different:differently] than expected in given bins?
 [globalSource:_Normalize against=chrs:Whole genome (all chromosomes)/chrarms:Genome excl centromere (all chr arms)/ensembl:Genes (All Ensembl gene regions)/userbins:Analysis domain (Union of analysis bins)]
 $EXPERIMENTAL$
 -> BinPreferencePValStat


#    Do the points of track 1 tend to accumulate 
#    [tails=less/more]
##[H0:_=The points of track 1 have a uniform distribution within the segments of track 2]
##[H1_ha1:_=The points of track 1 tend to be positioned towards the borders of the segments of track 2]
##[H1_ha2:_=The points of track 1 tend to be positioned towards the middle of the segments of track 2]
##[H1_ha3:_=The points of track 1 tend to be positioned towards the upstream side of the segments of track 2]
##[H1_ha4:_=The points of track 1 tend to be positioned towards the downstream side of the segments of track 2]
##[H1_ha5:_=The points of track 1 are unequally distributed within segments of track 2]
#    at the upstream end of the bin
#    [assumptions:_Null model=
#        PermutedSegsAndIntersegsTrack_:Preserve segments (T2) and inter-point distances (T1); randomize positions (MC)/
#    [rawStatistic:=AvgRelPosInBinStat:]
##    -> PointPositioningPValStat
#     -> RandomizationManagerStat

Located nonuniformly in bin (analytic)?:
    Do the points of track 1 tend to accumulate
    [tail:Alternative hypothesis=ha1:towards the borders/ha2:towards the middle/ha3:towards the upstream side/ha4:towards the downstream side/less] of the segments of track 2?
#    [tail=less/more]
    [H0:_=The points of track 1 have a uniform distribution within the bin]
#    [H1_less:_=The points of track 1 tend to be positioned towards the upstream side of the bin]
#    [H1_more:_=The points of track 1 tend to be positioned towards the downstream side of the bin]     
    [H1_ha1:_=The points of track 1 tend to be positioned towards the borders of the bin]
    [H1_ha2:_=The points of track 1 tend to be positioned towards the middle of the bin]
    [H1_ha3:_=The points of track 1 tend to be positioned towards the upstream side of the bin]
    [H1_ha4:_=The points of track 1 tend to be positioned towards the downstream side of the bin]
    [H1_ha5:_=The points of track 1 are unequally distributed within bin]
    [assumptions:_Null model=independentPoints:Preserve segments (T2) and number of points (T1); randomize positions (T1)]
    $EXPERIMENTAL$
#    [assumptions:_Null model=
#        independentPoints:Preserve segments (T2) and number of points (T1), randomize positions (T1)/
#        PermutedSegsAndIntersegsTrack_:Preserve segments (T2) and inter-point distances (T1); randomize positions (T1) (MC)/
#        _PermutedSegsAndIntersegsTrack:Preserve points (T1), segment lengths and inter-segment gaps (T2); randomize positions (T2) (MC)]
#    [rawStatistic:=AvgRelPointPositioningStat:]
#    -> PointPositioningPValStat,RandomizationManagerStat
    ->  OneTrackPointPositioningPValStat
'''

RAW_ANALYSIS_SPECS['Descriptive statistics:Basic'] = '''
#Plain results..
#Overview of segment properties: Counts, coverage and average length of segments
#    [rawStatistics:=CountElementStat|ProportionCountStat|AvgSegLenStat:]
#    -> GenericResultsCombinerStat
Overview of segment properties: Counts, coverage and average length of segments
    -> SegmentOverviewWithoutOverlapStat

Precision, recall...: Precision, recall, Hamming distance and Pearsons correlation coefficient of base pair coverage when viewing track1 as predictions and track2 as answer -> AccuracyStat
Similar segments: For all track1-segments, the number of similar segments in track2 [minRelSimilarity:_Relative similarity threshold=1.0/0.99/0.95/0.9/0.8/0.7/0.6/0.5/0.25/0.1] -> SimilarSegmentStat
#Corresponding segments: The count of corresponding segments between track1 and track2 [maxAbsDifference:_Max bp difference=0/2/5/10/20/50][maxRelDifference:_Max relative difference=0.01/0.05/0.1/0.5/1] -> SimilarSegmentStat
Count inside/outside: The number and proportion of track1-points inside and outside track2-segments -> PropPointCountsVsSegsStat
Count inside/outside (allowing overlaps): The number and proportion of track1-points (allowing overlaps) inside and outside track2-segments -> PropPointCountsAllowOverlapsVsSegsStat
Matrix of count inside: What is the number of track1-points inside track2-segments, for all combination of categories from both tracks -> CategoryPointCountInSegsMatrixStat
#Matrix of count inside (GK): What is the number of track1-points inside track2-segments, for all combination of categories from both tracks [rawStatistic:=PointCountInsideSegsStat:] -> CategoryMatrixStat
SequenceLevelOverlap: Dummy -> SequenceLevelOverlapStat
MarksSortedNucleotideLevelSegmentsStat: Dummy -> MarksSortedNucleotideLevelSegmentsStat
MarksSortedSequenceLevelSegmentsStat: Dummy -> MarksSortedSequenceLevelSegmentsStat
Mean: The mean value of track1 -> MeanStat
Sum: The sum of values of track1 -> SumStat
Mean inside and outside: The mean value of track2 inside track1 and outside track1 -> MeanInsideOutsideStat
Counts: The number of track1-points -> CountPointStat
TestLocalCountsCollection: only a test $EXPERIMENTAL$ [rawStatistic:_=CountPointStat] -> LocalResultsCollectionStat
Counts: The number of track1-points and the number of track2-points -> CountPointBothTracksStat
Counts (allowing overlaps): The number of track1-points (allowing overlaps)-> CountPointAllowingOverlapStat
#Category counts: The number of elements of each category of track1 [rawStatistic:=CountPointStat:]-> GeneralOneCatTrackJoinWithDictSumStat
#Category point counts: The number of points from each category of track1 (segments not correctly supported, overlapping points counted once) -> CategoryPointCountNoOverlapsStat
Frequency: The frequency of track1-points -> PointFreqStat
Relative avg position: The relative average position of track1-points inside the bins -> AvgRelPosInBinStat
Strands in bin: The Strand type of track1 inside the bins -> StrandsInsideBinStat
#(per bp)?
Coverage: Base pair and proportional coverage by track1, track2 and by both -> ProportionOverlapStat
#Category bp coverage: Bp coverage by track1, track2 and both, for each category of track1 [rawStatistic:=ProportionOverlapStat:]-> GeneralOneCatTrackJoinWithDoubleDictSumStat
Combined aggregates per bin: A custom operation on aggregate bin values on each track  $EXPERIMENTAL$ [rawStatisticTrack1=MaxOfMarksStat] [rawStatisticTrack2=MaxOfMarksStat] [combineOperation=product] -> ResultPerTrackCombinerStat
Enrichment: The enrichment of track1 inside track2 and vice versa, at bp level-> DerivedOverlapStat
#Category enrichment: Enrichment of track1 inside track2 and vice versa, at bp level, for each category of track1 [rawStatistic:=DerivedOverlapStat:]-> GeneralOneCatTrackStat
#Data inspection: Enrichment of track1-points inside track2 and vice versa, at bp level-> DerivedPointCountsVsSegsStat
Variance: The variance of values of track1 -> VarianceStat
Inside vs outside: The mean difference between values of track2 inside track1 versus outside track1 -> DiffOfMeanInsideOutsideStat
Std. dev: The standard deviation of values of track1 -> StdDevStat
Bp coverage: The number of base pairs covered by track1 -> CountSegmentStat
Proportional coverage: The proportion of total base pairs covered by track1 -> ProportionCountStat
Avg segment length: The average length of segments of track1 [withOverlaps:_Overlap handling=no:Cluster overlaps/yes:Allow overlaps] -> AvgSegLenStat
Avg segment distance: The average distance between segments of track1 [withOverlaps:_Overlap handling=no:Cluster overlaps] -> AvgSegDistStat
#Category bp coverage: The number of base pairs covered by each category of track1 [rawStatistic:=CountSegmentStat:]-> GeneralOneCatTrackJoinWithDictSumStat
Category bp coverage: The number of base pairs covered by each category of track1 -> BpCoverageByCatStat
Category proportional coverage: The proportion of total base pairs covered by each category of track1 -> PropCoverageByCatStat
Category point count: The number of elements each category of track1 (with overlaps) -> FreqByCatStat
Number of categories: The number of distinct categories present in each bin  -> NumberOfPresentCategoriesStat

Min and max: The extremal values (min/max) of track1 -> MinAndMaxStat
ROC-score: ROC-score if track1 are mixture of TP- and FP- segments, and values of track2 are used to rank the track1-segments -> ROCScoreFuncValBasedStat
ROC-score: ROC-score if track1 are mixture of TP- and FP- segments, and overlap with track2 is used to rank the track1-segments -> ROCScoreOverlapBasedStat
CC: Pearson's correlation coefficient of track1 and track2 -> CorrCoefStat
CC: Pearson's correlation coefficient of values for corresponding points in track1 and track2 -> CorrespondingPointMarkCCStat
Mean at points: The mean value of track1 at positions of track2 -> MeanValAtPointsStat
Mean inside: The mean value of track2 inside track1 -> MeanInsideStat
Most common value: The most common track1 value inside a track2 segment -> MostCommonCategoryStat
Most common value in bin: The most common value inside a bin -> MostCommonCategoryInBinStat
#Mean of values (log2): The mean value of values of track1 (log2-scaled) -> MeanMarkStat
#Freq change: The mean change in frequency from half of bin having highest frequency to bin having lowest frequency (ratio) -> FreqChangeRatioStat
#Inside case vs control: The number of  of track1-points that falls inside case/control-track2-segments [rawStatistic:=PointCountInsideSegsStat:] -> GeneralOneTcTrackStat
Overlap case vs control: The numbers and proportions of base pairs overlapping between track1-segments and track2-segments, for case/control-elements of track1, respectively -> DerivedCaseVsControlOverlapDifferenceStat
Counts of case vs control: The number of  of case/control-track1-points [rawStatistic:=CountPointStat:] -> GeneralOneTcTrackStat
Inside case vs control: The number of  of track1-points that falls inside track2-segments marked as case or control [rawStatistic:=PointCountInsideSegsStat:] -> GeneralTrack2TcStat 
Two-by-two table of inside: Two-by-two table of case/control track1-points that falls inside case/control track2-segments [rawStatistic:=PointCountInsideSegsStat:] -> ConfusionMatrixStat
Contingency table of inside: Contingency table of categorical track1-points that falls inside categorical track2-segments [rawStatistic:=PointCountInsideSegsStat:] -> CategoryMatrixStat
# [rawStatistic:=PointCountInsideSegsStat:] for GKs solution in next line:
#Pval Divergence matrix: Pval of divergence matrix of categorical track1-points that falls inside categorical track2-segments [normalizePointsBy:_Normalize points by=rowSum:For each point category, the sum of points inside segments over all segment categories/rowCount:The total number of points for each point category] -> PValOfPointInSegContingencyTableStat
#Case-control of inside: Frequency of case/control-track1-points that falls inside track2-segments [rawStatistic:=PointFreqInsideSegsStat:] -> GeneralOneTcTrackStat
Frequency proportion: The proportion of all points (Track1 and Track2) arising from track1 -> PropFreqOfTr1VsTr2Stat
Relative position within segments: The average relative position of track1-points within track2-segments -> AvgRelPointPositioningStat
Relative coverage per bin: The proportion of track1-segments (counting base pairs) falling within each bin -> PropOfSegmentsInsideEachBinStat
Relative frequency per bin: The proportion of track1-points falling within each bin -> PropOfPointsInsideEachBinStat
Sum of edge weights and 'a' (test): The sum of all edge weights and the extra 'a' column -> ThreeDStat
Two-level overlap: Overlap preference at the low- and high-resolution level $EXPERIMENTAL$ -> TwoLevelOverlapPreferenceStat
Number of total nodes and weighted nodes: The number of total nodes and weighted nodes -> MeasureGraphDensity3dStat

Relative proportional coverage: proportion of base pairs covered by track1, relative to global proportional coverage [rawStatistic:_=ProportionCountStat]
 [globalSource:_Normalize against=chrs:Whole genome (all chromosomes)/chrarms:Genome excl centromere (all chr arms)/ensembl:Genes (All Ensembl gene regions)/userbins:Analysis domain (Union of analysis bins)]  -> GenericRelativeToGlobalStat
#Bin size:Number of base pairs in analysis region $EXPERIMENTAL$ -> BinSizeStat
Three-way overlap: The observed overlap between subsets of three tracks $EXPERIMENTAL$
    [assumptions:_Null model=SegsSampledByIntensityTrack_:Preserve function (T2) and number of points (T1), randomize positions by intensity (MC)]
    -> ThreeWayBpOverlapStat
Three-way overlap under preservations: The expected overlap between three tracks under different sets of preserved relations $EXPERIMENTAL$
    [assumptions:_Null model=SegsSampledByIntensityTrack_:Preserve function (T2) and number of points (T1), randomize positions by intensity (MC)]
    -> ThreeWayExpectedWithEachPreserveCombinationBpOverlapStat
Three-way overlap factors under preservations: The expected overlap between three tracks under different sets of preserved relations $EXPERIMENTAL$
    [assumptions:_Null model=SegsSampledByIntensityTrack_:Preserve function (T2) and number of points (T1), randomize positions by intensity (MC)]
    [rawStatistic:=ThreeWayExpectedWithEachPreserveCombinationBpOverlapStat:]
    [referenceResDictKey:=preserveNone:]
    -> GenericFactorsAgainstReferenceResDictKeyStat
Three-way track inclusions: Overview of tracks whose coverage is a subset of (included in) that of other (combinations of) tracks $EXPERIMENTAL$
    [assumptions:_Null model=SegsSampledByIntensityTrack_:Preserve function (T2) and number of points (T1), randomize positions by intensity (MC)]
    -> ThreeWayTrackInclusionBpOverlapStat
Three-way expected overlap: The observed and expected overlap between subsets of three tracks $EXPERIMENTAL$, with bin preference given or not (null model is not relevant, only there to get in third track as intensity)
    [assumptions:_Null model=SegsSampledByIntensityTrack_:Preserve function (T2) and number of points (T1), randomize positions by intensity (MC)]     
     [rawStatistics:=ThreeWayBpOverlapStat|ThreeWayExpectedBpOverlapStat|ThreeWayExpectedBpOverlapGivenBinPresenceStat:]
    -> GenericResultsCombinerStat
Bin size: The number of bps per bin (and count of selected track as bi-product) $EXPERIMENTAL$ [rawStatistics:=BinSizeStat|CountStat:]-> GenericResultsCombinerStat
CombinationTest: combining
 [rawStatistics=RawOverlapStat|AccuracyStat]
 $EXPERIMENTAL$
 -> GenericResultsCombinerStat

Neighborhood correspondence along sequence: The correspondence between neighborhoods between consecutive nodes of track1 along the sequence
 [globalSource:_Full graph of possible neighborhood=chrs:Whole genome (all chromosomes)/chrarms:Genome excl centromere (all chr arms)/userbins:Analysis domain (Union of analysis bins)]
 $EXPERIMENTAL$
 [weightThreshold:Weight threshold=0/1/5/10/50/100]
 -> NeighborhoodOverlap3dStat
 
DiffRelCoverageStat: DiffRelCoverageStat... $EXPERIMENTAL$ $GLOBAL_SOURCE$ -> DiffRelCoverageStat
-> ComputeROCScoreFromRankedTargetControlMarksStat
-> ZipperStat
-> RawDataStat
-> SingleValExtractorStat
-> TpPointReshuffledStat
-> RandomizationManagerStat
-> TpPointInSegStat
-> SumInsideStat
-> TpReshuffledStat
-> ListCollapserStat
-> LogSumSegDistStat
-> TpRawOverlapStat
-> SumOfSquaresStat
-> CustomRStat
-> MarksSortedBySegmentOverlapStat
-> MarksSortedByFunctionValueStat
-> BasicCustomRStat
-> PointPositionsInSegsStat

Number of nodes and edges: The number of nodes and edges in track1 -> NumberOfNodesAndEdges3dStat
'''

RAW_ANALYSIS_SPECS['Descriptive statistics:Distributions'] = '''
#Distributions as result
Segment lengths: The distribution of lengths of each track1-segment [withOverlaps:_Overlap handling=no:Cluster overlaps/yes:Allow overlaps] -> SegmentLengthsStat
Segment distances: The distribution of distances between segments of track1 [withOverlaps:_Overlap handling=no:Cluster overlaps/yes:Allow overlaps] -> SegmentDistancesStat
Segment distances: The distribution of distances from each track1-segment to nearest track2-segment [withOverlaps:_Overlap handling=no:Cluster overlaps of track 1/yes:Allow overlaps of track 1] -> NearestSegmentDistsStat
Point to segment distances: The distribution of distances from each track1-point to nearest track2-segment -> NearestSegmentFromPointDistsStat
Point distances: The distribution of distances from each track1-point to nearest track2-point -> NearestPointDistsStat
Values: The distribution of values of track1-elements [withOverlaps:_Overlap handling=no:Cluster overlaps/yes:Allow overlaps] -> MarksListStat
Values inside: The distribution of values of track1-elements inside track2-elements -> ExtractMarksStat
Category distribution: The distribution of the number of element from each category of track1 -> FreqPerCatDistributionStat
Relative positions: The distribution of relative positions of points inside bins -> RelPositionsInBinStat
#Smoothed values: Point values smoothed by gaussian window also including neighbouring point values ([windowSize=21/201/2001/20001], [windowBpSize=5000/10000/25000/50000], [sdOfGaussian=1000/2000/5000/10000/20000], [guaranteeBpCoverByWindow=True], [withOverlaps:_Overlap handling=no:Cluster overlaps/yes:Allow overlaps]) -> SmoothedPointMarksStat
Edge weights: The distribution of weights for each edge of the graph -> EdgeDistributionStat
Number of neighbors: The distribution of number of neighbors for each node in the graph (track1) ->  NumNeighborsDistribution3dStat
Neighborhood correspondence along sequence distribution: The distribution of correspondence between neighborhoods between consecutive nodes of track1 along the sequence
 [globalSource:_Normalize against=chrs:Whole genome (all chromosomes)/chrarms:Genome excl centromere (all chr arms)/userbins:Analysis domain (Union of analysis bins)]
 [weightThreshold:Weight threshold=0/1/5/10/50/100]
 $EXPERIMENTAL$
 -> NeighborhoodCorrespondenceDistribution3dStat
'''

RAW_ANALYSIS_SPECS['Descriptive statistics:Other'] = '''
Scatter plot (F, F): Scatter plot ([track1SummarizerName:Summarizing function for track1 (F)=''' + FUNCTION_SUMMARIZERS + '''], [track2SummarizerName:Summarizing function for track2 (F)=''' + FUNCTION_SUMMARIZERS + '''])  -> DataComparisonStat
Scatter plot (P, F): Scatter plot ([track1SummarizerName:Summarizing function for track1 (P)=''' + POINTS_SUMMARIZERS + '''], [track2SummarizerName:Summarizing function for track2 (F)=''' + FUNCTION_SUMMARIZERS + '''])  -> DataComparisonStat
Scatter plot (F, P): Scatter plot ([track1SummarizerName:Summarizing function for track1 (F)=''' + FUNCTION_SUMMARIZERS+ '''], [track2SummarizerName:Summarizing function for track2 (P)=''' + POINTS_SUMMARIZERS  + '''])  -> DataComparisonStat
Scatter plot (P, P): Scatter plot ([track1SummarizerName:Summarizing function for track1 (P)=''' + POINTS_SUMMARIZERS + '''], [track2SummarizerName:Summarizing function for track2 (P)=''' + POINTS_SUMMARIZERS + '''])  -> DataComparisonStat
Scatter plot (S, S): $EXPERIMENTAL$ Scatter plot ([track1SummarizerName:Summarizing function for track1 (S)=''' + SEGMENTS_SUMMARIZERS + '''], [track2SummarizerName:Summarizing function for track2 (S)=''' + SEGMENTS_SUMMARIZERS + '''])  -> DataComparisonStat
#Scatter plot (track 1 valued): Scatter plot ([track1SummarizerName:Summarizing function for track1=''' + VALUED_POINTS_SUMMARIZERS + '''], [track2SummarizerName:Summarizing function for track2=''' + POINTS_SUMMARIZERS + '''])  -> DataComparisonStat

Bin-scaled distribution (function):Bin-scaled distribution (function) [numSubBins:_Resolution=5/10/20/50/100/200/500/1000/2000/5000] -> BinScaledFunctionAvgStat
Bin-scaled distribution (segments):Bin-scaled distribution (segments) [numSubBins:_Resolution=5/10/20/50/100/200/500/1000/2000/5000] -> BinScaledSegCoverageStat
Bin-scaled distribution (points):Bin-scaled distribution (points) [numSubBins:_Resolution=5/10/20/50/100/200/500/1000/2000/5000] $OVERLAP_HANDLING$ -> BinScaledPointCoverageStat

Plot of segment lengths vs value:Line plot of segment lengths vs mean values over all segments $OVERLAP_HANDLING$ $EXPERIMENTAL$ -> SegmentLengthsVsMeanValuesStat

Clustered heatmap of graph:
    Clustered heatmap of graph on track1
    [complete:_Complete graph=False:No/True:Yes]
    [rowsAsFromNodes:_Use as rows=True:From-nodes/False:To-nodes]
    [normalizationMethod:_Normalization method=
        none:No normalization/
        log:Logarithm ( ln(x) )/
        log+1:Logarithm ( ln(x+1) )/
        p_inverse:Inverse p-value (1-p)/
        p_to_normal_onesided:P-value (one-sided) to normal distribution/
        p_to_normal_twosided:P-value (two-sided) to normal distribution]
    [distMethod:_Row or column dissimilarity measure=
        euclidean:Euclidean distance/
        euclidean_positive:Euclidean distance of positive terms only/
        manhattan:Manhattan distance/manhattan_positive:Manhattan distance of positive terms only/
        minkowski:Cubic distance (Minkowski of power 3)/
        minkowski_positive:Cubic distance of positive terms only (Minkowski of power 3)/
        correlation:Use values, interpreted as correlation (1 - corr)/
        absolutecorrelation:Use absolute values, interpreted as correlation (1 - |corr|)]
    [clustMethod:_Hierarchical clustering method=
        average:Average linkage/
        complete:Complete linkage (max distance)/
        single:Single linkage (min distance)/
        centroid:Centroid linkage/
        ward:Ward\'s minimum-variance method/
        diana:Divisive Analysis Clustering]
    [numClustersRows:_Number of clusters of track 1 to divide results into=1/2/3/5/10/20/30/50/100/200/300/500]
    [numClustersCols:_Number of clusters of track 2 to divide results into=1/2/3/5/10/20/30/50/100/200/300/500]
    [childStat:=GraphAsMatrixStat:]
    -> ClusterMatrixStat
'''

RAW_ANALYSIS_SPECS['Descriptive statistics:Visualization'] = '''
Prototypic visualization: values inside vs outside visualized $EXPERIMENTAL$ -> ValuesInsideVsOutsideVisualizationStat
Raw visualization:raw data, plotted as one line per bin [normalizeRows:_Normalise bins=False:No/True:Yes] [centerRows:_Center bins=False:No/True:Yes] $EXPERIMENTAL$ -> RawVisualizationDataStat
'''


#for category in RAW_ANALYSIS_SPECS.keys():
#    #Put in REPLACE_TEMPLATES
#    RAW_ANALYSIS_SPECS[category] = re.sub('(\$[^$]*\$)', replaceFromTemplate, RAW_ANALYSIS_SPECS[category])
#    assert not '$' in RAW_ANALYSIS_SPECS[category]
#    
#    #ANALYSIS_SPECS[category] = [q for q in RAW_ANALYSIS_SPECS[category].split(os.linesep) if q!='' and q[0]!='#']
#    ANALYSIS_SPECS[category] = []
#    for q in RAW_ANALYSIS_SPECS[category].split(os.linesep):
#        if q=='' or q[0]=='#':
#            continue
#        elif q[0] in [' ','\t']:
#            #appends content to that of preceding line
#            assert len(ANALYSIS_SPECS[category]) > 0
#            ANALYSIS_SPECS[category][-1] += (q.strip())
#        else:
#            #adds new analysisLine
#            ANALYSIS_SPECS[category].append(q)
#    
#    
#    for analysis in ANALYSIS_SPECS[category]:
#        if not '->' in analysis:
#            logMessage('Invalid spec in analysisList.py - found analysis lacking any stat definition: ' + analysis, level=logging.ERROR)


#@runtimeLogging
def processAnalysisSpecs(rawSpecs):
    analysisSpecs = {}
    for category in rawSpecs.keys():
        #Put in REPLACE_TEMPLATES
        #print 'BEFORE: ',rawSpecs[category]
        #rawSpecs[category] = re.sub('(\$[^$]*\$)', replaceFromTemplate, rawSpecs[category])
        #assert not '$' in rawSpecs[category]
        #print 'AFTER: ',rawSpecs[category]
        #analysisSpecs[category] = [q for q in rawSpecs[category].split(os.linesep) if q!='' and q[0]!='#']
        analysisSpecs[category] = []
        for q in rawSpecs[category].split(os.linesep):
            if q=='' or q[0]=='#':
                continue

            q = re.sub('(\$[^$]*\$)', replaceFromTemplate, q).replace(os.linesep,'')
            
            if q[0] in [' ','\t']:
                #appends content to that of preceding line
                assert len(analysisSpecs[category]) > 0, 'category: '+category
                analysisSpecs[category][-1] += (q.strip())
            else:
                #adds new analysisLine
                analysisSpecs[category].append(q)
        
        
        for analysis in analysisSpecs[category]:
            if not '->' in analysis:
                logMessage('Invalid spec in analysisList.py - found analysis lacking any stat definition: ' + analysis, level=logging.ERROR)
    return analysisSpecs

ANALYSIS_SPECS = processAnalysisSpecs(RAW_ANALYSIS_SPECS)

#Where in the genome are genes closer to (..) repeats than expected if they were unrelated?: LogSumDistReshuffledStat
#
#Where in the genome is the number of genes larger than the number of repeats, taking into account their frequencies?
#and repeats different from expected if they were from the same density?

#Where are the points of Track 1 differently frequent than the points in Track 2, taking into account the different number of points present in each track? 
#Where are the points of Track 1 [differently/more/less] [Type of frequency = Relative:relatively/absolutely] frequent than the points in Track 2, taking into account the different number of points present in each track?
#Where are the points of Track 1 [different:of a different frequency/more:more frequent/less:less frequent] than the points in Track 2, taking into account the different number of points present in each track?
#Where are the points of Track 1 [Alternative hypotheses=different:of a different frequency/more:more frequent/less:less frequent] than the points in Track 2, taking into account the different number of points present in each track?
#Where in the genome are track1 closer to (..) track2 than expected if they were unrelated?: LogSumDistReshuffledStat
#Where in the genome are track1 further apart from track2 than expected by chance?: LogSumDistReshuffledStat
#
#Where in the genome is the frequencies of track1 and track2 different from expected if they were from the same density?

