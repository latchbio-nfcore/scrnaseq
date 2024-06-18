
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'barcode_whitelist': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Mandatory arguments',
        description='If not using the 10X Genomics platform, a custom barcode whitelist can be used with `--barcode_whitelist`.',
    ),
    'aligner': NextflowParameter(
        type=typing.Optional[str],
        default='alevin',
        section_title=None,
        description='Name of the tool to use for scRNA (pseudo-) alignment.',
    ),
    'protocol': NextflowParameter(
        type=typing.Optional[str],
        default='auto',
        section_title=None,
        description="The protocol that was used to generate the single cell data, e.g. 10x Genomics v2 Chemistry.\n\n Can be 'auto' (cellranger only), '10XV1', '10XV2', '10XV3', or any other protocol string that will get directly passed the respective aligner.",
    ),
    'skip_multiqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Skip Tools',
        description='Skip MultiQC Report',
    ),
    'skip_fastqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip FastQC',
    ),
    'skip_emptydrops': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip custom empty drops filter module',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'transcript_fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='A cDNA FASTA file',
    ),
    'gtf': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Reference GTF annotation file',
    ),
    'save_reference': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify this parameter to save the indices created (STAR, Kallisto, Salmon) to the results.',
    ),
    'salmon_index': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Alevin Options',
        description='This can be used to specify a precomputed Salmon index in the pipeline, in order to skip the generation of required indices by Salmon itself.',
    ),
    'txp2gene': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to transcript to gene mapping file. This allows the specification of a transcript to gene mapping file for Salmon Alevin and AlevinQC.',
    ),
    'simpleaf_rlen': NextflowParameter(
        type=typing.Optional[int],
        default=91,
        section_title=None,
        description='It is the target read length the index will be built for, using simpleaf.',
    ),
    'star_index': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='STARSolo Options',
        description='Specify a path to the precomputed STAR index.',
    ),
    'star_ignore_sjdbgtf': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Ignore the SJDB GTF file.',
    ),
    'seq_center': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Name of sequencing center for BAM read group tag.',
    ),
    'star_feature': NextflowParameter(
        type=typing.Optional[str],
        default='Gene',
        section_title=None,
        description='Quantification type of different transcriptomic feature. Use `GeneFull` on pre-mRNA count for single-nucleus RNA-seq reads. Use `Gene Velocyto` to generate RNA velocity matrix.',
    ),
    'kallisto_index': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Kallisto/BUS Options',
        description='Specify a path to the precomputed Kallisto index.',
    ),
    'kb_t1c': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Specify a path to the cDNA transcripts-to-capture.',
    ),
    'kb_t2c': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Specify a path to the intron transcripts-to-capture.',
    ),
    'kb_workflow': NextflowParameter(
        type=typing.Optional[str],
        default='standard',
        section_title=None,
        description='Type of workflow. Use `nac` for an index type that can quantify nascent and mature RNA. Use `lamanno` for RNA velocity based on La Manno et al. 2018 logic. (default: standard)',
    ),
    'kb_filter': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Activate Kallisto/BUStools filtering algorithm',
    ),
    'cellranger_index': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Cellranger Options',
        description='Specify a pre-calculated cellranger index. Readily prepared indexes can be obtained from the 10x Genomics website. ',
    ),
    'motifs': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Cellranger ARC Options',
        description='Specify a motif file to create a cellranger-arc index. Can be taken, e.g., from the JASPAR database.',
    ),
    'cellrangerarc_config': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specify a config file to create the cellranger-arc index.',
    ),
    'cellrangerarc_reference': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specify the genome reference name used in the config file to create a cellranger-arc index.',
    ),
    'universc_index': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='UniverSC Options',
        description='Specify a pre-calculated cellranger index. Readily prepared indexes can be obtained from the 10x Genomics website.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

