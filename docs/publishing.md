# Publishing Guild to npm

The package is **publish-ready** (`npm pack --dry-run` clean, bin self-tests
green, 1.2 MB tarball, 836 files). What's left is one user-side action.

## One-time setup

If you haven't published to npm before, or under the `@ayesel` scope:

```bash
# 1. Log in (opens a browser)
npm login

# 2. If @ayesel doesn't exist yet on npm, create it:
#    https://www.npmjs.com/org/create
#    (orgs of <= 5 members are free for public packages)
```

Verify you're logged in to the right account:

```bash
npm whoami
# expected: ayesel
```

## Publish

From the repo root (`/Users/bigdavis/Developer/frameworks/guild-bmad`):

```bash
# Final dry-run (always — confirms exactly what'll be shipped)
npm pack --dry-run | tail -20

# Confirm the integrity validator is green
./scripts/validate.sh

# Publish (scoped packages need --access public by default)
npm publish --access public
```

If the publish succeeds, `npx @ayesel/guild` will work for the world within a
minute. Verify:

```bash
# In a fresh terminal:
mkdir /tmp/test-install && cd /tmp/test-install
npx @ayesel/guild --version    # expected: 0.1.0
```

## After publishing

1. **Bump the version on the next release** — edit `package.json` (`0.1.0` →
   `0.1.1` for fixes, `0.2.0` for features), commit, then `npm publish` again.
   npm refuses to re-publish the same version.
2. **Tag the release in git** so origin/main has a corresponding tag:
   ```bash
   git tag v0.1.0 && git push origin v0.1.0
   ```
3. **Update the README badge** from `research preview` (orange) to `stable`
   (green) once you've verified at least one external install from npm worked.

## If something goes wrong

- **`E403 - 403 You don't have permission`** — the `@ayesel` scope likely
  isn't yours yet. Create it at <https://www.npmjs.com/org/create>.
- **`E402 - 402 Payment Required`** — scoped packages are free for public
  visibility, but the publish must include `--access public`. Re-run with it.
- **`E409 - 409 Conflict`** — the version is already published. Bump the
  version in `package.json`.
- **Cannot publish because of files-not-included** — check `package.json`'s
  `files` allowlist. The current setup ships `bin/`, `scripts/install.sh`,
  `scripts/validate.sh`, `guild.config.yaml`, `_bmad/`, `src/`, `.claude/`,
  `.cursor/`, `.gemini/`, `bmad-bundle/`. If you add a new top-level path
  Guild needs at install time, add it to `files` too.

## Unpublish (within 72h, last resort)

```bash
npm unpublish @ayesel/guild@0.1.0
```

Past 72h, npm restricts unpublishing to prevent breaking dependents. Bumping
the version and publishing a fix is the normal path.
