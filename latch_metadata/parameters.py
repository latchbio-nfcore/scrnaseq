import typing
from dataclasses import dataclass
from enum import Enum

import typing_extensions
from flytekit.core.annotation import FlyteAnnotation
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import NextflowParameter


# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters
class Aligner(Enum):
    star = "star"
    alevin = "alevin"
    kallisto = "kallisto"
    cellranger = "cellranger"
    cellranger_arc = "cellrangerarc"
    UniverSC = "universc"


class STAR_options(Enum):
    gene = "Gene"
    gene_full = "GeneFull"
    gene_vel = "Gene Velocyto"


generated_parameters = {
    "input": NextflowParameter(
        type=LatchFile,
        default=None,
        section_title=None,
        display_name="Sample Sheet",
        description="Path to comma-separated file containing information about the samples in the experiment.",
    ),
    "outdir": NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({"output": True})],
        default=None,
        section_title=None,
        display_name="Output Directory",
        description="The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.",
    ),
    "email": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        display_name="email",
        description="Email address for completion summary.",
    ),
    "multiqc_title": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        display_name="Multi QC Header",
        description="MultiQC report title. Printed as page header, used for filename if not otherwise specified.",
    ),
    "barcode_whitelist": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="Barcode Whitelist",
        description="If not using the 10X Genomics platform, a custom barcode whitelist can be used with `--barcode_whitelist`.",
    ),
    "aligner": NextflowParameter(
        type=Aligner,
        default=Aligner.alevin,
        section_title=None,
        display_name="Aligner",
        description="Name of the tool to use for scRNA (pseudo-) alignment.",
    ),
    "protocol": NextflowParameter(
        type=str,
        section_title=None,
        display_name="Chemistry",
        description="The protocol that was used to generate the single cell data, e.g. 10x Genomics v2 Chemistry.\n\n Can be 'auto' (cellranger only), '10XV1', '10XV2', '10XV3', or any other protocol string that will get directly passed the respective aligner.",
    ),
    "skip_multiqc": NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        display_name="skip multiqc",
        section_title="Skip Tools",
        description="Skip MultiQC Report",
    ),
    "skip_fastqc": NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        display_name="skip fastqc",
        section_title=None,
        description="Skip FastQC",
    ),
    "skip_emptydrops": NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        display_name="skip empty drops filter",
        section_title=None,
        description="Skip custom empty drops filter module",
    ),
    "genome": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title="Reference genome options",
        display_name="iGenome",
        description="Name of iGenomes reference.",
    ),
    "fasta": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="genome fasta",
        description="Path to FASTA genome file.",
    ),
    "transcript_fasta": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="transcript fasta",
        description="A cDNA FASTA file",
    ),
    "gtf": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="GTF file",
        description="Reference GTF annotation file",
    ),
    "save_reference": NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        display_name="save reference index?",
        description="Specify this parameter to save the indices created (STAR, Kallisto, Salmon) to the results.",
    ),
    "salmon_index": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title="Alevin Options",
        display_name="Precomputed salmon index",
        description="This can be used to specify a precomputed Salmon index in the pipeline, in order to skip the generation of required indices by Salmon itself.",
    ),
    "txp2gene": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="transcript to gene map",
        description="Path to transcript to gene mapping file. This allows the specification of a transcript to gene mapping file for Salmon Alevin and AlevinQC.",
    ),
    "simpleaf_rlen": NextflowParameter(
        type=typing.Optional[int],
        default=91,
        section_title=None,
        display_name="target read length",
        description="It is the target read length the index will be built for, using simpleaf.",
    ),
    "star_index": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title="STARSolo Options",
        display_name="precomputed star index",
        description="Specify a path to the precomputed STAR index.",
    ),
    "star_ignore_sjdbgtf": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        display_name="Ignore star sjdbgtf",
        description="Ignore the SJDB GTF file.",
    ),
    "seq_center": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        display_name="sequencing center",
        description="Name of sequencing center for BAM read group tag.",
    ),
    "star_feature": NextflowParameter(
        type=typing.Optional[STAR_options],
        default=STAR_options.gene,
        section_title=None,
        display_name="Star Feature",
        description="Quantification type of different transcriptomic feature. Use `GeneFull` on pre-mRNA count for single-nucleus RNA-seq reads. Use `Gene Velocyto` to generate RNA velocity matrix.",
    ),
    "kallisto_index": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title="Kallisto/BUS Options",
        display_name="Precomputed kallisto index",
        description="Specify a path to the precomputed Kallisto index.",
    ),
    "kb_t1c": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="kb_t1c",
        description="Specify a path to the cDNA transcripts-to-capture.",
    ),
    "kb_t2c": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="kb_t2c",
        description="Specify a path to the intron transcripts-to-capture.",
    ),
    "kb_workflow": NextflowParameter(
        type=typing.Optional[str],
        default="standard",
        section_title=None,
        display_name="kb_workflow",
        description="Type of workflow. Use `nac` for an index type that can quantify nascent and mature RNA. Use `lamanno` for RNA velocity based on La Manno et al. 2018 logic. (default: standard)",
    ),
    "kb_filter": NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        display_name="kb_filter",
        description="Activate Kallisto/BUStools filtering algorithm",
    ),
    "cellranger_index": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title="Cellranger Options",
        display_name="precomputed cellranger index",
        description="Specify a pre-calculated cellranger index. Readily prepared indexes can be obtained from the 10x Genomics website. ",
    ),
    "motifs": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title="Cellranger ARC Options",
        display_name="motif file",
        description="Specify a motif file to create a cellranger-arc index. Can be taken, e.g., from the JASPAR database.",
    ),
    "cellrangerarc_config": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        display_name="contig file",
        description="Specify a config file to create the cellranger-arc index.",
    ),
    "cellrangerarc_reference": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        display_name="reference genome",
        description="Specify the genome reference name used in the config file to create a cellranger-arc index.",
    ),
    "universc_index": NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title="UniverSC Options",
        display_name="precomputed cellranger index",
        description="Specify a pre-calculated cellranger index. Readily prepared indexes can be obtained from the 10x Genomics website.",
    ),
    "multiqc_methods_description": NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        display_name="custom MultiQC yaml file",
        description="Custom MultiQC yaml file containing HTML including a methods description.",
    ),
}
