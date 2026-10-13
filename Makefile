SHELL      := bash
.SHELLFLAGS := -euo pipefail -c
PLUGINS    := $(notdir $(wildcard plugins/*))
DIST       := dist
TOOLKIT    := .deps/valesordev/toolkit
TK         := python3 $(TOOLKIT)

.PHONY: help deps pin toolkit validate check-render build package package-done install check-target scaffold test dev clean

help: ## List targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-13s %s\n", $$1, $$2}'

deps: ## Check out each deps.json dependency into .deps/<name>/ at its ref (a symlink is left alone)
	@python3 -c 'import json; [print(n, d["repo"], d["ref"]) for n, d in json.load(open("deps.json")).items()]' | \
	while read -r name repo ref; do \
	  dir=.deps/$$name; \
	  if [ -L "$$dir" ]; then echo "  $$name: $$dir is a symlink, left alone"; continue; fi; \
	  case "$$repo" in *:*) url=$$repo ;; *) url=https://github.com/$$repo.git ;; esac; \
	  [ -d "$$dir/.git" ] || git clone -q "$$url" "$$dir"; \
	  test -z "$$(git -C $$dir status --porcelain)" || { echo "$$dir has local changes"; exit 1; }; \
	  git -C "$$dir" fetch -q --tags origin; \
	  git -C "$$dir" -c advice.detachedHead=false checkout -q --detach "$$ref^{commit}"; \
	  echo "  $$name @ $$ref ($$(git -C $$dir rev-parse --short HEAD))"; \
	done

pin: ## Move one dependency: make pin DEP=valesordev REF=<tag or commit>
	@test -n "$(DEP)" -a -n "$(REF)" || { echo "usage: make pin DEP=<name> REF=<tag or commit>"; exit 1; }
	@python3 -c 'import json, sys; n, r = sys.argv[1:]; d = json.load(open("deps.json")); d[n]["ref"] = r; open("deps.json", "w").write(json.dumps(d, indent=2) + "\n")' $(DEP) $(REF)
	@$(MAKE) -s deps

toolkit:
	@test -d $(TOOLKIT) || { echo "no toolkit at $(TOOLKIT): run \`make deps\`"; exit 1; }

validate: check-render ## claude plugin validate + authoring conventions (examples, skill limits, assist levels, README tables)
	claude plugin validate .
	@for p in $(PLUGINS); do claude plugin validate plugins/$$p; done
	@$(TK)/check_conventions.py --root $(CURDIR)

check-render: toolkit ## Fail if any plugins/*/src/** render is stale
	@for p in $(PLUGINS); do $(TK)/render.py --root $(CURDIR) --check plugins/$$p; done

build: toolkit ## Render plugins/*/src/** in place, and instructions/* with shared/ inlined into dist/<plugin>/
	@for p in $(PLUGINS); do $(TK)/render.py --root $(CURDIR) --tree plugins/$$p; done
	@for f in $(wildcard plugins/*/instructions/*); do \
	  p=$$(echo $$f | cut -d/ -f2); out=$(DIST)/$$p/$$(basename $${f%.tmpl}); \
	  $(TK)/render.py --root $(CURDIR) $$f $$out && echo "  $$out"; \
	done

package: toolkit ## Build, zip changed skills to dist/skills/, list changed Project instructions (ALL=1 for everything)
	@$(MAKE) -s build >/dev/null
	@$(TK)/package.py --root $(CURDIR) $(if $(ALL),--all)

package-done: toolkit ## Record the current skills and Project instructions as uploaded to claude.ai
	@$(TK)/package.py --root $(CURDIR) --done

install: toolkit ## Vendor a target into a repo's .claude/: make install TARGET=andara-content DEST=../andara.solo7.media
	@test -n "$(TARGET)" -a -n "$(DEST)" || { echo "usage: make install TARGET=<targets/ name> DEST=<repo path>"; exit 1; }
	$(TK)/install.py --root $(CURDIR) $(TARGET) $(DEST)

check-target: toolkit ## Report drift between a target repo and this repo: make check-target TARGET=… DEST=…
	@test -n "$(TARGET)" -a -n "$(DEST)" || { echo "usage: make check-target TARGET=<name> DEST=<repo path>"; exit 1; }
	$(TK)/install.py --root $(CURDIR) --check $(TARGET) $(DEST)

scaffold: toolkit ## New repo from scaffolds/: make scaffold NAME=andara-content DEST=… [INTO=1 for an existing git repo]
	@test -n "$(NAME)" -a -n "$(DEST)" || { echo "usage: make scaffold NAME=<scaffolds/ name> DEST=<repo path> [INTO=1]"; exit 1; }
	$(TK)/scaffold.py --root $(CURDIR) $(if $(INTO),--into) $(NAME) $(DEST)

test: toolkit ## Run install/role/plugin tests, plus each scaffold's own tests
	python3 -m unittest discover -s tests -v
	@for s in $(wildcard scaffolds/*/tests); do (cd $$(dirname $$s) && python3 -m unittest discover -s tests); done

dev: ## Register this checkout as local marketplace "system9studios" (plugins load in place)
	claude plugin marketplace add $(CURDIR)

clean: ## Remove build output
	rm -rf $(DIST)
