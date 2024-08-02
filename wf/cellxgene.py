import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

from latch.resources.tasks import large_task
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)


class Aligner(Enum):
    star = "star"
    alevin = "alevin"
    kallisto = "kallisto"
    # cellranger = "cellranger"
    # cellranger_arc = "cellrangerarc"
    # UniverSC = "universc"


@large_task
def cellxgene_prep(
    run_name: str,
    outdir: LatchDir,
    aligner: Aligner,
    skip_emptydrops: Optional[bool],
) -> LatchOutputDir:
    print("Setting up local directories")
    local_output_directory = Path(f"/root/output/{run_name}/cellxgene_h5ad")
    local_output_directory.mkdir(parents=True, exist_ok=True)

    try:
        # List installed packages in the cellxgene environment
        pip_list_cmd = ["/bin/bash", "-c", "source /mambaforge/bin/activate cellxgene && pip list"]
        print("Listing installed packages in cellxgene environment:")
        subprocess.run(pip_list_cmd, check=True)

        base_path = f"{outdir.remote_path}/{run_name}/{aligner.value}/mtx_conversions"

        if skip_emptydrops:
            input_file = "combined_raw_matrix.h5ad"
        else:
            input_file = "combined_custom_emptydrops_filter_matrix.h5ad"

        input_path = Path(LatchFile(f"{base_path}/{input_file}").local_path)
        output_path = local_output_directory / f"prepared_{input_file}"

        cmd = [
            "/bin/bash",
            "-c",
            "source /mambaforge/bin/activate cellxgene && cellxgene prepare --output "
            + str(output_path)
            + " "
            + str(input_path),
        ]
        print(" ".join(cmd))

        subprocess.run(cmd, check=True)

        print(f"Prepared file saved to: {output_path}")
    except Exception as e:
        print(f"Error occurred: {e}")

    print("Uploading results")
    return LatchOutputDir(str("/root/output"), outdir.remote_path)
