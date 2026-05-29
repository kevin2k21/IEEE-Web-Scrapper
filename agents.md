# AGENTS.md

This file is the shared, agent-facing entrypoint for this repository.

Canonical detailed guide:

- [agents.md](./agents.md)

Primary skill library:

- [skills/](./skills/)

## Recommended Loading Order

1. Read [agents.md](./agents.md) for role selection and collaboration guidance.
2. Load the role-specific folder under [skills/](./skills/).
3. Read `SKILL.md` first.
4. Read `references/playbook.md` only if deeper guidance is needed.

## Role Shortlist

- `product-manager`
- `ux-expert`
- `architect`
- `ui-developer`
- `backend-developer`
- `reviewer`
- `tester`
- `security-expert`
- `devsecops-platform`

## Repo Expectations For Any Agent

- inspect the current codebase before proposing large changes
- separate current behavior from proposed behavior
- keep outputs concrete and actionable
- call out risks, missing tests, and security implications when relevant
- avoid claiming undocumented or unimplemented capabilities
