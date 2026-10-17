SHELL       := bash
.SHELLFLAGS := -euo pipefail -c

# The server repo owns the Content Language, andara-cli, and andara.core.
# Packs here are checked with the andara-cli release named in andara.ref.
ANDARA_GH   := valesordev/andara.valesordev.com
ANDARA_REF  ?= $(strip $(file < andara.ref))
RELEASES    ?= https://github.com/$(ANDARA_GH)/releases/download
TOOLS       := .tools
# Set ANDARA_SRC to a server clone to build andara-cli from it instead of
# downloading the release (e.g. make tools ANDARA_SRC=../andara.valesordev.com).
# For changing the Content Language; needs Go. CI never uses it.
ANDARA_SRC  ?=
CLI         := $(CURDIR)/$(TOOLS)/bin/andara-cli
SPEC        := $(TOOLS)/spec/content-language
CORE_VERSION ?= 1
export ANDARA_CONTENT_CACHE := $(CURDIR)/$(TOOLS)/cache
PACKS       := $(patsubst %/,%,$(sort $(dir $(wildcard content/*/pack.aw))))
TAG         ?= cli-dev

.PHONY: help tools seed check check-lore check-packs check-fmt compile fmt pin packs clean need-cli

help: ## List targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-11s %s\n", $$1, $$2}'

tools: ## Install andara-cli from the release in andara.ref (or build it from ANDARA_SRC); cache andara.core
	@mkdir -p $(TOOLS)/bin
ifdef ANDARA_SRC
	go build -C $(ANDARA_SRC) -o $(CLI) ./cmd/andara-cli
	@$(MAKE) --no-print-directory seed SRC=$(abspath $(ANDARA_SRC))
	@echo "andara-cli built from $$(git -C $(ANDARA_SRC) rev-parse --short HEAD) (ANDARA_SRC=$(ANDARA_SRC))"
else
	@os=$$(uname -s | tr '[:upper:]' '[:lower:]'); \
	case $$(uname -m) in x86_64|amd64) arch=amd64 ;; aarch64|arm64) arch=arm64 ;; *) arch=$$(uname -m) ;; esac; \
	base=$(RELEASES)/$(ANDARA_REF); \
	tmp=$$(mktemp -d); trap 'rm -rf "$$tmp"' EXIT; \
	curl -fsSL -o "$$tmp/SHA256SUMS" "$$base/SHA256SUMS"; \
	read -r sum file < <(awk -v s="_$${os}_$${arch}.tar.gz" \
	  '{ f = $$2; sub(/^\*/, "", f) } f ~ /^andara-cli_/ && substr(f, length(f) - length(s) + 1) == s { print $$1, f; exit }' \
	  "$$tmp/SHA256SUMS") || true; \
	[ -n "$${file:-}" ] || { echo "tools: no andara-cli archive for $${os}_$${arch}" >&2; exit 1; }; \
	curl -fsSL -o "$$tmp/$$file" "$$base/$$file"; \
	got=$$({ sha256sum "$$tmp/$$file" 2>/dev/null || shasum -a 256 "$$tmp/$$file"; } | cut -d' ' -f1); \
	[ "$$got" = "$$sum" ] || { echo "tools: checksum mismatch for $$file" >&2; exit 1; }; \
	tar -xzf "$$tmp/$$file" -C "$$tmp" andara-cli; \
	install -m 0755 "$$tmp/andara-cli" $(CLI); \
	echo "andara-cli $$($(CLI) version | awk '$$1 == "version:" { print $$2 }') from release $(ANDARA_REF) ($$file, sha256 ok)"
# INTERIM until AW-CLI-002: the binary doesn't embed andara.core or ship the
# spec yet, so fetch the server source at the binary's commit, once.
	@commit=$$($(CLI) version | awk '$$1 == "commit:" { print $$2 }'); \
	tmp=$$(mktemp -d); trap 'rm -rf "$$tmp"' EXIT; \
	curl -fsSL -o "$$tmp/src.tar.gz" https://codeload.github.com/$(ANDARA_GH)/tar.gz/$$commit; \
	top=$$(tar -tzf "$$tmp/src.tar.gz" | awk -F/ 'NR == 1 { print $$1 }'); \
	tar -xzf "$$tmp/src.tar.gz" -C "$$tmp" "$$top/content/core" "$$top/docs/specs/content-language"; \
	$(MAKE) --no-print-directory seed SRC="$$tmp/$$top"
endif

# INTERIM until AW-CLI-002: seed the andara.core cache and the spec from a
# server source tree (SRC). Dropped once the binary embeds core.
# andara.core ships compiled until its .aw sources land (content/core/README.md);
# fetch-core --from needs sources, so copy the compiled templates into the cache.
# Drop this fallback when valesordev/andara.valesordev.com#152 is fixed.
seed:
	@core=$(SRC)/content/core; \
	if compgen -G "$$core/*.aw" >/dev/null || compgen -G "$$core/**/*.aw" >/dev/null; then \
	  $(CLI) content fetch-core --from $$core --version $(CORE_VERSION); \
	else \
	  dest=$(ANDARA_CONTENT_CACHE)/andara.core@$(CORE_VERSION)/templates; \
	  rm -rf $$dest && mkdir -p $$dest && cp $$core/templates/*.json $$dest/; \
	  echo "cached andara.core@$(CORE_VERSION) from compiled seed: $$(ls $$dest | wc -l) templates in $$dest"; \
	fi
	@rm -rf $(SPEC) && mkdir -p $(dir $(SPEC)) && cp -R $(SRC)/docs/specs/content-language $(SPEC)
	@echo "spec: $(SPEC)/"

check: check-lore check-packs check-fmt compile ## Everything a PR must pass; what CI runs

check-lore: ## Validate canon and design docs (BASE=origin/main also lists status changes since it)
	@test -x .claude/bin/lore-check || { echo "lore-check missing: run make install TARGET=andara-content from automate.system9studios.com"; exit 1; }
	.claude/bin/lore-check $(if $(BASE),--changes $(BASE))

check-packs: ## Fail when a content/ directory's name differs from its pack declaration
	@fail=0; for p in $(PACKS); do \
	  id=$$(awk '$$1 == "pack" { print $$2; exit }' $$p/pack.aw); \
	  [ "$$id" = "$${p#content/}" ] || { echo "check: $$p declares pack $$id" >&2; fail=1; }; \
	done; exit $$fail

check-fmt: need-cli ## Fail if any pack isn't in canonical form
	@for p in $(PACKS); do $(CLI) content fmt --check --path $$p; done

compile: need-cli ## Compile every pack to build/<pack>/
	@if [ -z "$(PACKS)" ]; then echo "no packs yet (content/<pack>/pack.aw)"; fi
	@for p in $(PACKS); do $(CLI) content compile --path $$p --out build/$$(basename $$p); echo "ok  $$p"; done

fmt: need-cli ## Rewrite every pack to canonical form
	@for p in $(PACKS); do $(CLI) content fmt --path $$p; done

packs: ## List packs
	@printf '%s\n' $(PACKS)

pin: ## Write TAG (default cli-dev) to andara.ref (the owner's call; lands by PR)
	@echo $(TAG) > andara.ref
	@cat andara.ref

need-cli:
	@test -x $(CLI) || { echo "andara-cli not installed: run make tools"; exit 1; }

clean: ## Remove build output (keeps .tools/)
	rm -rf build
