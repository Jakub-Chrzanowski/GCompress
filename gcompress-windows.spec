# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for the Windows build of GCompress.
#
# This must be run from an MSYS2 MINGW64 shell that has the GTK4/PyGObject
# stack installed (mingw-w64-x86_64-gtk4, mingw-w64-x86_64-python-gobject,
# mingw-w64-x86_64-python-pyinstaller). See .github/workflows/release.yml,
# job "build-windows", for the exact, known-good sequence of commands - that
# workflow is the source of truth; this file assumes it was run that way.
#
# Build with:
#   pyinstaller gcompress-windows.spec
#
# ffmpeg.exe / ffprobe.exe are NOT embedded here - they are plain console
# executables, so gcompress.py (see _find_tool) looks for them in the same
# folder as gcompress.exe at runtime. The release workflow copies them next
# to dist/gcompress.exe after this build finishes.

import os
from PyInstaller.utils.hooks import collect_all

mingw_prefix = os.environ.get("MINGW_PREFIX")
if not mingw_prefix:
    raise SystemExit(
        "MINGW_PREFIX is not set. Run this from an MSYS2 MINGW64 shell - "
        "see .github/workflows/release.yml (job build-windows) for setup."
    )

datas = []
binaries = []
hiddenimports = []

gi_datas, gi_binaries, gi_hidden = collect_all("gi")
datas += gi_datas
binaries += gi_binaries
hiddenimports += gi_hidden


def add_tree(src):
    """Bundle a whole directory from the MSYS2 MINGW64 prefix, preserving
    its path relative to that prefix (so it lands in the same relative
    place inside the frozen app, e.g. share/glib-2.0/schemas)."""
    if not os.path.isdir(src):
        print(f"[gcompress-windows.spec] WARNING: missing {src}, skipping")
        return
    for root, _dirs, files in os.walk(src):
        if not files:
            continue
        rel_dir = os.path.relpath(root, mingw_prefix)
        datas.append((os.path.join(root, "*"), rel_dir))


# GTK4/GLib runtime data PyInstaller's own hooks don't know to pull in:
# introspection typelibs, the icon theme, compiled GSettings schemas and the
# gdk-pixbuf loader cache. Without these the app can still start but file
# dialogs, icons or image loading may misbehave.
add_tree(os.path.join(mingw_prefix, "lib", "girepository-1.0"))
add_tree(os.path.join(mingw_prefix, "share", "glib-2.0", "schemas"))
add_tree(os.path.join(mingw_prefix, "share", "icons", "Adwaita"))
add_tree(os.path.join(mingw_prefix, "share", "icons", "hicolor"))
add_tree(os.path.join(mingw_prefix, "lib", "gdk-pixbuf-2.0"))

a = Analysis(
    ["gcompress.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="gcompress",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon="gcompress.ico",
)
