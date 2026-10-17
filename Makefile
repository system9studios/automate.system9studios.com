SHELL      := bash
.SHELLFLAGS := -euo pipefail -c
PLUGINS    := $(notdir $(wildcard plugins/*))
DIST       := dist
TOOLKIT    := .deps/valesordev/toolkit
TK         := python3 $(TOOLKIT)

.PHONY: help deps pin toolkit validate check-public tools check-render build install check-target docs-export scaffold test dev clean

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

pin: ## Move one dependency: make pin DEP=valesordev REF=<tag or commit> [RELEASE=<vX.Y.Z>: PR, merge, tag this repo]
	@test -n "$(DEP)" -a -n "$(REF)" || { echo "usage: make pin DEP=<name> REF=<tag or commit> [RELEASE=<vX.Y.Z>]"; exit 1; }
	@if [ -n "$(RELEASE)" ]; then \
	  [[ "$(RELEASE)" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$$ ]] || { echo "RELEASE must be vX.Y.Z"; exit 1; }; \
	  [ "$$(git branch --show-current)" = main ] || { echo "RELEASE needs main checked out"; exit 1; }; \
	  test -z "$$(git status --porcelain)" || { echo "RELEASE needs a clean tree"; exit 1; }; \
	  git fetch -q --tags origin; \
	  [ "$$(git rev-parse HEAD)" = "$$(git rev-parse origin/main)" ] || { echo "main is not at origin/main: pull first"; exit 1; }; \
	  ! git rev-parse -q --verify "refs/tags/$(RELEASE)" >/dev/null || { echo "tag $(RELEASE) already exists"; exit 1; }; \
	fi
	@python3 -c 'import json, sys; n, r = sys.argv[1:]; d = json.load(open("deps.json")); d[n]["ref"] = r; open("deps.json", "w").write(json.dumps(d, indent=2) + "\n")' $(DEP) $(REF)
	@$(MAKE) -s deps
	@if [ -n "$(RELEASE)" ]; then \
	  ! git diff --quiet deps.json || { echo "deps.json unchanged: $(DEP) is already at $(REF)"; exit 1; }; \
	  repo=$$(python3 -c 'import json, sys; print(json.load(open("deps.json"))[sys.argv[1]]["repo"].rsplit("/", 1)[-1].removesuffix(".git"))' $(DEP)); \
	  branch=chore/$$repo-$(REF); msg="chore: $$repo $(REF)"; \
	  git switch -q -c "$$branch"; \
	  git commit -q -m "$$msg" deps.json; \
	  git push -q -u origin "$$branch"; \
	  gh pr create --base main --head "$$branch" --title "$$msg" --body "Pins $(DEP) to $(REF). Tagged $(RELEASE) on merge."; \
	  for _ in {1..24}; do \
	    out=$$(gh pr checks "$$branch" 2>&1 || true); \
	    [[ "$$out" == *"no checks reported"* ]] || break; \
	    sleep 5; \
	  done; \
	  gh pr checks "$$branch" --watch --fail-fast; \
	  gh pr merge "$$branch" --merge --delete-branch --match-head-commit "$$(git rev-parse "$$branch")"; \
	  git switch -q main; git pull -q --ff-only origin main; \
	  git branch -D "$$branch" >/dev/null 2>&1 || true; \
	  [ "$$(git rev-parse HEAD)" = "$$(git rev-parse origin/main)" ] || { echo "main is not at origin/main after merge: tag $(RELEASE) by hand"; exit 1; }; \
	  git tag -s $(RELEASE) -m "$(RELEASE): pin $(DEP) $(REF)"; \
	  git push -q origin $(RELEASE); \
	  echo "  $(RELEASE) tagged at $$(git rev-parse --short HEAD) and pushed"; \
	fi

toolkit:
	@test -d $(TOOLKIT) || { echo "no toolkit at $(TOOLKIT): run \`make deps\`"; exit 1; }

validate: check-render ## claude plugin validate + authoring conventions (examples, skill limits, assist levels, README tables)
	claude plugin validate .
	@for p in $(PLUGINS); do claude plugin validate plugins/$$p; done
	@$(TK)/check_conventions.py --root $(CURDIR)

check-public: tools ## Public-readiness gate: private Notion links, denylist (AUTOMATE_DENYLIST), gitleaks, setting terms [COMMITS=<range>] [NO_DENYLIST=1]
	$(TK)/check_public.py --root $(CURDIR) $(if $(COMMITS),--commits $(COMMITS)) $(if $(NO_DENYLIST),--no-denylist)
	python3 -m unittest discover -s tests -p test_targets.py -k SettingContentTest

tools: toolkit ## Fetch the pinned gitleaks into .tools/, checksum-verified
	@$(TK)/tools.py --root $(CURDIR)

check-render: toolkit ## Fail if any plugins/*/src/** render is stale
	@for p in $(PLUGINS); do $(TK)/render.py --root $(CURDIR) --check plugins/$$p; done

build: toolkit ## Render plugins/*/src/** in place
	@for p in $(PLUGINS); do $(TK)/render.py --root $(CURDIR) --tree plugins/$$p; done

install: toolkit ## Vendor a target into a repo's .claude/: make install TARGET=andara-content DEST=../andara.solo7.media
	@test -n "$(TARGET)" -a -n "$(DEST)" || { echo "usage: make install TARGET=<targets/ name> DEST=<repo path>"; exit 1; }
	$(TK)/install.py --root $(CURDIR) $(TARGET) $(DEST)

check-target: toolkit ## Report drift between a target repo and this repo: make check-target TARGET=… DEST=…
	@test -n "$(TARGET)" -a -n "$(DEST)" || { echo "usage: make check-target TARGET=<name> DEST=<repo path>"; exit 1; }
	$(TK)/install.py --root $(CURDIR) --check $(TARGET) $(DEST)

docs-export: toolkit ## Export docs/ to a site repo as content/<repo>/: make docs-export SITE=../solo7.media [DRY=1]
	@test -n "$(SITE)" || { echo "usage: make docs-export SITE=<site repo path> [DRY=1]"; exit 1; }
	$(TK)/export_docs.py --root $(CURDIR) $(if $(DRY),--dry-run) $(SITE)

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
