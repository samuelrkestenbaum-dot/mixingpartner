
<!-- BUILD-OS:START (managed by install-project.sh) -->
## Build OS (project scope)

This repository runs a native **Build OS** orchestrator, vendored into the repo
at **project scope** (`.claude/` + `build-os/`) so it loads in **every** Claude
Code session on this repo — local, web, or remote — at clone time. Use the
**build-orchestrator** subagent **proactively at session start** and before any
build packet (architecture, next steps, tool routing, or "keep going"). The
orchestrator routes; it never implements. Implementation goes through
**builder**, proof through **qa**, judgment through **reviewer**, and closure
through **archivist**.

This project's state lives in `build-os/` (`build-os/memory/`,
`build-os/packets/`, `build-os/receipts/`). The orchestrator reads it at session
start and the archivist advances it on every packet close.

### Per-task protocol

1. **Classify** the task type and its authority.
2. **Read the router** — `build-os/memory/tool_router.md` (this project's, if
   present) — and pick the matching row.
3. **Declare a Tool Budget** — the exact tools/agents you will use.
4. **Announce** it on one line: `Tools: [x] — why`.
5. **Budget breach = stop.** Needing a tool or authority outside the declared
   budget is a hard stop for explicit go, not a silent expansion.
6. **Close with a receipt** via the archivist (`build-os/receipts/<id>.md`).

### Hard gates

- **Design / UI** work is **frontend only**.
- **Marketing / media** work happens **only inside marketing/media packets**.
- **Agent swarm** is allowed **only for parallelizable work and only with an
  explicit merge plan**.
- **No external mutation without explicit go** — never push, merge, deploy,
  publish, or touch secrets without an explicit go from the user.

### Working contract

- **Verify the branch base** (`git merge-base`) before building.
- **≤2 commits** per packet; **Commit-1 green in isolation**.
- **Full proof + safety grep** before a packet closes (qa reports exact counts).
- **Never merge/push/deploy without go.**
<!-- BUILD-OS:END -->
