# Developer Notes

## Local Development

```sh
git clone https://github.com/DesignPatternsAdventure/pattern_feedback_tool.git
cd pattern_feedback_tool
poetry install

# See the available tasks
poetry run doit list

# Run the default task list (lint, auto-format, test coverage, etc.)
poetry run doit --continue

# Make code changes and run specific tasks as needed:
poetry run doit run test
```

## Publishing

For testing, create an account on [TestPyPi](https://test.pypi.org/legacy/). Replace `...` with the API token generated on TestPyPi or PyPi respectively

```sh
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi ...

poetry run doit run publish_test_pypi
# If you didn't configure a token, you will need to provide your username and password to publish
```

To publish to the real PyPi

```sh
poetry config pypi-token.pypi ...
poetry run doit run publish

# For a full release, triple check the default tasks, increment the version, rebuild documentation (twice), and publish!
poetry run doit run --continue
poetry run doit run cl_bump lock document deploy_docs publish

# For pre-releases use cl_bump_pre
poetry run doit run cl_bump_pre -p rc
poetry run doit run lock document deploy_docs publish
```

## Current Status

<!-- {cts} COVERAGE -->
| File                                    |   Statements |   Missing |   Excluded | Coverage   |
|-----------------------------------------|--------------|-----------|------------|------------|
| `pattern_feedback_tool/__init__.py`     |            5 |         0 |          0 | 100.0%     |
| `pattern_feedback_tool/doit_tasks.py`   |          139 |        18 |          0 | 87.1%      |
| `pattern_feedback_tool/graphics.py`     |           15 |         0 |          0 | 100.0%     |
| `pattern_feedback_tool/lint_parsers.py` |           64 |         0 |          0 | 100.0%     |
| `pattern_feedback_tool/linters.py`      |           17 |         1 |          0 | 94.1%      |
| `pattern_feedback_tool/settings.py`     |           28 |         2 |          0 | 92.9%      |
| **Totals**                              |          268 |        21 |          0 | 92.2%      |

Generated on: 2022-11-13
<!-- {cte} -->
