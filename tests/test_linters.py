import pytest
from radon.cli.harvest import CCHarvester

from pattern_feedback_tool.linters import run_pylint, run_radon

from .configuration import SAMPLE_CODE_DIR


def test_run_radon(assert_against_cache):
    results = run_radon(SAMPLE_CODE_DIR, min_score='D', radon_harvester=CCHarvester)

    cleaned_results = results.replace(SAMPLE_CODE_DIR.parent.as_posix(), '~')
    assert_against_cache(cleaned_results.split('\n'))


def test_run_pylint(assert_against_cache):
    with pytest.raises(NotImplementedError):
        run_pylint()
