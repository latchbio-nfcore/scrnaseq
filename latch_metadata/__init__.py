from latch.types.directory import LatchDir
from latch.types.metadata import LatchAuthor, NextflowMetadata, NextflowRuntimeResources

from .parameters import generated_parameters

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
)
