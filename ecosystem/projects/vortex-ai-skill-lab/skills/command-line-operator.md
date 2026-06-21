# Skill: Command-Line Operator

## Use When

Use this skill when working with Linux, WSL, Git, Makefile, tmux, logs, or runtime processes.

## Rules

- Check current directory first.
- Check git status before patching.
- Do not print secrets.
- Do not print .env.
- Use safe, reversible commands.
- Prefer status, smoke test, cleanup, then commit.
- Keep commands copyable.
- Validate results with clear PASS markers.

## Operator Pattern

1. Inspect
2. Diagnose
3. Patch small
4. Compile or smoke test
5. Cleanup generated noise
6. Commit
7. Record carry-over
