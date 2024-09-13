from typing import Annotated, List, Optional

from flytekit.core.annotation import FlyteAnnotation
from latch.resources.launch_plan import LaunchPlan
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile

from wf.entrypoint import (
    Aligner,
    Chemistry,
    Reference_Type,
    SampleSheet,
    STAR_options,
    cellxgene_prep,
    initialize,
    kb_workflow,
    nextflow_runtime,
)


@workflow(metadata._nextflow_metadata)
def nf_nf_core_scrnaseq(
    run_name: str,
    input: List[SampleSheet],
    outdir: LatchOutputDir,
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
) -> LatchOutputDir:
    """
    nf-core/scrnaseq

    Sample Description
    """

    pvc_name: str = initialize()
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
