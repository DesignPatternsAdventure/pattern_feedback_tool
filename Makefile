# Configuration Settings
GIT_COMMIT := 70653ea19d0c34d847813c29b1004af967900ce9

I_TEST_DIR := integration_tests
T1_LOG := $(I_TEST_DIR)/t1_pylint.log

JQ := gojq  # Use either jq or gojq

.PHONY: clean
clean:  # Remove the local copy of the integration test code
	@echo "\nRemoving '$(I_TEST_DIR)' directory"
	@$(RM) -r $(I_TEST_DIR)

.PHONY: reset
reset: clean  # Reset the test code used for integration testing
	@echo "\nCloning test code for commit=$(GIT_COMMIT)"
	@gh repo clone DesignPatternsAdventure/community-rpg $(I_TEST_DIR)
	@cd $(I_TEST_DIR) && git reset --hard $(GIT_COMMIT)

.PHONY: run
run: $(if $(wildcard $(I_TEST_DIR)), , reset)  # Run the integration tests
	@echo "\nRunning tests"
	poetry run pylint $(I_TEST_DIR)/rpg --rcfile=.pylintrc --output-format=json --output=$(T1_LOG) --exit-zero
	@(cat $(T1_LOG) | $(JQ) 'map(.symbol) | unique') >$(T1_LOG).json
	@cat $(T1_LOG).json

# -----------------------------------------------------------------------------------------------------------------
# -----------------------       (Makefile helpers and decoration)      --------------------------------------------
# -- Copied from https://github.com/awinecki/magicfile/blob/c0d1acc141a285e60b5d3fade7a7b8994f033380/Makefile --
# -----------------------------------------------------------------------------------------------------------------

.DEFAULT_GOAL := help
# check https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
NC = \033[0m
ERR = \033[31;1m
TAB := '%-20s' # Increase if you have long commands

# tput colors
red := $(shell tput setaf 1)
green := $(shell tput setaf 2)
yellow := $(shell tput setaf 3)
blue := $(shell tput setaf 4)
cyan := $(shell tput setaf 6)
cyan80 := $(shell tput setaf 86)
grey500 := $(shell tput setaf 244)
grey300 := $(shell tput setaf 240)
bold := $(shell tput bold)
underline := $(shell tput smul)
_r := $(shell tput sgr0)  # reset terminal styling

help:
	@printf '\n'
	@printf '    $(underline)$(grey500)Available make commands:$(_r)\n\n'
	@# Print non-check commands with comments
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:.+#.+$$' $(MAKEFILE_LIST) \
		| grep -v '^check-' \
		| grep -v '^env-' \
		| grep -v '^arg-' \
		| sed 's/:.*#/: #/g' \
		| awk 'BEGIN {FS = "[: ]+#[ ]+"}; \
		{printf " $(grey300)   make $(_r)$(cyan80)$(bold)$(TAB) $(_r)$(grey300)# %s$(_r)\n", $$1, $$2}'
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:( +\w+-\w+)*$$' $(MAKEFILE_LIST) \
		| grep -v help \
		| awk 'BEGIN {FS = ":"}; \
		{printf " $(grey300)   make $(_r)$(cyan80)$(bold)$(TAB)$(_r)\n", $$1}'
	@echo "\n    $(underline)$(grey500)Helper/Checks$(_r)\n"
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:.+#.+$$' $(MAKEFILE_LIST) \
		| grep -E '^(check|arg|env)-' \
		| awk 'BEGIN {FS = "[: ]+#[ ]+"}; \
		{printf " $(grey300)   make $(_r)$(grey500)$(TAB) $(_r)$(grey300)# %s$(_r)\n", $$1, $$2}'
	@echo ""
