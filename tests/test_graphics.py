import json

from pattern_feedback_tool.graphics import run_code2flow, run_pycg

from .configuration import SAMPLE_CODE_DIR


def test_run_code2flow(assert_against_cache, fix_test_cache):
    # Specify a '.json' file so that graphviz isn't required
    out_path = fix_test_cache / f'code2flow-{SAMPLE_CODE_DIR.stem}.json'

    run_code2flow(SAMPLE_CODE_DIR, output_image=out_path)  # act

    data = json.loads(out_path.read_text())
    node_names = sorted([_v['name'] for _v in data['graph']['nodes'].values()])
    assert_against_cache(node_names)


def test_run_pycg(assert_against_cache):
    result = run_pycg(SAMPLE_CODE_DIR / 'game_view.py', package='rpg')

    # FYI: This is just a deterministic way to log the call graph. Seems to change when re-run
    assert_against_cache(sorted(result.keys()))
