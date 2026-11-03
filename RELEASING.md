# Releasing TermForge to PyPI

Releases are published by `.github/workflows/release.yml` using
[PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC). No API token
or password is stored in GitHub. The workflow runs only when a tag matching `v*` is pushed.

## One-time setup (do this before the first release)

1. **Check the name.** `https://pypi.org/project/termforge/` should return 404 (it did when
   this was written). If someone has taken it since, pick another name, update `name` in
   `pyproject.toml`, and use that name below.
2. **Create a PyPI account** (and enable 2FA) at https://pypi.org/account/register/ if you
   do not have one.
3. **Add a pending trusted publisher**: https://pypi.org/manage/account/publishing/ ->
   "Add a new pending publisher" -> GitHub tab, and enter exactly:
   - PyPI Project Name: `termforge`
   - Owner: `maddoxk`
   - Repository name: `TermForge`
   - Workflow name: `release.yml`
   - Environment name: `pypi`

   A pending publisher reserves nothing until the first successful publish creates the project.
4. **Create the GitHub environment**: repo Settings -> Environments -> New environment ->
   name it exactly `pypi`. Recommended: add yourself under "Required reviewers" so every
   release needs one manual approval click before upload.

## Cutting a release

1. Bump `__version__` in `termforge/__init__.py` (the only place the version lives;
   `pyproject.toml` reads it). Add a `CHANGELOG.md` entry.
2. Merge that change to `main` via a PR (CI must be green).
3. Tag the merge commit and push the tag. The tag must be `v` + the exact version:
   ```bash
   git checkout main && git pull
   git tag v2.0.0
   git push origin v2.0.0
   ```
4. Watch the "Release to PyPI" run in the Actions tab. If you added required reviewers,
   approve the `publish` job when prompted. The workflow fails early if the tag does not
   match `__version__`.
5. Verify in a fresh venv: `pip install termforge==2.0.0 && python -c "import termforge"`.
6. Update the README install section to make `pip install termforge` the primary
   instruction and drop the "not on PyPI yet" note.

## Notes

- PyPI never lets you re-upload a version. If a release is broken, bump the version
  (e.g. `2.0.1`) and tag again; you can "yank" the bad one on pypi.org.
- To rehearse without risk, build locally: `python -m build && twine check --strict dist/*`
  and `scripts/check_installed_wheel.sh dist`. Do not run `twine upload` by hand.
