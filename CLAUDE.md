# CLAUDE.md - Guidelines for Claude Code

This file provides quick-reference commands and execution standards for Claude Code when working with PhoneFix.

## Quick CLI Commands
- Check attached devices: `python3 -m phone_fix devices`
- Run non-destructive scan: `python3 -m phone_fix scan --output device_health_report.md`
- Run verified optimizations: `python3 -m phone_fix optimize --yes --output optimization_benchmark.md`
- Restore uninstalled packages: `python3 -m phone_fix rollback <package_names...>`
- Run unit test suite: `pytest -v`

## Core Workflow
1. Always check `python3 -m phone_fix devices` first.
2. If unauthorized, guide the user to accept the USB debugging RSA key prompt.
3. Always run `scan` and present the health report before running `optimize`.
4. Never delete personal user files or vault folders (`.safebox`, `secretAlbum`).
5. Only run `optimize` after explicit user agreement.
