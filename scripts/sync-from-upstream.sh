#!/usr/bin/env bash
# ABOUTME: Pull latest from the upstream eda template repo and sanity-check for personal refs
# ABOUTME: Usage: bash scripts/sync-from-upstream.sh

set -euo pipefail

UPSTREAM_REMOTE="upstream"
BRANCH="main"
CHECKER="scripts/check-personal-refs.sh"
REPO_ROOT="$(git rev-parse --show-toplevel)"

# ── 1. Verify upstream remote exists ────────────────────────────────────────
if ! git remote get-url "$UPSTREAM_REMOTE" &>/dev/null; then
    echo "❌ Remote '$UPSTREAM_REMOTE' not found."
    echo "   Add it with:"
    echo "   git remote add upstream /path/to/claude-databricks-eda"
    exit 1
fi

echo "📡 Fetching from $UPSTREAM_REMOTE..."
git fetch "$UPSTREAM_REMOTE"

# ── 2. Preview what's coming in ──────────────────────────────────────────────
INCOMING=$(git log HEAD.."$UPSTREAM_REMOTE/$BRANCH" --oneline)
if [[ -z "$INCOMING" ]]; then
    echo "✅ Already up to date with $UPSTREAM_REMOTE/$BRANCH."
    exit 0
fi

echo ""
echo "Incoming commits:"
echo "$INCOMING" | sed 's/^/  /'
echo ""

# ── 3. Sanity-check upstream for personal refs before merging ────────────────
echo "🔍 Checking upstream/$BRANCH for personal references..."
TMPDIR_WORKTREE=$(mktemp -d)
git worktree add "$TMPDIR_WORKTREE" "$UPSTREAM_REMOTE/$BRANCH" 2>/dev/null

cleanup() { git worktree remove --force "$TMPDIR_WORKTREE" 2>/dev/null || true; }
trap cleanup EXIT

CHECK_RESULT=0
# Pass our local patterns file so the checker in the worktree knows what to look for
(cd "$TMPDIR_WORKTREE" && PERSONAL_REFS_FILE="$REPO_ROOT/scripts/.personal-refs" bash "$CHECKER") || CHECK_RESULT=$?

if [[ $CHECK_RESULT -ne 0 ]]; then
    echo ""
    echo "⛔ Aborting sync — fix personal references in upstream before merging."
    exit 1
fi

# ── 4. Merge ─────────────────────────────────────────────────────────────────
echo ""
echo "✅ Check passed. Merging $UPSTREAM_REMOTE/$BRANCH..."
git merge "$UPSTREAM_REMOTE/$BRANCH" --no-ff -m "chore: sync from upstream eda template"

echo ""
echo "✅ Sync complete. Review the merge, then: git push"
