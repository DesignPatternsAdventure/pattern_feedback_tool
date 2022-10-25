"""Graphic Output Tools."""

from pathlib import Path

from beartype import beartype
from code2flow.engine import code2flow
from pycg import formats
from pycg.pycg import CallGraphGenerator
from pycg.utils.constants import CALL_GRAPH_OP

# ---------------- code2flow ----------------


@beartype
def run_code2flow(
    arg_path: Path,
    output_image: Path,
    **kwargs: dict,  # type: ignore[type-arg]
) -> None:
    """Run code2flow to generate a call graph.

    - Based on: https://github.com/scottrogowski/code2flow/blob/7cfc8204bcbff39d1f3e8e5359a97ed1ffe1aeca/code2flow/engine.py#L860-L875

    Args:
        arg_path: "Directory containing source files to analyze, or multiple file paths"
        output_image: Image file to create (SVG, PNG, etc.)
        **kwargs: additional keyword arguments

    """
    code2flow(raw_source_paths=[arg_path], output_file=output_image.as_posix(), **kwargs)


# ---------------- pycg ----------------


@beartype
def run_pycg(
    arg_path: Path,
    package: str | None = None,
    max_iter: int = -1,
    **kwargs: dict,  # type: ignore[type-arg]
) -> dict:  # type: ignore[type-arg]
    """Run pycg to generate a call graph.

    - Based on: https://github.com/vitsalis/PyCG/blob/99c991e585615263f36fae5849df9c2daa684021/pycg/__main__.py#L75-L89

    Args:
        arg_path: "Directory containing source files to analyze, or multiple file paths"
        package: optional package name. Default is None
        max_iter: integer iterations. Default is -1 to defer to pycg
        **kwargs: additional keyword arguments

    Returns:
        dict: call graph

    """
    cg = CallGraphGenerator([arg_path], package=package, max_iter=max_iter, operation=CALL_GRAPH_OP, **kwargs)
    cg.analyze()

    formatter = formats.Simple(cg)

    # FASTEN format is probably easier to parse, but Simple is more human readable
    # formatter = formats.Fasten(cg, package=package, product="", forge="", version="", timestamp=0)

    return formatter.generate()  # type: ignore[no-any-return]

    # Also experimented with the graph output, but similar to Simple
    # as_formatter = formats.AsGraph(cg)
    # output = as_formatter.generate()

    # TODO: Still investigating how to best utilize these call graphs: https://github.com/vitsalis/PyCG#examples
