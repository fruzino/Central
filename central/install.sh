#!/usr/bin/env bash
DESKTOP_FILE="$HOME/.local/share/applications/central.desktop"
mkdir -p "$HOME/.local/share/applications"
VERSION=1.0

cat << EOF > "$DESKTOP_FILE"
[Desktop Entry]
Type=Application
Version=$VERSION
Name=Central
Comment=Manage and organize your files/folders easily using CENTRAL!
Exec="$SCRIPT_PATH"
Icon=system-file-manager
Terminal=true
Categories=Utility;System;
EOF

if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications"
fi

echo "Central is installed. You can close this window."