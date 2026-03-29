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
   git clone [https://github.com/your-username/gcompress.git](https://github.com/your-username/gcompress.git)
   cd gcompress
   ```

2. Execute the script:
   ```bash
   python3 gcompress.py
   ```

> [!NOTE]
> GCompress will save the output file in the same directory as the original file, appending `_compressed` to the filename. Your original files are never overwritten.

## Building a Standalone Executable (Linux)

If you prefer to compile the application into a single executable using PyInstaller, you must set up your virtual environment correctly to allow access to system-level GTK bindings.

> [!IMPORTANT]  
> Standard Python virtual environments (`python3 -m venv .venv`) isolate the environment from system packages. Since the `gi` (PyGObject) module relies heavily on system-level C libraries (GTK4), your virtual environment **must** inherit system packages.

1. Create a virtual environment with system site packages enabled:
   ```bash
   python3 -m venv --system-site-packages .venv
   source .venv/bin/activate
   ```

2. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

3. Build the executable:
   ```bash
   pyinstaller --onefile --windowed gcompress.py
   ```

4. Find your executable in the generated `dist/` directory.

> [!WARNING]  
> Packaging GTK applications with PyInstaller on Linux can sometimes cause issues with missing system icons, themes, or typelibs on target machines that do not have GTK4 installed. For the best native Linux experience, it is highly recommended to distribute the `.py` script alongside a `.desktop` file instead of using PyInstaller.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
