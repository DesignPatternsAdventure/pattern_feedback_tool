from radon.cli.harvest import CCHarvester

from pattern_feedback_tool.linters import run_radon

from .configuration import SAMPLE_CODE_DIR


def test_run_radon(assert_against_cache):
    results = run_radon(SAMPLE_CODE_DIR, min_score='D', radon_harvester=CCHarvester)

    assert_against_cache(results.split('\n'))
