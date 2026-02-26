#!/usr/bin/env bash
# ABOUTME: Scan tracked files for personal/org-specific references before publishing
# ABOUTME: Exits 0 if clean, 1 if issues found. Safe to use as a pre-push hook.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Patterns file: override via PERSONAL_REFS_FILE env var (used by sync script
# when running in a worktree), otherwise default to sibling .personal-refs.
PATTERNS_FILE="${PERSONAL_REFS_FILE:-$SCRIPT_DIR/.personal-refs}"

if [[ ! -f "$PATTERNS_FILE" ]]; then
    echo "❌ Patterns file not found: $PATTERNS_FILE"
    echo "   Copy scripts/.personal-refs.template to scripts/.personal-refs"
    echo "   and add your personal identifiers (one grep pattern per line)."
    exit 1
fi

# Load patterns — skip blank lines and # comments (bash 3 compatible)
PATTERNS=()
while IFS= read -r line; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line//[[:space:]]/}" ]] && continue
    PATTERNS+=("$line")
done < "$PATTERNS_FILE"

if [[ ${#PATTERNS[@]} -eq 0 ]]; then
    echo "⚠️  No patterns in $PATTERNS_FILE — nothing to check."
    exit 0
fi

# Files/dirs to skip (credentials, binaries, generated, and this script itself)
EXCLUDE_PATHS=(
    ".git"
    ".venv"
    ".env"
    "uv.lock"
    "*.lock"
    "__pycache__"
    ".DS_Store"
    "*.pyc"
    "check-personal-refs.sh"
    ".personal-refs"
)

# Build the exclude args for grep
EXCLUDE_ARGS=()
for path in "${EXCLUDE_PATHS[@]}"; do
    EXCLUDE_ARGS+=(--exclude-dir="$path" --exclude="$path")
done

FOUND=0

for pattern in "${PATTERNS[@]}"; do
    matches=$(grep -rniI "${EXCLUDE_ARGS[@]}" "$pattern" . 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
        if [[ $FOUND -eq 0 ]]; then
            echo "❌ Personal references found:"
            echo ""
        fi
        echo "  Pattern: $pattern"
        while IFS= read -r line; do
            echo "    $line"
        done <<< "$matches"
        echo ""
        FOUND=1
    fi
done

if [[ $FOUND -eq 0 ]]; then
    echo "✅ No personal references found."
    exit 0
else
    echo "Fix the above before pushing to a shared/public repo."
    exit 1
fi
