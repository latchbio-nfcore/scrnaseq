from typing import List, Optional

from latch.resources.launch_plan import LaunchPlan
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile

from wf.cellxgene import cellxgene_prep
from wf.entrypoint import (
    Aligner,
    Chemistry,
    Reference_Type,
    SampleSheet,
    STAR_options,
    initialize,
    kb_workflow,
    nextflow_runtime,
)


@workflow(metadata._nextflow_metadata)
def nf_nf_core_scrnaseq(
    run_name: str,
    input: List[SampleSheet],
    email: Optional[str],
    multiqc_title: Optional[str],
    barcode_whitelist: Optional[LatchFile],
    protocol: Chemistry,
    skip_multiqc: bool,
    skip_fastqc: bool,
    genome_source: str,
    genome: Optional[str],
    fasta: Optional[LatchFile],
    transcript_fasta: Optional[LatchFile],
    gtf: Optional[LatchFile],
    salmon_index: Optional[LatchDir],
    txp2gene: Optional[LatchFile],
    star_index: Optional[LatchDir],
    star_ignore_sjdbgtf: Optional[LatchFile],
    seq_center: Optional[str],
    kallisto_index: Optional[LatchDir],
    kb_t1c: Optional[LatchFile],
    kb_t2c: Optional[LatchFile],
    kb_filter: bool,
    cellranger_index: Optional[LatchFile],
    motifs: Optional[str],
    cellrangerarc_config: Optional[str],
    cellrangerarc_reference: Optional[str],
    universc_index: Optional[LatchFile],
    multiqc_methods_description: Optional[LatchFile],
    aligner: Aligner = Aligner.alevin,
    latch_genome: Reference_Type = Reference_Type.hg38,
    simpleaf_rlen: Optional[int] = 91,
    star_feature: Optional[STAR_options] = STAR_options.gene,
    kb_workflow: Optional[kb_workflow] = kb_workflow.std,
    save_reference: bool = False,
    skip_emptydrops: bool = True,
    outdir: LatchOutputDir = LatchOutputDir("latch:///SingleCellRNAseq"),
) -> LatchOutputDir:
    """
    nf-core/scrnaseq is a bioinformatics best-practice analysis pipeline for processing 10x Genomics single-cell RNA-seq data.

    <html>
    <p align="center">
    <img src="https://user-images.githubusercontent.com/31255434/182289305-4cc620e3-86ae-480f-9b61-6ca83283caa5.jpg" alt="Latch Verified" width="100">
    </p>

    <p align="center">
    <strong>
    Latch Verified
    </strong>
    </p>

    <p align="center">

    [![Cite with Zenodo](http://img.shields.io/badge/DOI-10.5281/zenodo.3568187-1073c8?labelColor=000000)](https://doi.org/10.5281/zenodo.3568187)

    **nf-core/scrnaseq** is a bioinformatics best-practice analysis pipeline for processing 10x Genomics single-cell RNA-seq data.

    ## Introduction

    This workflow is hosted on Latch Workflows, using a native Nextflow integration, with a graphical interface for accessible analysis by scientists. There is also an integration with Latch Registry so that batched workflows can be launched from “graphical sample sheets” or tables associating raw sequencing files with metadata.

    This is a community effort in building a pipeline capable to support:

    - Alevin-Fry + AlevinQC
    - STARSolo
    - Kallisto + BUStools

    ## Documentation

    The nf-core/scrnaseq pipeline comes with documentation about the pipeline [usage](https://nf-co.re/scrnaseq/usage), [parameters](https://nf-co.re/scrnaseq/parameters) and [output](https://nf-co.re/scrnaseq/output).

    ## Usage

    First, prepare a samplesheet with your input data that looks as follows:

    `samplesheet.csv`:

    sample,fastq_1,fastq_2,expected_cells
    pbmc8k,pbmc8k_S1_L007_R1_001.fastq.gz,pbmc8k_S1_L007_R2_001.fastq.gz,10000
    pbmc8k,pbmc8k_S1_L008_R1_001.fastq.gz,pbmc8k_S1_L008_R2_001.fastq.gz,10000

    Each row represents a fastq file (single-end) or a pair of fastq files (paired end).

    ## Decision Tree for users

    The nf-core/scrnaseq pipeline features several paths to analyze your single cell data. Future additions will also be done soon, e.g. the addition of multi-ome analysis types. To aid users in analyzing their data, we have added a decision tree to help people decide on what type of analysis they want to run and how to choose appropriate parameters for that.

    Options for the respective alignment method can be found [here](https://github.com/nf-core/scrnaseq/blob/dev/docs/usage.md#aligning-options) to choose between methods.

    ## Pipeline output

    To see the results of an example test run with a full size dataset refer to the [results](https://nf-co.re/scrnaseq/results) tab on the nf-core website pipeline page.
    For more details about the output files and reports, please refer to the
    [output documentation](https://nf-co.re/scrnaseq/output).

    ## Credits

    nf-core/scrnaseq was originally written by Bailey PJ, Botvinnik O, Marques de Almeida F, Gabernet G, Peltzer A, Sturm G.

    We thank the following people and teams for their extensive assistance in the development of this pipeline:

    - @heylf
    - @KevinMenden
    - @FloWuenne
    - @rob-p
    - [GHGA](https://www.ghga.de/)

    ## Contributions and Support

    If you would like to contribute to this pipeline, please see the [contributing guidelines](.github/CONTRIBUTING.md).

    For further information or help, don't hesitate to get in touch on the [Slack `#scrnaseq` channel](https://nfcore.slack.com/channels/scrnaseq) (you can join with [this invite](https://nf-co.re/join/slack)).

    ## Citations

    If you use nf-core/scrnaseq for your analysis, please cite it using the following doi: [10.5281/zenodo.3568187](https://doi.org/10.5281/zenodo.3568187)

    The basic benchmarks that were used as motivation for incorporating the three available modular workflows can be found in [this publication](https://www.biorxiv.org/content/10.1101/673285v2).

    We offer all three paths for the processing of scRNAseq data so it remains up to the user to decide which pipeline workflow is chosen for a particular analysis question.

    An extensive list of references for the tools used by the pipeline can be found in the [`CITATIONS.md`](CITATIONS.md) file.

    """

    pvc_name: str = initialize(run_name=run_name)
    run_name = nextflow_runtime(
        pvc_name=pvc_name,
        input=input,
        outdir=outdir,
        run_name=run_name,
        email=email,
        multiqc_title=multiqc_title,
        barcode_whitelist=barcode_whitelist,
        aligner=aligner,
        protocol=protocol,
        skip_multiqc=skip_multiqc,
        skip_fastqc=skip_fastqc,
        skip_emptydrops=skip_emptydrops,
        genome_source=genome_source,
        genome=genome,
        latch_genome=latch_genome,
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
    )

    return cellxgene_prep(
        run_name=run_name,
        aligner=aligner,
        skip_emptydrops=skip_emptydrops,
        outdir=outdir,
    )


LaunchPlan(
    nf_nf_core_scrnaseq,
    "Small Test",
    {
        "input": [
            SampleSheet(
                sample="SRR19078418",
                fastq_1=LatchFile(
                    "s3://latch-public/nf-core/scrnaseq/test_data/Pool85_1_S1_L001_R1_001.fastq.gz"
                ),
                fastq_2=LatchFile(
                    "s3://latch-public/nf-core/scrnaseq/test_data/Pool85_1_S1_L001_R2_001.fastq.gz"
                ),
                expected_cells=None,
                seq_center=None,
            ),
            SampleSheet(
                sample="SRR19078429",
                fastq_1=LatchFile(
                    "s3://latch-public/nf-core/scrnaseq/test_data/Pool85_1_S1_L002_R1_001.fastq.gz"
                ),
                fastq_2=LatchFile(
                    "s3://latch-public/nf-core/scrnaseq/test_data/Pool85_1_S1_L002_R2_001.fastq.gz"
                ),
                expected_cells=None,
                seq_center=None,
            ),
        ],
        "run_name": "Test_run",
        "protocol": Chemistry._10xv3,
    },
)
