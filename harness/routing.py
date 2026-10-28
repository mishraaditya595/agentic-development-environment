"""Conservative managed routing section: exact marker lines, normalized CRLF support."""
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
    if b"\x00" in existing:
        raise ValueError("AGENTS.md appears binary")
    try:
        text = existing.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("AGENTS.md is not UTF-8") from exc
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    lines = normalized.splitlines()
    starts = [i for i, line in enumerate(lines) if line == START]
    ends = [i for i, line in enumerate(lines) if line == END]
    if starts or ends:
        if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
            raise ValueError("AGENTS.md has invalid ADE routing marker order or count")
        actual = "\n".join(lines[starts[0]:ends[0]+1])
        if actual != BLOCK.rstrip("\n"):
            raise ValueError("Existing ADE routing block has been modified")
        return existing
    if newline == "\r\n" and "\n" in text.replace("\r\n", ""):
        raise ValueError("Mixed line endings in AGENTS.md")
    suffix = "" if not text else (newline if text.endswith(newline) else newline + newline)
    return existing + suffix.encode("utf-8") + BLOCK.replace("\n", newline).encode("utf-8")
