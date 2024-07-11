from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={},
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=8, memory=8, storage_gib=500)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], barcode_whitelist: typing.Optional[LatchFile], skip_multiqc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], skip_emptydrops: typing.Optional[bool], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], transcript_fasta: typing.Optional[LatchFile], gtf: typing.Optional[LatchFile], save_reference: typing.Optional[bool], salmon_index: typing.Optional[LatchFile], txp2gene: typing.Optional[LatchFile], star_index: typing.Optional[LatchFile], star_ignore_sjdbgtf: typing.Optional[str], seq_center: typing.Optional[str], kallisto_index: typing.Optional[LatchFile], kb_t1c: typing.Optional[LatchFile], kb_t2c: typing.Optional[LatchFile], kb_filter: typing.Optional[bool], cellranger_index: typing.Optional[LatchFile], motifs: typing.Optional[str], cellrangerarc_config: typing.Optional[str], cellrangerarc_reference: typing.Optional[str], universc_index: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], aligner: typing.Optional[str], protocol: typing.Optional[str], simpleaf_rlen: typing.Optional[int], star_feature: typing.Optional[str], kb_workflow: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            ".git",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
            "-resume",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('barcode_whitelist', barcode_whitelist),
                *get_flag('aligner', aligner),
                *get_flag('protocol', protocol),
                *get_flag('skip_multiqc', skip_multiqc),
                *get_flag('skip_fastqc', skip_fastqc),
                *get_flag('skip_emptydrops', skip_emptydrops),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('transcript_fasta', transcript_fasta),
                *get_flag('gtf', gtf),
                *get_flag('save_reference', save_reference),
                *get_flag('salmon_index', salmon_index),
                *get_flag('txp2gene', txp2gene),
                *get_flag('simpleaf_rlen', simpleaf_rlen),
                *get_flag('star_index', star_index),
                *get_flag('star_ignore_sjdbgtf', star_ignore_sjdbgtf),
                *get_flag('seq_center', seq_center),
                *get_flag('star_feature', star_feature),
                *get_flag('kallisto_index', kallisto_index),
                *get_flag('kb_t1c', kb_t1c),
                *get_flag('kb_t2c', kb_t2c),
                *get_flag('kb_workflow', kb_workflow),
                *get_flag('kb_filter', kb_filter),
                *get_flag('cellranger_index', cellranger_index),
                *get_flag('motifs', motifs),
                *get_flag('cellrangerarc_config', cellrangerarc_config),
                *get_flag('cellrangerarc_reference', cellrangerarc_reference),
                *get_flag('universc_index', universc_index),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms1536M -Xmx6144M -XX:ActiveProcessorCount=8",
            "NXF_DISABLE_CHECK_LATEST": "true",
            "NXF_ENABLE_VIRTUAL_THREADS": "false",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_scrnaseq", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_scrnaseq(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], barcode_whitelist: typing.Optional[LatchFile], skip_multiqc: typing.Optional[bool], skip_fastqc: typing.Optional[bool], skip_emptydrops: typing.Optional[bool], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], transcript_fasta: typing.Optional[LatchFile], gtf: typing.Optional[LatchFile], save_reference: typing.Optional[bool], salmon_index: typing.Optional[LatchFile], txp2gene: typing.Optional[LatchFile], star_index: typing.Optional[LatchFile], star_ignore_sjdbgtf: typing.Optional[str], seq_center: typing.Optional[str], kallisto_index: typing.Optional[LatchFile], kb_t1c: typing.Optional[LatchFile], kb_t2c: typing.Optional[LatchFile], kb_filter: typing.Optional[bool], cellranger_index: typing.Optional[LatchFile], motifs: typing.Optional[str], cellrangerarc_config: typing.Optional[str], cellrangerarc_reference: typing.Optional[str], universc_index: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], aligner: typing.Optional[str] = 'alevin', protocol: typing.Optional[str] = 'auto', simpleaf_rlen: typing.Optional[int] = 91, star_feature: typing.Optional[str] = 'Gene', kb_workflow: typing.Optional[str] = 'standard') -> None:
    """
    nf-core/scrnaseq

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, barcode_whitelist=barcode_whitelist, aligner=aligner, protocol=protocol, skip_multiqc=skip_multiqc, skip_fastqc=skip_fastqc, skip_emptydrops=skip_emptydrops, genome=genome, fasta=fasta, transcript_fasta=transcript_fasta, gtf=gtf, save_reference=save_reference, salmon_index=salmon_index, txp2gene=txp2gene, simpleaf_rlen=simpleaf_rlen, star_index=star_index, star_ignore_sjdbgtf=star_ignore_sjdbgtf, seq_center=seq_center, star_feature=star_feature, kallisto_index=kallisto_index, kb_t1c=kb_t1c, kb_t2c=kb_t2c, kb_workflow=kb_workflow, kb_filter=kb_filter, cellranger_index=cellranger_index, motifs=motifs, cellrangerarc_config=cellrangerarc_config, cellrangerarc_reference=cellrangerarc_reference, universc_index=universc_index, multiqc_methods_description=multiqc_methods_description)

