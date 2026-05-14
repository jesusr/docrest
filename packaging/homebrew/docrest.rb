# Template Homebrew formula for docrest.
#
# This file is a STARTING POINT. It is not a published formula — copy it into
# your tap repository (e.g. `homebrew-docrest/Formula/docrest.rb`) and then:
#
#   1. Replace `url` with the tarball URL of your GitHub release tag.
#   2. Update `sha256` with the SHA256 of that tarball
#      (`shasum -a 256 docrest-X.Y.Z.tar.gz`).
#   3. Replace the `# RESOURCES START` / `# RESOURCES END` block with the
#      output of `packaging/homebrew/generate_resources.sh`.
#
# Users will then install with:
#   brew tap <github-user>/docrest
#   brew install docrest
#
class Docrest < Formula
  include Language::Python::Virtualenv

  desc "Convert documentation between formats (md, docx, pdf, txt, diagrams)"
  homepage "https://github.com/REPLACE_ME/docrest"
  url "https://github.com/REPLACE_ME/docrest/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_TARBALL_SHA256"
  license "MIT"

  # Dependencies must be alphabetically ordered for `brew style`.
  depends_on "pandoc" # required for md <-> docx, docx -> pdf
  depends_on "pango"  # WeasyPrint runtime dependency for PDF output
  depends_on "python@3.13"

  # mmdc (Mermaid CLI) and plantuml are optional and installed at runtime via
  # `docrest install`, since neither has a stable Homebrew-only path that
  # avoids extra runtimes (Node.js / Java) you might not want pulled in.

  # RESOURCES START
  # Regenerate this block by running:
  #   packaging/homebrew/generate_resources.sh
  # The script prints `resource "name" do ... end` blocks for every runtime
  # dependency declared in pyproject.toml. Paste them between the START/END
  # markers.
  # RESOURCES END

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "docrest #{version}", shell_output("#{bin}/docrest --version")
    assert_match "Supported", shell_output("#{bin}/docrest formats")
    (testpath/"hello.md").write("# hello\n\nworld\n")
    system bin/"docrest", "convert", testpath/"hello.md", testpath/"hello.txt"
    assert_path_exists testpath/"hello.txt"
  end
end
