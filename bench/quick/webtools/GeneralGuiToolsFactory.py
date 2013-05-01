from quick.webtools.Tool1 import Tool1
from quick.webtools.Tool2 import Tool2
from quick.webtools.Tool3 import Tool3
from quick.webtools.Tool4 import Tool4
from quick.webtools.Tool5 import Tool5
from quick.webtools.CreateBenchmarkTool import CreateBenchmarkTool

#from quick.webtools.EivindGLsTool import EivindGLsTool
#from quick.webtools.HiepsTool import HiepsTool
from quick.webtools.create.CreateDnaBasedCustomTrackTool import CreateDnaBasedCustomTrackTool
from quick.webtools.create.CreateSegmentsFromGeneListTool import CreateSegmentsFromGeneListTool
from quick.webtools.create.SmoothedTrackTool import SmoothedTrackTool
from quick.webtools.export.ExtractIntersectingGenesTool import ExtractIntersectingGenesTool
from quick.webtools.InstallUcscTool import InstallUcscTool
from quick.webtools.nmer.NmerAnalyzeTool import NmerAnalyzeTool
from quick.webtools.nmer.NmerExtractTool import NmerExtractTool
from quick.webtools.nmer.NmerInspectTool import NmerInspectTool
from quick.webtools.plot.BinScaledPlotTool import BinScaledPlotTool
from quick.webtools.plot.ScatterPlotTool import ScatterPlotTool
from quick.webtools.tfbs.TfTargetsTool import TfTargetsTool
from quick.webtools.tfbs.GeneRegulatorsTool import GeneRegulatorsTool
from quick.webtools.tfbs.GeneSetRegulatorsTool import GeneSetRegulatorsTool
from quick.webtools.imports.UploadGenomeTool import UploadGenomeTool
from quick.webtools.imports.InstallGenomeTool import InstallGenomeTool
from quick.webtools.cleanup.RemoveGenomeTool import RemoveGenomeTool
from quick.webtools.track.GenomeInfoTool import GenomeInfoTool
from quick.webtools.track.RenameTrackTool import RenameTrackTool
from quick.webtools.regulome.SelectTfTool import SelectTfTool
from quick.webtools.regulome.SelectDiseaseTool import SelectDiseaseTool
from quick.webtools.regulome.CreateRegulomeTool import CreateRegulomeTool
from quick.webtools.restricted.TfMappings import TfMappings
from quick.webtools.restricted.McFdrSimulationTool import McFdrSimulationTool
from quick.webtools.GenerateTool import GenerateTool
from quick.webtools.restricted.GetDiskPathForHistoryElement import GetDiskPathForHistoryElement 
from quick.webtools.gtrack.ComplementTrackElementInformation import ComplementTrackElementInformation 
from quick.webtools.gtrack.ConvertToLinkedValuedSegments import ConvertToLinkedValuedSegments 
from quick.webtools.gtrack.SortGtrackFile import SortGtrackFile 
from quick.webtools.gtrack.BioXSDtoGtrackConverterTool import BioXSDtoGtrackConverterTool 
from quick.webtools.gtrack.ValidateGtrackFile import ValidateGtrackFile 
from quick.webtools.restricted.ListStorebioProjects import ListStorebioProjects 
from quick.webtools.gtrack.TabularToGtrackTool import TabularToGtrackTool 
from quick.webtools.gtrack.ExpandGtrackHeaderTool import ExpandGtrackHeaderTool 
from quick.webtools.restricted.FilterHistoryElementOnCohosenValues import FilterHistoryElementOnCohosenValues 
from quick.webtools.util.StandardizeTrackFilesTool import StandardizeTrackFilesTool 
from quick.webtools.tfbs.FindCooperativeTfsTool import FindCooperativeTfsTool 
from quick.webtools.util.CreateCategoricalTrackTool import CreateCategoricalTrackTool 
from quick.webtools.util.ShowTailOfLogFile import ShowTailOfLogFile 
from quick.webtools.util.McfdrSpecification import McfdrSpecification 
from quick.webtools.restricted.DebugAnalysisTool import DebugAnalysisTool 
from quick.webtools.create.SplitSegmentsTool import SplitSegmentsTool 
from quick.webtools.util.HalfdansTool import HalfdansTool 
from quick.webtools.restricted.DebugAnalysisListTool import DebugAnalysisListTool 
from quick.webtools.restricted.McfdrExplorationTool import McfdrExplorationTool 
from quick.webtools.restricted.UploadDataToStorebio import UploadDataToStorebio 
from quick.webtools.restricted.EditHistoryItem import EditHistoryItem 
from quick.webtools.restricted.CollapseOverlappingCategorySegments import CollapseOverlappingCategorySegments 
from quick.webtools.restricted.DownloadHistoryItems import DownloadHistoryItems 
from quick.webtools.export.AddMetadataToDataset import AddMetadataToDataset 
from quick.webtools.restricted.AddFilesToStorebioinfoDataset import AddFilesToStorebioinfoDataset 
from quick.webtools.restricted.MakeGenomePartionAccordingToSegments import MakeGenomePartionAccordingToSegments 
from quick.webtools.tfbs.GenerateRandomFastaFile import GenerateRandomFastaFile 
from quick.webtools.tfbs.TestOverrepresentationOfPwmInDna import TestOverrepresentationOfPwmInDna 
from quick.webtools.restricted.ConcatenateHistoryItems import ConcatenateHistoryItems 
from quick.webtools.track.ReplaceSegmentsWithBorderPoints import ReplaceSegmentsWithBorderPoints 
from quick.webtools.track.MakePartitionTrackAccordingToBinAndPoints import MakePartitionTrackAccordingToBinAndPoints
from quick.webtools.manipulate.ExpandBedSegmentsTool import ExpandBedSegmentsTool
from quick.webtools.create.CreateFunctionTrackAsDistanceToNearestSegments import CreateFunctionTrackAsDistanceToNearestSegments 
from quick.webtools.restricted.InspectMemmapFile import InspectMemmapFile 
from quick.webtools.restricted.ListSubtrackNames import ListSubtrackNames 
from quick.webtools.track.AnalyzeMultiTrackRelations import AnalyzeMultiTrackRelations 
from quick.webtools.restricted.DebugBatchLine import DebugBatchLine 
from quick.webtools.restricted.ExtractPwms import ExtractPwms 
from quick.webtools.restricted.AssortedSmallTools import AssortedSmallTools 
from quick.webtools.restricted.GenerateCircosImage import GenerateCircosImage 
from quick.webtools.util.BatchRunTool import BatchRunTool 
from quick.webtools.restricted.SigvesTool import SigvesTool 
from quick.webtools.track.ExtractHistoryTrackNames import ExtractHistoryTrackNames 
from quick.webtools.util.AddBatchLineToTestCollection import AddBatchLineToTestCollection 
from quick.webtools.manipulate.FindSegmentNeighbourhoods import FindSegmentNeighbourhoods 
from quick.webtools.util.TouchStandardizedTrack import TouchStandardizedTrack 
from quick.webtools.manipulate.UniversalConverterTool import UniversalConverterTool 
from quick.webtools.tfbs.CreatePwmScoreTracksTool import CreatePwmScoreTracksTool 
from quick.webtools.restricted.TonysTool import TonysTool 
from quick.webtools.restricted.BenchmarkCreationTool import BenchmarkCreationTool 
from quick.webtools.restricted.BenchmarkRetrievalTool import BenchmarkRetrievalTool 
from quick.webtools.restricted.BenchmarkEvaluationTool import BenchmarkEvaluationTool 

