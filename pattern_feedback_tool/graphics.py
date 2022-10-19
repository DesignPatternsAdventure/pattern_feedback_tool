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


# ---------------- PLANNED: pylint.pyreverse ----------------


@beartype
def run_pyreverse(
    arg_path: Path,
    package: str = 'No Name',
    **kwargs: dict,  # type: ignore[type-arg]
) -> None:
    """Run pyreverse to generate a class diagram.

    - Based on: https://github.com/PyCQA/pylint/blob/7088409227e826ed8720886252fe05265daa9045/pylint/pyreverse/main.py#L231-L246

    Args:
        arg_path: "Directory containing source files to analyze, or multiple file paths"
        package: string package name. Default is "No Name"
        **kwargs: additional keyword arguments for pyreverse config

    Returns:
        str: plantuml syntax

    """
    # See: https://github.com/PyCQA/pylint/blob/7088409227e826ed8720886252fe05265daa9045/pylint/__init__.py#L60-L67
    # And how mocked in unit tests:
    #   https://github.com/PyCQA/pylint/tree/7088409227e826ed8720886252fe05265daa9045/tests/pyreverse
    raise NotImplementedError('pyreverse should probably be called from shell')

    # from argparse import Namespace
    # from pylint.pyreverse.main import fix_import_path, project_from_files, Linker, DiadefsHandler, writer, OPTIONS
    #
    # config_kwargs = {
    #     str(value.get("dest") or key.replace('-', '_')): value["default"]
    #     for key, value in dict(OPTIONS).items()
    # }
    # config_kwargs["classes"] = config_kwargs["classes"] or []
    # config_kwargs["output_format"] = 'plantuml'
    # config_kwargs["output_directory"] = 'tmp'
    # config = Namespace(**(config_kwargs | kwargs))

    # args = [arg_path.as_posix()]
    # # https://github.com/PyCQA/pylint/blob/7088409227e826ed8720886252fe05265daa9045/pylint/lint/utils.py#L89
    # with fix_import_path(args):
    #     # https://github.com/PyCQA/pylint/blob/7088409227e826ed8720886252fe05265daa9045/pylint/pyreverse/inspector.py#L316
    #     project = project_from_files(args, project_name=package or "No Name")
    #     linker = Linker(project, tag=True)
    #     handler = DiadefsHandler(config)
    #     diadefs = handler.get_diadefs(project, linker)
    # writer.DiagramWriter(config).write(diadefs)


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
