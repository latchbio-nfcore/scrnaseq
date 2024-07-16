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
    Section("Input/Output", Params("input", "outdir", "email")),
    Section("MultiQC Title", Params("multiqc_title")),
    Section(
        "Reference Genome Options",
        Fork(
            "genome_source",
            "",
            latch_genome_source=ForkBranch("Latch Certified Reference Genome", Params("genome")),
            input_ref=ForkBranch(
                "Custom Reference Genome", Params("fasta", "gtf", "transcript_fasta", "save_reference")
            ),
        ),
    ),
    Section("Custom Barcode Whitelist", Params("barcode_whitelist")),
    Section("Chemistry", Params("protocol")),
    Section("Skip Tools", Params("skip_multiqc", "skip_fastqc", "skip_emptydrops")),
    Section(
        "Aligners",
        Params("aligner"),
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
    Section("Generic Options", Params("multiqc_methods_description")),
]

NextflowMetadata(
    display_name="nf-core/scrnaseq",
    author=LatchAuthor(
        name="Harihara",
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

"""@workflow(metadata._nextflow_metadata)
def nf_nf_core_scrnaseq(
    input: LatchFile,
    outdir: LatchOutputDir,
    email: typing.Optional[str],
    multiqc_title: typing.Optional[str],
    barcode_whitelist: typing.Optional[LatchFile],
    skip_multiqc: typing.Optional[bool],
    skip_fastqc: typing.Optional[bool],
    skip_emptydrops: typing.Optional[bool],
    genome: typing.Optional[str],
    fasta: typing.Optional[LatchFile],
    transcript_fasta: typing.Optional[LatchFile],
    gtf: typing.Optional[LatchFile],
    save_reference: typing.Optional[bool],
    salmon_index: typing.Optional[LatchFile],
    txp2gene: typing.Optional[LatchFile],
    star_index: typing.Optional[LatchFile],
    star_ignore_sjdbgtf: typing.Optional[str],
    seq_center: typing.Optional[str],
    kallisto_index: typing.Optional[LatchFile],
    kb_t1c: typing.Optional[LatchFile],
    kb_t2c: typing.Optional[LatchFile],
    kb_filter: typing.Optional[bool],
    cellranger_index: typing.Optional[LatchFile],
    motifs: typing.Optional[str],
    cellrangerarc_config: typing.Optional[str],
    cellrangerarc_reference: typing.Optional[str],
    universc_index: typing.Optional[LatchFile],
    multiqc_methods_description: typing.Optional[str],
    protocol: str,
    aligner: typing.Optional[str] = "alevin",
    simpleaf_rlen: typing.Optional[int] = 91,
    star_feature: typing.Optional[str] = "Gene",
    kb_workflow: typing.Optional[str] = "standard",
) -> None:
    pvc_name: str = initialize()
    run_name = nextflow_runtime(
        pvc_name=pvc_name,
        input=input,
        outdir=outdir,
        email=email,
        multiqc_title=multiqc_title,
        barcode_whitelist=barcode_whitelist,
        aligner=aligner,
        protocol=protocol,
        skip_multiqc=skip_multiqc,
        skip_fastqc=skip_fastqc,
        skip_emptydrops=skip_emptydrops,
        genome=genome,
        fasta=fasta,
        transcript_fasta=transcript_fasta,
        gtf=gtf,
        save_reference=save_reference,
        salmon_index=salmon_index,
        txp2gene=txp2gene,
        simpleaf_rlen=simpleaf_rlen,
        star_index=star_index,
        star_ignore_sjdbgtf=star_ignore_sjdbgtf,
        seq_center=seq_center,
        star_feature=star_feature,
        kallisto_index=kallisto_index,
        kb_t1c=kb_t1c,
        kb_t2c=kb_t2c,
        kb_workflow=kb_workflow,
        kb_filter=kb_filter,
        cellranger_index=cellranger_index,
        motifs=motifs,
        cellrangerarc_config=cellrangerarc_config,
        cellrangerarc_reference=cellrangerarc_reference,
        universc_index=universc_index,
        multiqc_methods_description=multiqc_methods_description,
    )"""