class GeneralGuiToolsFactory:
    @staticmethod
    def getWebTool(toolId):
        if toolId == 'hb_generic_1':
            return Tool1()
        elif toolId == 'hb_generic_2':
            #return EivindGLsTool()
            return Tool2()
        elif toolId == 'hb_generic_3':
            return Tool3()
        elif toolId == 'hb_generic_4':
            return Tool4()
        elif toolId == 'hb_generic_5':
            return Tool5()
        elif toolId == 'hb_genelist':
            return CreateSegmentsFromGeneListTool()
        elif toolId == 'hb_create_dna_based':
            return CreateDnaBasedCustomTrackTool()
        elif toolId == 'hb_create_smoothed_track':
            return SmoothedTrackTool()
        elif toolId == 'hb_intersecting_genes':
            return ExtractIntersectingGenesTool()
        elif toolId == 'hb_nmer_analyze':
            return NmerAnalyzeTool()
        elif toolId == 'hb_nmer_extract':
            return NmerExtractTool()
        elif toolId == 'hb_nmer_inspect':
            return NmerInspectTool()
        elif toolId == 'hb_plot_scatter':
            return ScatterPlotTool()
        elif toolId == 'hb_plot_progpattern':
            return BinScaledPlotTool()
        elif toolId == 'hb_tf_reg_gene':
            return GeneRegulatorsTool()
        elif toolId == 'hb_tf_reg_gene_set':
            return GeneSetRegulatorsTool()
        elif toolId == 'hb_tf_gene_targets':
            return TfTargetsTool()
        elif toolId == 'hb_rename_track':
            return RenameTrackTool()
        elif toolId == 'hb_select_tf':
            return SelectTfTool()
        elif toolId == 'hb_select_disease':
            return SelectDiseaseTool()
        elif toolId == 'hb_create_regulome':
            return CreateRegulomeTool()
        elif toolId == 'hb_upload_genome':
            return UploadGenomeTool()
        elif toolId == 'hb_install_genome':
            return InstallGenomeTool()
        elif toolId == 'hb_remove_genome':
            return RemoveGenomeTool()
        elif toolId == 'hb_install_ucsc':
            return InstallUcscTool()            
        elif toolId == 'hb_genome_info':
            return GenomeInfoTool()
        elif toolId == 'hb_tf_mappings':
            return TfMappings()
        elif toolId == 'mc_fdr_simulation_tool':
            return McFdrSimulationTool()
        elif toolId == 'hb_generate_tool':
            return GenerateTool()
            
            
        #
        # hb_nmer_analyze
        # hb_nmer_extract
        # hb_nmer_inspect
        # hb_plot_scatter
        # hb_plot_progpattern
        
        elif toolId == 'hb_get_disk_path_for_history_element':
            return GetDiskPathForHistoryElement()
        elif toolId == 'hb_complement_track_element_information':
            return ComplementTrackElementInformation()
        elif toolId == 'hb_convert_to_linked_valued_segments':
            return ConvertToLinkedValuedSegments()
        elif toolId == 'hb_sort_gtrack_file':
            return SortGtrackFile()
        elif toolId == 'hb_bioxsd_to_gtrack_converter_tool':
            return BioXSDtoGtrackConverterTool()
        elif toolId == 'hb_validate_gtrack_file':
            return ValidateGtrackFile()
        elif toolId == 'hb_list_storebio_projects':
            return ListStorebioProjects()
        elif toolId == 'hb_tabular_to_gtrack_tool':
            return TabularToGtrackTool()
        elif toolId == 'hb_expand_gtrack_header_tool':
            return ExpandGtrackHeaderTool()
        elif toolId == 'hb_filter_history_element_on_cohosen_values':
            return FilterHistoryElementOnCohosenValues()
        elif toolId == 'hb_standardize_track_files_tool':
            return StandardizeTrackFilesTool()
        elif toolId == 'hb_find_cooperative_tfs_tool':
            return FindCooperativeTfsTool()
        elif toolId == 'hb_create_categorical_track_tool':
            return CreateCategoricalTrackTool()
        elif toolId == 'hb_show_tail_of_log_file':
            return ShowTailOfLogFile()
        elif toolId == 'hb_mcfdr_specification':
            return McfdrSpecification()
        elif toolId == 'hb_debug_analysis_tool':
            return DebugAnalysisTool()
        elif toolId == 'hb_split_segments_tool':
            return SplitSegmentsTool()
        elif toolId == 'hb_halfdans_tool':
            return HalfdansTool()
        elif toolId == 'hb_debug_analysis_list_tool':
            return DebugAnalysisListTool()
        elif toolId == 'hb_mcfdr_exploration_tool':
            return McfdrExplorationTool()
        elif toolId == 'hb_upload_data_to_storebio':
            return UploadDataToStorebio()
        elif toolId == 'hb_edit_history_item':
            return EditHistoryItem()
        elif toolId == 'hb_collapse_overlapping_category_segments':
            return CollapseOverlappingCategorySegments()
        elif toolId == 'hb_download_history_items':
            return DownloadHistoryItems()
        elif toolId == 'hb_add_metadata_to_dataset':
            return AddMetadataToDataset()
        elif toolId == 'hb_add_files_to_storebioinfo_dataset':
            return AddFilesToStorebioinfoDataset()
        elif toolId == 'hb_make_genome_partion_according_to_segments':
            return MakeGenomePartionAccordingToSegments()
        elif toolId == 'hb_generate_random_fasta_file':
            return GenerateRandomFastaFile()
        elif toolId == 'hb_test_overrepresentation_of_pwm_in_dna':
            return TestOverrepresentationOfPwmInDna()
        elif toolId == 'hb_concatenate_history_items':
            return ConcatenateHistoryItems()
        elif toolId == 'hb_create_benchmark':
            return BenchmarkTool()
        elif toolId == 'hb_replace_segments_with_border_points':
            return ReplaceSegmentsWithBorderPoints()
        elif toolId == 'hb_make_partition_track_according_to_bin_and_points':
            return MakePartitionTrackAccordingToBinAndPoints()
        elif toolId == 'hb_expandbed':
            return ExpandBedSegmentsTool()
        elif toolId == 'hb_create_function_track_as_distance_to_nearest_segments':
            return CreateFunctionTrackAsDistanceToNearestSegments()
        elif toolId == 'hb_inspect_memmap_file':
            return InspectMemmapFile()
        elif toolId == 'hb_list_subtrack_names':
            return ListSubtrackNames()
        elif toolId == 'hb_analyze_multi-track_relations':
            return AnalyzeMultiTrackRelations()
        elif toolId == 'hb_debug_batch_line':
            return DebugBatchLine()
        elif toolId == 'hb_extract_pwms':
            return ExtractPwms()
        elif toolId == 'hb_assorted_small_tools':
            return AssortedSmallTools()
        elif toolId == 'hb_generate_circos_image':
            return GenerateCircosImage()
        elif toolId == 'hb_batch_run_tool':
            return BatchRunTool()
        elif toolId == 'hb_sigves_tool':
            return SigvesTool()
        elif toolId == 'hb_extract_history_track_names':
            return ExtractHistoryTrackNames()
        elif toolId == 'hb_add_batch_line_to_test_collection':
            return AddBatchLineToTestCollection()
        elif toolId == 'hb_find_segment_neighbourhoods':
            return FindSegmentNeighbourhoods()
        elif toolId == 'hb_touch_standardized_track':
            return TouchStandardizedTrack()
        elif toolId == 'hb_universal_converter_tool':
            return UniversalConverterTool()
        elif toolId == 'hb_create_pwm_score_tracks_tool':
            return CreatePwmScoreTracksTool()
        elif toolId == 'hb_tonys_tool':
            return TonysTool()
        elif toolId == 'hb_benchmark_creation_tool':
            return BenchmarkCreationTool()
        elif toolId == 'hb_benchmark_retrieval_tool':
            return BenchmarkRetrievalTool()
        elif toolId == 'hb_benchmark_evaluation_tool':
            return BenchmarkEvaluationTool()
        else:
            raise Exception('no such prototype: ' + toolId)            
