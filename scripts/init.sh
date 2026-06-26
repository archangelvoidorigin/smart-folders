#!/usr/bin/env bash
# Smart Folder Init — thin shim
# Usage: bash scripts/init.sh [folder_name] [role] [depth]
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

FOLDER_NAME=${1:-"my-folder"}
ROLE=${2:-"Custom"}
DEPTH=${3:-"medium"}

PYTHONPATH="$PROJECT_DIR:$PYTHONPATH" python -m smartfolders init "$FOLDER_NAME" --role "$ROLE" --depth "$DEPTH" --output .
