# GCompress

GCompress is a modern, lightweight GUI application built with Python and GTK4 that simplifies the process of compressing videos and images. It acts as a user-friendly frontend for FFmpeg, allowing you to easily reduce file sizes without memorizing complex command-line arguments.

## Features

* **Modern Interface:** Built seamlessly with GTK4 and Python.
* **Granular Control:** An intuitive 1-100% quality slider automatically calculates the optimal `CRF` (for video) or `q:v` (for images) values.
* **Live Progress Tracking:** Parses FFmpeg output to display real-time progress bars for video compression.
* **Asynchronous Processing:** Compression runs in a background thread, ensuring the UI remains responsive even during heavy workloads.

## Prerequisites

Before running or building GCompress, ensure you have the following system dependencies installed:

* `python3`
* `ffmpeg` (and `ffprobe`, which is usually bundled with it)
* GTK4 Python bindings (`python-gobject` and `gtk4` on Arch Linux, or `python3-gi` and `gir1.2-gtk-4.0` on Debian/Ubuntu)

## Running from Source

You can run the application directly using Python. 

1. Clone the repository:
   ```bash
   git clone https://github.com/Jakub-Chrzanowski/gcompress.git
   cd gcompress
   ```

2. Execute the script:
   ```bash
   python3 gcompress
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.
