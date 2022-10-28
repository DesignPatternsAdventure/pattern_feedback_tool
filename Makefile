# Configuration Settings
GIT_COMMIT := head

I_TEST_DIR := integration_tests
C1_LOG := c1_pylint.log
C3_LOG := c3_flake8.log

# On Mac, can install these opinionated tools with brew:
# 	brew install gojq jc
JQ := gojq  # Use either jq or gojq
CAT := cat  # Use either cat or bat

.PHONY: clean
clean:  # Remove the local copy of the integration test code
	@echo "\nRemoving '$(I_TEST_DIR)' directory"
	@$(RM) -r $(I_TEST_DIR)

# HACK: Assumes pft is last line in pyproject.toml, but could do an actual find+replace
.PHONY: reset
reset: clean  # Reset the test code used for integration testing
	@echo "\nCloning test code for commit=$(GIT_COMMIT)"
	gh repo clone DesignPatternsAdventure/community-rpg $(I_TEST_DIR)
	cd $(I_TEST_DIR) && git reset --hard $(GIT_COMMIT)
	cd $(I_TEST_DIR) && sed -i '' -e '$$ d' pyproject.toml && poetry add ../../pattern_feedback_tool

.PHONY: _run
_run: $(if $(wildcard $(I_TEST_DIR)), , reset)
	@echo "\nRunning pattern feedback tool integration checks"

.PHONY: update
update:  # Sync with latest feedback tool code
	@echo "\nUpdating integration test against latest feedback tool code"
	poetry version patch
	cd $(I_TEST_DIR) && poetry update && poetry install --sync

.PHONY: check1
check1: _run  # pylint (one-off testing)
	@echo "\nRunning $@"
	cd $(I_TEST_DIR) && poetry run pylint src --rcfile=.pylintrc --output-format=json --output=$(C1_LOG) --exit-zero
	($(CAT) $(I_TEST_DIR)/$(C1_LOG) | $(JQ) 'map(.symbol) | unique') >$(I_TEST_DIR)/$(C1_LOG).json
	$(CAT) $(I_TEST_DIR)/$(C1_LOG).json

.PHONY: check2
check2: _run  # pyreverse
	@echo "\nRunning $@"
	cd $(I_TEST_DIR) && poetry run doit run build_diagrams

.PHONY: check3
check3: _run  # flake8 (one-off testing)
	@echo "\nRunning $@"
	$(RM) $(I_TEST_DIR)/$(C3_LOG)
	cd $(I_TEST_DIR) && poetry run flake8 src --config=.flake8 --output-file=$(C3_LOG) --exit-zero
	$(CAT) $(I_TEST_DIR)/$(C3_LOG)

.PHONY: check_doit
check_doit: _run  # combined pytest, pylint, and flake8 (but will not run build_diagrams)
	@echo "\nRunning $@"
	cd $(I_TEST_DIR) && poetry run doit

.PHONY: run
run: _run check1 check2 check3 check_doit  # Run the integration tests

# -----------------------------------------------------------------------------------------------------------------
# -----------------------       (Makefile helpers and decoration)      --------------------------------------------
# -- Copied from https://github.com/awinecki/magicfile/blob/c0d1acc141a285e60b5d3fade7a7b8994f033380/Makefile --
# -----------------------------------------------------------------------------------------------------------------

.DEFAULT_GOAL := help
# check https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
NC = \033[0m
ERR = \033[31;1m
TAB := '%-10s' # Increase if you have long commands

# tput colors
cyan80 := $(shell tput setaf 86)
bold := $(shell tput bold)
underline := $(shell tput smul)
_r := $(shell tput sgr0)  # reset terminal styling

help:
	@printf '\n'
	@printf '    $(underline)$(bold)Available make commands:$(_r)\n\n'
	@# Print non-check commands with comments
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:.+#.+$$' $(MAKEFILE_LIST) \
		| grep -v '^check-' \
		| grep -v '^env-' \
		| grep -v '^arg-' \
		| sed 's/:.*#/: #/g' \
		| awk 'BEGIN {FS = "[: ]+#[ ]+"}; \
		{printf "    make $(cyan80)$(bold)$(TAB) $(_r)# %s\n", $$1, $$2}'
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:( +\w+-\w+)*$$' $(MAKEFILE_LIST) \
		| grep -v help \
		| awk 'BEGIN {FS = ":"}; \
		{printf "    make $(cyan80)$(bold)$(TAB)$(_r)\n", $$1}'
	@echo "\n    $(underline)$(bold)Helper/Checks$(_r)\n"
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:.+#.+$$' $(MAKEFILE_LIST) \
		| grep -E '^(check|arg|env)-' \
		| awk 'BEGIN {FS = "[: ]+#[ ]+"}; \
		{printf "    make $(TAB) # %s\n", $$1, $$2}'
	@echo ""
