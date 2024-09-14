from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    Fork,
    ForkBranch,
    LatchRule,
    NextflowParameter,
    Params,
    Section,
    Spoiler,
    Text,
)


class Aligner(Enum):
    star = "star"
    alevin = "alevin"
    kallisto = "kallisto"


class STAR_options(Enum):
    gene = "Gene"
    gene_full = "GeneFull"
    gene_vel = "Gene Velocyto"


class Chemistry(Enum):
    _10xv1 = "10XV1"
    _10xv2 = "10XV2"
    _10xv3 = "10XV3"


class kb_workflow(Enum):
    std = "standard"
    nac = "nac"
    lamanno = "lamanno"


class Reference_Type(Enum):
    hg38 = "Homo sapiens (RefSeq GRCh38)"
    mm10 = "Mus musculus (RefSeq GRCm38)"


@dataclass
class SampleSheet:
    sample: str
    fastq_1: LatchFile
    fastq_2: LatchFile
    expected_cells: Optional[int]
    seq_center: Optional[str]


flow = [
    Section(
        "Input",
        Params("input"),
    ),
    Section(
        "Reference Genome Options",
        Fork(
            "genome_source",
            "",
            latch_genome_source=ForkBranch(
                "Latch Certified Reference Genome",
                Params("latch_genome"),
            ),
            input_ref=ForkBranch(
                "Custom Reference Genome",
                Params("fasta", "gtf", "save_reference"),
                # Text(
                #     "The transcriptome and GTF files in iGenomes are vastly out of date with respect to current annotations from Ensembl e.g. human iGenomes annotations are from Ensembl release 75, while the current Ensembl release is 108. Please consider downloading and using a more updated version of your reference genome."
                # ),
                # Params("genome"),
            ),
        ),
    ),
    Section(
        "Aligners",
        Params("aligner"),
        Params("protocol"),
        Params("barcode_whitelist"),
        Spoiler(
            "Aligner Options",
            Fork(
                "Aligner_options",
                "",
                alevin_frk=ForkBranch(
                    "Alevin", Params("salmon_index", "txp2gene", "simpleaf_rlen")
                ),
                kallisto_frk=ForkBranch(
                    "Kallisto/Bustools",
                    Params(
                        "kallisto_index", "kb_t1c", "kb_t2c", "kb_workflow", "kb_filter"
                    ),
                ),
                star_frk=ForkBranch(
                    "Star", Params("star_index", "star_ignore_sjdbgtf", "star_feature")
                ),
            ),
        ),
    ),
    Section(
        "Output Directory",
        Params("run_name"),
        Text("Parent directory for outputs"),
        Params("outdir"),
    ),
    Spoiler(
        "Optional Arguments",
        Text("Additional optional Arguments"),
        Section(
            "Multi QC",
            Params("multiqc_title", "multiqc_methods_description"),
        ),
        Section(
            "Skip Tools",
            Params("skip_fastqc"),
        ),
    ),
]


