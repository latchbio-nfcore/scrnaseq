import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional

import requests
import typing_extensions
from flytekit.core.annotation import FlyteAnnotation
from latch.executions import rename_current_execution, report_nextflow_used_storage
from latch.ldata.path import LPath
from latch.resources.tasks import custom_task, nextflow_runtime_task
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.nextflow.workflow import get_flag
from latch_cli.services.register.utils import import_module_by_path
from latch_cli.utils import urljoins
from wf.cellxgene import cellxgene_prep

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

sys.stdout.reconfigure(line_buffering=True)


@dataclass
class SampleSheet:
    sample: str
    fastq_1: LatchFile
    fastq_2: LatchFile
    expected_cells: Optional[int]
    seq_center: Optional[str]


class Aligner(Enum):
    star = "star"
    alevin = "alevin"
    kallisto = "kallisto"


class Chemistry(Enum):
    _10xv1 = "10XV1"
    _10xv2 = "10XV2"
    _10xv3 = "10XV3"
    auto = "auto"


class STAR_options(Enum):
    gene = "Gene"
    gene_full = "GeneFull"
    gene_vel = "Gene Velocyto"


class Reference_Type(Enum):
    hg38 = "Homo sapiens (RefSeq GRCh38)"
    mm10 = "Mus musculus (RefSeq GRCm38)"


class kb_workflow(Enum):
    std = "standard"
    nac = "nac"
    lamanno = "lamanno"


def get_flag_defaults(name: str, val: Any, default_val: Optional[Any]):
    if val == default_val or val is None:
        return ""
    else:
        return get_flag(name=name, val=val)


@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        # "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage-ofs",
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_expiration_hours": 1,
            "storage_gib": 100,
            "version": 2,
        },
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]


input_construct_samplesheet = metadata._nextflow_metadata.parameters[
    "input"
].samplesheet_constructor


