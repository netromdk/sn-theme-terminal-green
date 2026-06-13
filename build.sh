#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v npm &>/dev/null; then
  echo "Error: npm is not installed"
  exit 1
fi

# Install sass locally into node_modules/ if not already present.
if [ ! -x node_modules/.bin/sass ]; then
  echo "Installing sass locally..."
  npm install
fi

npm run build
echo "Built: dist/dist.css and dist/dist.min.css"