generated_parameters = {
    "input": NextflowParameter(
        type=List[SampleSheet],
        display_name="Samplesheet",
        description="Information about the samples in the experiment",
        section_title=None,
        samplesheet_type="csv",
        samplesheet=True,
    ),
    "outdir": NextflowParameter(
        type=LatchOutputDir,
        default=None,
        section_title=None,
        display_name="Output Directory",
        description="The output directory where the results will be saved.",
    ),
    "run_name": NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        display_name="Run name",
        description="Name of Run",
        rules=[
            LatchRule(
                regex=r"^[a-zA-Z0-9_-]+$",
                message="Run name must contain only letters, digits, underscores, and dashes. No spaces are allowed.",
            )
        ],
    ),
    "email": NextflowParameter(
        type=Optional[str],
        default=None,
        section_title=None,
        display_name="email",
        description="Email address for completion summary.",
    ),
    "multiqc_title": NextflowParameter(
        type=Optional[str],
        default=None,
        section_title=None,
        display_name="Multi QC Header",
        description="MultiQC report title. Printed as page header, used for filename if not otherwise specified.",
    ),
    "barcode_whitelist": NextflowParameter(
        type=Optional[LatchFile],
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
        type=Chemistry,
        section_title=None,
        display_name="Chemistry",
        description="The protocol that was used to generate the single cell data, e.g. 10x Genomics v2 Chemistry.\n\n Can be '10XV1', '10XV2', '10XV3'.",
    ),
    "skip_multiqc": NextflowParameter(
        type=bool,
        default=None,
        display_name="Skip MultiQC",
        description="Skip MultiQC Report",
    ),
    "skip_fastqc": NextflowParameter(
        type=bool,
        default=None,
        display_name="Skip FastQC",
        section_title=None,
        description="Skip FastQC",
    ),
    "skip_emptydrops": NextflowParameter(
        type=bool,
        default=True,
        display_name="skip empty drops filter",
        section_title=None,
        description="Skip custom empty drops filter module",
    ),
    "genome_source": NextflowParameter(
        type=str,
        display_name="Reference Genome",
        description="Choose Reference Genome",
    ),
    "latch_genome": NextflowParameter(
        type=Reference_Type,
        display_name="Latch Verfied Reference Genome",
        description="Name of Latch Verfied Reference Genome.",
        default=Reference_Type.hg38,
    ),
    "fasta": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="genome fasta",
        description="Path to FASTA genome file.",
    ),
    "transcript_fasta": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="transcript fasta",
        description="A cDNA FASTA file",
    ),
    "gtf": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="GTF file",
        description="Reference GTF annotation file",
    ),
    "save_reference": NextflowParameter(
        type=bool,
        default=False,
        section_title=None,
        display_name="Save Reference",
        description="Specify this parameter to save the indices created (STAR, Kallisto, Salmon) to the results.",
    ),
    "salmon_index": NextflowParameter(
        type=Optional[LatchDir],
        default=None,
        section_title="Alevin Options",
        display_name="Precomputed Salmon Index",
        description="This can be used to specify a precomputed Salmon index in the pipeline, in order to skip the generation of required indices by Salmon itself.",
    ),
    "txp2gene": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="Transcript to Gene Mapping File",
        description="Path to transcript to gene mapping file. This allows the specification of a transcript to gene mapping file for Salmon Alevin and AlevinQC.",
    ),
    "simpleaf_rlen": NextflowParameter(
        type=Optional[int],
        default=91,
        section_title=None,
        display_name="Target Read Length",
        description="It is the target read length the index will be built for, using simpleaf.",
    ),
    "star_index": NextflowParameter(
        type=Optional[LatchDir],
        default=None,
        section_title="STARSolo Options",
        display_name="Precomputed STAR Index",
        description="Specify a path to the precomputed STAR index.",
    ),
    "star_ignore_sjdbgtf": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="Ignore STAR SJDB GTF file",
        description="Ignore the SJDB GTF file.",
    ),
    "seq_center": NextflowParameter(
        type=Optional[str],
        default=None,
        section_title=None,
        display_name="sequencing center",
        description="Name of sequencing center for BAM read group tag.",
    ),
    "star_feature": NextflowParameter(
        type=Optional[STAR_options],
        default=STAR_options.gene,
        section_title=None,
        display_name="STAR Feature",
        description="Quantification type of different transcriptomic feature. Use `GeneFull` on pre-mRNA count for single-nucleus RNA-seq reads. Use `Gene Velocyto` to generate RNA velocity matrix.",
    ),
    "kallisto_index": NextflowParameter(
        type=Optional[LatchDir],
        default=None,
        section_title="Kallisto/BUS Options",
        display_name="Precomputed Kallisto Index",
        description="Specify a path to the precomputed Kallisto index.",
    ),
    "kb_t1c": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="cDNA transcripts-to-capture File",
        description="Specify a path to the cDNA transcripts-to-capture.",
    ),
    "kb_t2c": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="Intron transcripts-to-capture File",
        description="Specify a path to the intron transcripts-to-capture.",
    ),
    "kb_workflow": NextflowParameter(
        type=Optional[kb_workflow],
        default=kb_workflow.std,
        section_title=None,
        display_name="Workflow Type",
        description="Type of workflow. Use `nac` for an index type that can quantify nascent and mature RNA. Use `lamanno` for RNA velocity based on La Manno et al. 2018 logic. (default: standard)",
    ),
    "kb_filter": NextflowParameter(
        type=bool,
        default=None,
        section_title=None,
        display_name="Activate Kallisto/BUStools Filtering Algorithm",
        description="Activate Kallisto/BUStools filtering algorithm",
    ),
    "cellranger_index": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title="Cellranger Options",
        display_name="precomputed cellranger index",
        description="Specify a pre-calculated cellranger index. Readily prepared indexes can be obtained from the 10x Genomics website. ",
    ),
    "motifs": NextflowParameter(
        type=Optional[str],
        default=None,
        section_title="Cellranger ARC Options",
        display_name="motif file",
        description="Specify a motif file to create a cellranger-arc index. Can be taken, e.g., from the JASPAR database.",
    ),
    "cellrangerarc_config": NextflowParameter(
        type=Optional[str],
        default=None,
        section_title=None,
        display_name="contig file",
        description="Specify a config file to create the cellranger-arc index.",
    ),
    "cellrangerarc_reference": NextflowParameter(
        type=Optional[str],
        default=None,
        section_title=None,
        display_name="reference genome",
        description="Specify the genome reference name used in the config file to create a cellranger-arc index.",
    ),
    "universc_index": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title="UniverSC Options",
        display_name="precomputed cellranger index",
        description="Specify a pre-calculated cellranger index. Readily prepared indexes can be obtained from the 10x Genomics website.",
    ),
    "multiqc_methods_description": NextflowParameter(
        type=Optional[LatchFile],
        default=None,
        section_title=None,
        display_name="Custom MultiQC yaml file",
        description="Custom MultiQC yaml file containing HTML including a methods description.",
    ),
    "genome": NextflowParameter(
        type=Optional[str],
        default=None,
        section_title=None,
        display_name="iGenomes Reference",
        description="If using a reference genome configured in the pipeline using iGenomes, use this parameter to give the ID for the reference. This is then used to build the full paths for all required reference genome files e.g. --genome GRCh38.",
    ),
}
