# andara.solo7.media

Game content for Andara's World: Builder packs in the Andara Content Language, compiled with `andara-cli` from the [andara.valesordev.com](https://github.com/valesordev/andara.valesordev.com) release named in `andara.ref` (`cli-dev` for now).

```bash
make tools    # once per clone, and after andara.ref changes: downloads andara-cli, verifies its checksum
make check    # what CI runs on every PR and on main
```

`make tools` needs only `make`, `curl` and `tar`, no Go and no access to the server repo. To build `andara-cli` from a server clone instead (for changing the Content Language; needs Go), run `make tools ANDARA_SRC=../andara.valesordev.com`.

Canon and design docs live in `docs/` (see `CLAUDE.md`); this repo is authoritative for them. Concept-art images in `docs/art/img/` and `docs/art/inbox/` (drop your own there under any name) are stored with Git LFS: run `git lfs install` once per machine before cloning.

Each `content/<pack>/` holds one pack, and the directory name must match the `pack` declaration in its `pack.aw`. A pack's Zone IDs must not collide with the dev fixture's (`town`, `docks`, `wilds`, `purgatory`); the server refuses the collision at load time, and `check` can't see it.

`main` is protected: changes land by pull request, with signed commits and a passing `check`.

See `CLAUDE.md` for layout and rules. Agent config is installed from automate.system9studios.com (`make install TARGET=andara-content DEST=$PWD`).
