# Homebrew packaging

This directory holds the scaffolding required to publish `docrest` through a
[Homebrew tap](https://docs.brew.sh/Taps). It does **not** publish anything by
itself — it is meant to be used together with a separate tap repository.

## One-time setup

1. **Create a GitHub release** in this repository for the version you want to
   publish (e.g. `v0.1.0`). Make sure the source tarball at
   `https://github.com/<user>/docrest/archive/refs/tags/v0.1.0.tar.gz`
   resolves and download it locally:

   ```bash
   curl -L -o docrest-0.1.0.tar.gz \
       https://github.com/<user>/docrest/archive/refs/tags/v0.1.0.tar.gz
   shasum -a 256 docrest-0.1.0.tar.gz
   ```

2. **Create a tap repository** on GitHub. The repository name **must** start
   with `homebrew-` (e.g. `homebrew-docrest`). Inside it create a directory
   called `Formula/`.

3. **Copy `docrest.rb`** from this directory into `Formula/docrest.rb` in the
   tap repository.

4. **Update the placeholders** at the top of the formula:
   - `homepage` — point to the docrest GitHub repo.
   - `url` — release tarball URL.
   - `sha256` — the value printed by `shasum -a 256` above.

5. **Generate the `resource` blocks**:

   ```bash
   pipx install homebrew-pypi-poet     # one-time
   packaging/homebrew/generate_resources.sh > /tmp/docrest-resources.rb
   ```

   Paste the contents of `/tmp/docrest-resources.rb` into `Formula/docrest.rb`
   between the `# RESOURCES START` and `# RESOURCES END` markers.

6. **Validate locally**:

   ```bash
   brew install --build-from-source ./Formula/docrest.rb
   brew test docrest
   brew audit --new --formula docrest
   ```

7. **Push** the tap repository. End users can now run:

   ```bash
   brew tap <github-user>/docrest
   brew install docrest
   ```

## Releasing a new version

For each subsequent docrest release:

1. Cut a new git tag and GitHub release.
2. Update `url` + `sha256` in the formula.
3. Re-run `generate_resources.sh` (Python dependency pins may have changed) and
   replace the resource block.
4. Run `brew test docrest` locally, then push the tap.

## Why not `homebrew-core`?

Submitting to `homebrew-core` requires a stable project with notable usage and
passes a stricter audit. Once docrest has real adoption, you can submit a PR to
`homebrew/homebrew-core` so users can `brew install docrest` without tapping.
The formula in this directory is structured so the move would be mostly a copy.

## Optional runtime tools

The formula depends on `pandoc` and `pango` (for WeasyPrint). The other
optional tools used by docrest are intentionally not declared as Homebrew
dependencies:

- `mmdc` (Mermaid CLI) — distributed via npm, requires a Node.js runtime.
- `plantuml` — pulls in a Java runtime.

Users install them on demand using `docrest install mmdc` / `docrest install
plantuml`.
