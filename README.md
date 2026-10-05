# GCompress

GCompress is a modern, lightweight GUI application built with Python and GTK4 that simplifies the process of compressing videos and images. It acts as a user-friendly frontend for FFmpeg, allowing you to easily reduce file sizes without memorizing complex command-line arguments. It runs on both Linux and Windows.

## Download

Grab the latest build for your platform from the [Releases page](https://github.com/Jakub-Chrzanowski/GCompress/releases):

* **Windows:** `GCompress-windows-x64.zip` - unzip anywhere and run `gcompress.exe`. FFmpeg is already bundled inside, nothing else to install.
* **Arch / Manjaro / EndeavourOS:** `gcompress-<version>-1-any.pkg.tar.zst` - install with `sudo pacman -U gcompress-*.pkg.tar.zst`. `pacman` pulls in FFmpeg and GTK4 automatically.

Both files are built and attached to every release automatically by CI (see [Releases are automated](#releases-are-automated)), straight from the source in this repository.

## Features

* **Modern Interface:** Built seamlessly with GTK4 and Python.
* **Granular Control:** An intuitive 1-100% quality slider automatically calculates the optimal `CRF` (for video) or `q:v` (for images) values.
* **Live Progress Tracking:** Parses FFmpeg output to display real-time progress bars for video compression.
* **Asynchronous Processing:** Compression runs in a background thread, ensuring the UI remains responsive even during heavy workloads.

## Prerequisites

These are only needed if you're running from source or building GCompress yourself - the files on the [Releases page](https://github.com/Jakub-Chrzanowski/GCompress/releases) already include everything required.

* `python3`
* `ffmpeg` (and `ffprobe`, which is usually bundled with it)
* GTK4 Python bindings:
  * Arch Linux: `python-gobject` and `gtk4`
  * Debian/Ubuntu: `python3-gi` and `gir1.2-gtk-4.0`
  * Windows: install these through MSYS2 (see below) - there is no standalone Windows installer for GTK4/PyGObject.

## Running from Source

### Linux

1. Clone the repository:
   ```bash
   git clone https://github.com/Jakub-Chrzanowski/gcompress.git
   cd gcompress
   ```

2. Execute the script:
   ```bash
   python3 gcompress
   ```

### Windows

GTK4 and PyGObject aren't available through a regular Windows Python install, so running from source means using [MSYS2](https://www.msys2.org/):

1. Install MSYS2, then open the **MSYS2 MINGW64** shell (not the plain MSYS2 shell) from the Start menu.
2. Install the dependencies:
   ```bash
   pacman -S --needed mingw-w64-x86_64-python mingw-w64-x86_64-python-gobject mingw-w64-x86_64-gtk4 mingw-w64-x86_64-ffmpeg git
   ```
3. Clone the repository and run it:
   ```bash
   git clone https://github.com/Jakub-Chrzanowski/gcompress.git
   cd gcompress
   python gcompress
   ```

> [!NOTE]
> GCompress will save the output file in the same directory as the original file, appending `_compressed` to the filename. Your original files are never overwritten.

## Packaging for Arch Linux (PKGBUILD)

On Arch-based systems (Arch, Manjaro, EndeavourOS), the native way to install GCompress as a proper application - with an entry in your application menu, an icon, and clean removal via `pacman` - is to build it from the `PKGBUILD` included in this repository, instead of using PyInstaller.

### 1. Prerequisites

```bash
sudo pacman -S --needed base-devel
```

(`base-devel` provides `makepkg` and other build tools; it's usually only needed once.)

### 2. Build and install

From the repository root (where `PKGBUILD`, `gcompress.desktop` and `gcompress.svg` are located):

```bash
makepkg -si
```

This builds the package and installs it with `pacman` (you'll be prompted for your `sudo` password). GCompress will then show up in your application menu like any other installed program, and can also be run from a terminal with `gcompress`.

### 3. Uninstalling

```bash
sudo pacman -R gcompress
```

## Building the Windows Package Manually

The [automated workflow](#releases-are-automated) does this for every release, but you can run the same steps yourself from an **MSYS2 MINGW64** shell:

1. Install the build dependencies (see [Running from Source → Windows](#windows) above) plus PyInstaller:
   ```bash
   pacman -S --needed mingw-w64-x86_64-python-pip
   pip install pyinstaller
   ```
2. Get `ffmpeg.exe` and `ffprobe.exe` (e.g. from a [static FFmpeg build](https://github.com/BtbN/FFmpeg-Builds/releases)) and place them in the project folder.
3. Build:
   ```bash
   cp gcompress gcompress.py
   pyinstaller gcompress-windows.spec
   ```
4. `dist/gcompress.exe` is the app. Copy `ffmpeg.exe` and `ffprobe.exe` into the same folder as `gcompress.exe` - the app looks for them right next to itself before falling back to PATH.

> [!NOTE]
> `gcompress-windows.spec` bundles GTK4's own runtime data (typelibs, icon theme, GSettings schemas, gdk-pixbuf loaders) from the MSYS2 MINGW64 prefix, which plain PyInstaller hooks don't pick up on their own. If a build ever starts and then fails to show its window or load icons, that's the first place to check.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
