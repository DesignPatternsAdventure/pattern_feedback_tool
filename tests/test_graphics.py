from bs4 import BeautifulSoup

from pattern_feedback_tool.graphics import run_code2flow

from .configuration import SAMPLE_CODE_DIR


def test_run_code2flow(assert_against_cache, fix_test_cache):
    tmp_image_path = fix_test_cache / f'code2flow-{SAMPLE_CODE_DIR.stem}.svg'

    run_code2flow(SAMPLE_CODE_DIR, output_image=tmp_image_path)  # act

    with open(tmp_image_path) as fp:
        soup = BeautifulSoup(fp)
    text_tags = sorted(_t.text for _t in soup.find_all('text'))
    assert_against_cache(text_tags)
