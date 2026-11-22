#!/usr/bin/env bash
# Deploy script for Ashish Kulkarni's personal website & Notes blog

set -e

echo "Building static site..."
python3 build.py

echo "Committing source changes to main..."
git add -A
if ! git diff-index --quiet HEAD --; then
  COMMIT_MSG="${1:-Update website and blog content}"
  git commit -m "$COMMIT_MSG"
fi

echo "Pushing main branch..."
git push origin main

echo "Deploying dist/ to GitHub Pages (gh-pages branch)..."
git subtree push --prefix dist origin gh-pages

echo "✓ Deployment complete! Live at: https://ashish-mk.github.io/"