@nextflow_runtime_task(cpu=8, memory=8, storage_gib=500)
def nextflow_runtime(
    run_name: str,
    pvc_name: str,
    input: List[SampleSheet],
    outdir: LatchOutputDir,
    email: Optional[str],
    multiqc_title: Optional[str],
    barcode_whitelist: Optional[LatchFile],
    protocol: Chemistry,
    skip_multiqc: bool,
    skip_fastqc: bool,
    genome_source: str,
    fasta: Optional[LatchFile],
    transcript_fasta: Optional[LatchFile],
    gtf: Optional[LatchFile],
    salmon_index: Optional[LatchDir],
    txp2gene: Optional[LatchFile],
    star_index: Optional[LatchFile],
    star_ignore_sjdbgtf: Optional[str],
    seq_center: Optional[str],
    kallisto_index: Optional[LatchFile],
    kb_t1c: Optional[LatchFile],
    kb_t2c: Optional[LatchFile],
    kb_filter: bool,
    cellranger_index: Optional[LatchFile],
    motifs: Optional[str],
    cellrangerarc_config: Optional[str],
    cellrangerarc_reference: Optional[str],
    universc_index: Optional[LatchFile],
    multiqc_methods_description: Optional[str],
    aligner: Aligner,
    latch_genome: Reference_Type,
    simpleaf_rlen: Optional[int],
    star_feature: Optional[STAR_options],
    kb_workflow: Optional[kb_workflow],
    save_reference: bool = False,
    skip_emptydrops: bool = True,
) -> str:
    shared_dir = Path("/nf-workdir")
    rename_current_execution(str(run_name))

    input_samplesheet = input_construct_samplesheet(input)

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
        *get_flag("input", input_samplesheet),
        *get_flag_defaults(
            "outdir", LatchOutputDir(outdir.remote_path + "/" + run_name), None
        ),
        *get_flag_defaults("email", email, None),
        *get_flag_defaults("multiqc_title", multiqc_title, None),
        *get_flag_defaults("barcode_whitelist", barcode_whitelist, None),
        *get_flag_defaults("aligner", aligner, Aligner.alevin),
        *get_flag_defaults("protocol", protocol, None),
        *get_flag_defaults("skip_multiqc", skip_multiqc, None),
        *get_flag_defaults("skip_fastqc", skip_fastqc, None),
        *get_flag_defaults("skip_emptydrops", skip_emptydrops, None),
    ]

    if genome_source == "latch_genome_source":
        print(latch_genome.name)
        cmd += [
            "--fasta",
            f"s3://latch-public/test-data/35597/scrnaseq_ref/{latch_genome.name}/{latch_genome.name}.fa",
            "--gtf",
            f"s3://latch-public/test-data/35597/scrnaseq_ref/{latch_genome.name}/{latch_genome.name}.gtf",
        ]

    cmd += [
        *get_flag_defaults("fasta", fasta, None),
        *get_flag_defaults("transcript_fasta", transcript_fasta, None),
        *get_flag_defaults("gtf", gtf, None),
        *get_flag_defaults("save_reference", save_reference, False),
        *get_flag_defaults("salmon_index", salmon_index, None),
        *get_flag_defaults("txp2gene", txp2gene, None),
        *get_flag_defaults("simpleaf_rlen", simpleaf_rlen, "91"),
        *get_flag_defaults("star_index", star_index, None),
        *get_flag_defaults("star_ignore_sjdbgtf", star_ignore_sjdbgtf, None),
        *get_flag_defaults("seq_center", seq_center, None),
        *get_flag_defaults("star_feature", star_feature, STAR_options.gene),
        *get_flag_defaults("kallisto_index", kallisto_index, None),
        *get_flag_defaults("kb_t1c", kb_t1c, None),
        *get_flag_defaults("kb_t2c", kb_t2c, None),
        *get_flag_defaults("kb_workflow", kb_workflow, None),
        *get_flag_defaults("kb_filter", kb_filter, None),
        *get_flag_defaults("cellranger_index", cellranger_index, None),
        *get_flag_defaults("motifs", motifs, None),
        *get_flag_defaults("cellrangerarc_config", cellrangerarc_config, None),
        *get_flag_defaults("cellrangerarc_reference", cellrangerarc_reference, None),
        *get_flag_defaults("universc_index", universc_index, None),
        *get_flag_defaults(
            "multiqc_methods_description", multiqc_methods_description, None
        ),
    ]

    print("Launching Nextflow Runtime")
    print(" ".join(cmd))
    print(flush=True)

    failed = False
    try:
        env = {
            **os.environ,
            "NXF_ANSI_LOG": "false",
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms1536M -Xmx6144M -XX:ActiveProcessorCount=4",
            "NXF_DISABLE_CHECK_LATEST": "true",
            "NXF_ENABLE_VIRTUAL_THREADS": "false",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    except subprocess.CalledProcessError:
        failed = True
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(
                    urljoins(
                        "latch:///your_log_dir/nf_nf_core_methylseq",
                        name,
                        "nextflow.log",
                    )
                )
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)

        print("Computing size of workdir... ", end="")
        try:
            result = subprocess.run(
                ["du", "-sb", str(shared_dir)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5 * 60,
            )

            size = int(result.stdout.split()[0])
            report_nextflow_used_storage(size)
            print(f"Done. Workdir size: {size / 1024 / 1024 / 1024: .2f} GiB")
        except subprocess.TimeoutExpired:
            print(
                "Failed to compute storage size: Operation timed out after 5 minutes."
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to compute storage size: {e.stderr}")
        except Exception as e:
            print(f"Failed to compute storage size: {e}")

        if failed:
            sys.exit(1)

        return str(run_name)


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
    fasta: Optional[LatchFile],
    transcript_fasta: Optional[LatchFile],
    gtf: Optional[LatchFile],
    salmon_index: Optional[LatchDir],
    txp2gene: Optional[LatchFile],
    star_index: Optional[LatchFile],
    star_ignore_sjdbgtf: Optional[str],
    seq_center: Optional[str],
    kallisto_index: Optional[LatchFile],
    kb_t1c: Optional[LatchFile],
    kb_t2c: Optional[LatchFile],
    kb_filter: bool,
    cellranger_index: Optional[LatchFile],
    motifs: Optional[str],
    cellrangerarc_config: Optional[str],
    cellrangerarc_reference: Optional[str],
    universc_index: Optional[LatchFile],
    multiqc_methods_description: Optional[str],
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
