import typing

import typing_extensions
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    Fork,
    ForkBranch,
    LatchAuthor,
    NextflowMetadata,
    NextflowParameter,
    NextflowRuntimeResources,
    Params,
    Section,
    Spoiler,
    Text,
)

from .parameters import generated_parameters

# from wf.entrypoint import initialize, nextflow_runtime

flow = [
    Section("Input/Output", Params("input")),
    Section("Output", Params("outdir", "runname")),
    Section(
        "Reference Genome Options",
        Fork(
            "genome_source",
            "",
            latch_genome_source=ForkBranch("Latch Certified Reference Genome", Params("latch_genome")),
            input_ref=ForkBranch(
                # "Custom Reference Genome", Params("fasta", "gtf", "transcript_fasta", "save_reference")
                "Custom Reference Genome",
                Params("fasta", "gtf"),
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
                alevin_frk=ForkBranch("Alevin", Params("salmon_index", "txp2gene", "simpleaf_rlen")),
                cellrangerarc_frk=ForkBranch(
                    "Cellranger Arc", Params("cellrangerarc_config", "cellrangerarc_reference", "motifs")
                ),
                cellranger_frk=ForkBranch("Cellranger", Params("cellranger_index")),
                kallisto_frk=ForkBranch(
                    "Kallisto/Bustools", Params("kallisto_index", "kb_t1c", "kb_t2c", "kb_workflow", "kb_filter")
                ),
                star_frk=ForkBranch("Star", Params("star_index", "star_ignore_sjdbgtf", "star_feature")),
                universc_frk=ForkBranch("UniverSC", Params("universc_index")),
            ),
        ),
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
            Params("skip_multiqc", "skip_fastqc", "skip_emptydrops"),
        ),
    ),
]

NextflowMetadata(
    display_name="nf-core/scrnaseq",
    author=LatchAuthor(
        name="nf-core",
    ),
    parameters=generated_parameters,
    runtime_resources=NextflowRuntimeResources(
        cpus=8,
        memory=8,
        storage_gib=500,
    ),
    log_dir=LatchDir("latch:///your_log_dir"),
    flow=flow,
)
