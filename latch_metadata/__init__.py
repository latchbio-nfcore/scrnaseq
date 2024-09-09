from latch.types.directory import LatchDir
from latch.types.metadata import LatchAuthor, NextflowMetadata, NextflowRuntimeResources

from .parameters import flow, generated_parameters

NextflowMetadata(
    display_name="nf-core/scrnaseq",
    author=LatchAuthor(
        name="nf-core",
    ),
    parameters=generated_parameters,
    runtime_resources=NextflowRuntimeResources(
        cpus=4,
        memory=8,
        storage_gib=100,
    ),
    flow=flow,
    log_dir=LatchDir("latch:///your_log_dir"),
)
