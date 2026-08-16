# Git Instructions

## Rules

Agents MUST:
- Inspect git status before making significant changes.
- Preserve existing uncommitted changes.
- Avoid overwriting user changes.
- Review git diff after modifications.

Agents MUST NOT automatically:
- git push
- git commit
- git reset --hard
- git clean -fd
- delete branches
- force push
- discard user changes
- overwrite unrelated modifications

## Destructive Operations

If a potentially destructive Git operation is required:
STOP and ask the user for confirmation.

Never assume that uncommitted changes belong to the Agent.
