#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS.txt
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
tar -xzf sys-protocol-001-evidence.tar.gz -C "$scratch"
cd "$scratch/sys-protocol-001"
./reproduce.sh
