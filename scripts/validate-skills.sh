#!/bin/sh

# Validate the portable metadata and local links for every catalog skill.
set -u

root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd) || exit 1
skills_dir=$root/skills
failed=0
count=0

if [ ! -d "$skills_dir" ]; then
  printf '%s\n' "Validation failed: skills/ directory does not exist" >&2
  exit 1
fi

for package in "$skills_dir"/*; do
  [ -d "$package" ] || continue
  file=$package/SKILL.md
  name=$(basename "$package")
  count=$((count + 1))

  if [ ! -f "$file" ]; then
    printf 'FAIL %s: missing SKILL.md\n' "$name" >&2
    failed=1
    continue
  fi

  frontmatter_errors=$(awk '
    function trim(value) {
      sub(/^[[:space:]]+/, "", value)
      sub(/[[:space:]]+$/, "", value)
      return value
    }
    function usable(value) {
      value = trim(value)
      if (value ~ /^".*"$/ || value ~ /^\047.*\047$/) {
        value = substr(value, 2, length(value) - 2)
        value = trim(value)
      }
      return value != "" && value !~ /^(null|Null|NULL|~)$/
    }
    NR == 1 {
      if ($0 != "---") print "frontmatter must start and end with --- delimiters"
      next
    }
    !closed && $0 ~ /^---[[:space:]]*$/ { closed = 1; next }
    !closed {
      for (i = 1; i <= 3; i++) {
        field = (i == 1 ? "name" : (i == 2 ? "description" : "license"))
        if ($0 ~ "^" field ":[[:space:]]*") {
          value = $0
          sub("^" field ":[[:space:]]*", "", value)
          values[field] = value
        }
      }
    }
    END {
      if (!closed) print "frontmatter must start and end with --- delimiters"
      for (i = 1; i <= 3; i++) {
        field = (i == 1 ? "name" : (i == 2 ? "description" : "license"))
        if (!(field in values) || !usable(values[field]))
          print "frontmatter " field " is empty or missing"
      }
    }
  ' "$file")
  if [ -n "$frontmatter_errors" ]; then
    printf '%s\n' "$frontmatter_errors" | while IFS= read -r error; do
      printf 'FAIL %s: %s\n' "$name" "$error" >&2
    done
    failed=1
  fi

  # Extract Markdown destinations from [text](destination), then check only
  # relative file paths. URLs, anchors, and mail addresses are external.
  awk '
    /^[[:space:]]*(```|~~~)/ { in_fence = !in_fence; next }
    in_fence { next }
    { line = $0; while (match(line, /\[[^]]*\]\([^)]*\)/)) {
        link = substr(line, RSTART, RLENGTH)
        sub(/^.*\]\(/, "", link); sub(/\)$/, "", link)
        sub(/[[:space:]].*$/, "", link)
        if (link !~ /^(https?:|mailto:|#|\/)/ && link != "") print link
        line = substr(line, RSTART + RLENGTH)
      }
    }
  ' "$file" | while IFS= read -r target; do
    case "$target" in
      *'#'*) target=${target%%#*} ;;
    esac
    [ -n "$target" ] || continue
    if [ ! -e "$package/$target" ]; then
      printf 'FAIL %s: Markdown link does not exist: %s\n' "$name" "$target" >&2
      # The pipeline runs in a subshell; emit a marker for the parent shell.
      printf '%s\n' "$name" >> "$root/.validate-skills-failed"
    fi
  done
  if [ -f "$root/.validate-skills-failed" ]; then
    failed=1
    rm -f "$root/.validate-skills-failed"
  fi
done

if [ "$count" -eq 0 ]; then
  printf '%s\n' 'Validation failed: no skill packages found' >&2
  exit 1
fi

if [ "$failed" -ne 0 ]; then
  exit 1
fi
printf 'Validated %s skill package(s).\n' "$count"
