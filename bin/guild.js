#!/usr/bin/env node
/**
 * Guild installer CLI.
 *
 * Thin Node wrapper over scripts/install.sh so Guild can be installed via
 *   npx @ayesel/guild [target] [--mode guild|bmad|full|auto]
 *
 * install.sh remains the single source of truth for what gets copied; this
 * wrapper only resolves the package root + target directory and shells out
 * to bash with stdio inherited (so interactive mode prompts still work).
 */
'use strict';

const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

const PKG_ROOT = path.resolve(__dirname, '..');
const INSTALLER = path.join(PKG_ROOT, 'scripts', 'install.sh');

function readVersion() {
  try {
    return require(path.join(PKG_ROOT, 'package.json')).version;
  } catch {
    return 'unknown';
  }
}

function printHelp() {
  console.log(`Guild — AI-powered design framework installer

Usage:
  npx @ayesel/guild [target-dir] [options]

Arguments:
  target-dir            Project to install Guild into (default: current directory)

Options:
  --mode <mode>         guild | bmad | full | auto  (default: auto)
  -v, --version         Print Guild version and exit
  -h, --help            Show this help

Examples:
  npx @ayesel/guild                       # install into the current project (auto-detect)
  npx @ayesel/guild ./my-app --mode guild # Guild design agents only
  npx @ayesel/guild ./my-app --mode full  # Guild + BMAD dev pipeline
`);
}

function main() {
  const argv = process.argv.slice(2);

  if (argv.includes('-h') || argv.includes('--help')) {
    printHelp();
    process.exit(0);
  }
  if (argv.includes('-v') || argv.includes('--version')) {
    console.log(readVersion());
    process.exit(0);
  }

  // Split target (first non-flag token) from passthrough flags.
  let target = process.cwd();
  const passthrough = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--mode') {
      passthrough.push(a, argv[i + 1]);
      i++;
    } else if (a.startsWith('-')) {
      passthrough.push(a);
    } else if (target === process.cwd() && !passthrough.includes('--target-set')) {
      target = path.resolve(a);
      passthrough.push('--target-set'); // sentinel so only the first bare arg is the target
    }
  }
  const cleanPassthrough = passthrough.filter((x) => x !== '--target-set');

  if (!fs.existsSync(INSTALLER)) {
    console.error(`Error: installer not found at ${INSTALLER}. The package may be corrupted — try reinstalling.`);
    process.exit(1);
  }

  const result = spawnSync('bash', [INSTALLER, target, ...cleanPassthrough], {
    stdio: 'inherit',
    cwd: PKG_ROOT,
  });

  if (result.error) {
    if (result.error.code === 'ENOENT') {
      console.error('Error: `bash` is required to run the Guild installer but was not found on PATH.');
      console.error('On Windows, run this from Git Bash or WSL.');
    } else {
      console.error(`Error running installer: ${result.error.message}`);
    }
    process.exit(1);
  }
  process.exit(result.status === null ? 1 : result.status);
}

main();
