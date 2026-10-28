"""Canonical managed routing section for consumer AGENTS.md files."""

START = "<!-- ADE ROUTING START v1 -->"
END = "<!-- ADE ROUTING END -->"
BLOCK = """<!-- ADE ROUTING START v1 -->
## ADE skill selection

This repository uses the Agentic Development Environment. For each coding task,
consult `.agentic-dev/skill-map.json` and choose the relevant **installed**
primary skill. Supporting skills are optional; do not invoke absent skills.
Read its SKILL.md and follow relevant project rules. Descriptions are guidance,
not a guarantee that a model will select the correct skill automatically.

Before claiming completion, run the configured ADE checks where available;
missing, failed, or blocked checks are never passing evidence. Merging,
deploying, force pushing and changing production data require explicit
human authorization.
<!-- ADE ROUTING END -->
"""

def managed_instructions(existing: bytes) -> bytes:
    """Preserve all unrelated bytes and refuse edits to an ADE-owned block."""
    if b"\x00" in existing:
        raise ValueError("AGENTS.md appears binary")
    try:
        text = existing.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("AGENTS.md is not UTF-8") from exc
    a, b = text.count(START), text.count(END)
    if a != b or a > 1:
        raise ValueError("AGENTS.md has malformed ADE routing markers")
    if a:
        first = text.index(START)
        last = text.index(END, first) + len(END)
        if text[first:last] != BLOCK.rstrip("\n"):
            raise ValueError("Existing ADE routing block was modified; manual review required")
        return existing
    suffix = "" if not text else ("\n" if text.endswith("\n\n") else "\n\n" if not text.endswith("\n") else "\n")
    return existing + suffix.encode("utf-8") + BLOCK.encode("utf-8")
