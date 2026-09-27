#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${VERSION:-2.0.0}"
ARCH="$(dpkg --print-architecture 2>/dev/null || uname -m)"
DIST_DIR="$ROOT_DIR/dist_linux"
WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/steghunter-build.XXXXXX")"
PACKAGE_ROOT="$WORK_DIR/deb-root"
APP_DIR="$PACKAGE_ROOT/opt/steg-hunter-pro"
trap 'rm -rf "$WORK_DIR"' EXIT

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Build this package on Linux; PyInstaller does not cross-compile." >&2
  exit 1
fi
if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller is missing. Install with: python -m pip install -e '.[linux-build]'" >&2
  exit 1
fi

cd "$ROOT_DIR"
mkdir -p "$DIST_DIR" "$WORK_DIR"
pyinstaller --clean --noconfirm \
  --distpath "$DIST_DIR" \
  --workpath "$WORK_DIR/pyinstaller" \
  StegHunter_Pro.spec

APP_BUNDLE="$DIST_DIR/StegHunter_Pro"
if [[ ! -x "$APP_BUNDLE/StegHunter_Pro" ]]; then
  echo "PyInstaller did not produce the expected Linux application bundle." >&2
  exit 1
fi

tar -C "$DIST_DIR" -czf "$DIST_DIR/StegHunter-Pro-${VERSION}-linux-${ARCH}.tar.gz" StegHunter_Pro

mkdir -p "$APP_DIR" "$PACKAGE_ROOT/usr/share/applications" "$PACKAGE_ROOT/DEBIAN"
cp -a "$APP_BUNDLE/." "$APP_DIR/"
cat > "$PACKAGE_ROOT/usr/share/applications/steg-hunter-pro.desktop" <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=StegHunter Pro
Comment=Image steganography analysis and forensics
Exec=/opt/steg-hunter-pro/StegHunter_Pro
Terminal=false
Categories=Utility;Security;
DESKTOP
cat > "$PACKAGE_ROOT/DEBIAN/control" <<CONTROL
Package: steg-hunter-pro
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: StegHunter Team <info@steghunter.dev>
Description: Image steganography analysis and forensics desktop application
 StegHunter Pro inspects images for statistical anomalies, LSB payloads,
 metadata, and trailing file data.
CONTROL
dpkg-deb --build --root-owner-group "$PACKAGE_ROOT" \
  "$DIST_DIR/steg-hunter-pro_${VERSION}_${ARCH}.deb"

echo "Created Linux bundle and Debian package in $DIST_DIR"
