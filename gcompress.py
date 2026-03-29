import gi
import subprocess
import threading
import os
import sys
import re

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Pango

class GCompressWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("GCompress")
        self.set_default_size(450, 350)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        main_box.set_margin_top(24)
        main_box.set_margin_bottom(24)
        main_box.set_margin_start(24)
        main_box.set_margin_end(24)
        self.set_child(main_box)

        # Tytuł
        title_label = Gtk.Label(label="<span size='x-large' weight='bold'>GCompress</span>", use_markup=True)
        main_box.append(title_label)

        # Wybór pliku
        self.file_button = Gtk.Button(label="Wybierz plik...")
        self.file_button.set_halign(Gtk.Align.CENTER)
        self.file_button.connect("clicked", self.on_file_clicked)
        main_box.append(self.file_button)

        self.file_label = Gtk.Label(label="Brak wybranego pliku")
        self.file_label.set_wrap(True)
        self.file_label.set_justify(Gtk.Justification.CENTER)
        main_box.append(self.file_label)

        # Suwak Jakości
        quality_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        quality_label = Gtk.Label(label="Jakość kompresji (1% - 100%):")
        quality_label.set_halign(Gtk.Align.START)
        quality_box.append(quality_label)

        self.quality_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1)
        self.quality_scale.set_value(70) # Domyślna wartość
        self.quality_scale.set_draw_value(True)
        quality_box.append(self.quality_scale)
        main_box.append(quality_box)

        # Pasek postępu
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_fraction(0.0)
        main_box.append(self.progress_bar)

        # Przycisk kompresji
        self.compress_button = Gtk.Button(label="Kompresuj")
        self.compress_button.set_halign(Gtk.Align.CENTER)
        self.compress_button.set_sensitive(False)
        self.compress_button.connect("clicked", self.on_compress_clicked)
        self.compress_button.add_css_class("suggested-action")
        main_box.append(self.compress_button)

        self.status_label = Gtk.Label(label="")
        self.status_label.set_wrap(True)
        self.status_label.set_justify(Gtk.Justification.CENTER)
        main_box.append(self.status_label)

        self.selected_file = None
        self.process = None

    def on_file_clicked(self, button):
        dialog = Gtk.FileDialog()
        dialog.open(self, None, self.on_file_selected)

    def on_file_selected(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                self.selected_file = file.get_path()
                self.file_label.set_text(f"Wybrano: {os.path.basename(self.selected_file)}")
                self.status_label.set_text("")
                self.progress_bar.set_fraction(0.0)
                self.compress_button.set_sensitive(True)
        except GLib.Error:
            pass

    def on_compress_clicked(self, button):
        if not self.selected_file: return
        
        self.compress_button.set_sensitive(False)
        self.file_button.set_sensitive(False)
        self.quality_scale.set_sensitive(False)
        self.progress_bar.set_fraction(0.0)
        self.status_label.set_text("Analizowanie pliku...")

        thread = threading.Thread(target=self.run_ffmpeg)
        thread.daemon = True
        thread.start()

    def get_duration(self, input_file):
        try:
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
            output = subprocess.check_output(cmd, text=True).strip()
            return float(output)
        except Exception:
            return 0.0

    def run_ffmpeg(self):
        input_file = self.selected_file
        filename, ext = os.path.splitext(input_file)
        output_file = f"{filename}_compressed{ext}"
        quality_val = self.quality_scale.get_value()
        
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.webm']
        is_video = ext.lower() in video_extensions

        duration = 0.0
        if is_video:
            duration = self.get_duration(input_file)

        try:
            if is_video:
                # Przeliczenie 1-100 na CRF (100 = najlepsza jakość CRF 18, 1 = najgorsza CRF 35)
                crf = int(35 - ((quality_val - 1) / 99) * 17)
                cmd = ['ffmpeg', '-y', '-i', input_file, '-vcodec', 'libx264', '-crf', str(crf), '-preset', 'fast', '-progress', 'pipe:1', output_file]
            else:
                # Przeliczenie 1-100 na q:v (100 = najlepsza q:v 2, 1 = najgorsza q:v 15)
                qv = int(15 - ((quality_val - 1) / 99) * 13)
                cmd = ['ffmpeg', '-y', '-i', input_file, '-q:v', str(qv), output_file]
            
            GLib.idle_add(self.status_label.set_text, "Kompresowanie...")

            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            for line in self.process.stdout:
                if is_video and duration > 0 and "out_time_ms=" in line:
                    try:
                        time_ms = int(line.split('=')[1].strip())
                        progress = (time_ms / 1000000.0) / duration
                        progress = min(max(progress, 0.0), 1.0) # Zabezpieczenie przed przekroczeniem 100%
                        GLib.idle_add(self.update_progress, progress)
                    except ValueError:
                        pass

            self.process.wait()
            success = self.process.returncode == 0

        except FileNotFoundError:
            GLib.idle_add(self.on_compress_finished, False, "Błąd: Nie znaleziono FFmpeg. Upewnij się, że jest zainstalowany.")
            return

        GLib.idle_add(self.on_compress_finished, success, output_file)

    def update_progress(self, fraction):
        self.progress_bar.set_fraction(fraction)

    def on_compress_finished(self, success, result_text):
        self.compress_button.set_sensitive(True)
        self.file_button.set_sensitive(True)
        self.quality_scale.set_sensitive(True)
        
        if success:
            self.progress_bar.set_fraction(1.0)
            self.status_label.set_text(f"✅ Gotowe! Zapisano jako:\n{os.path.basename(result_text)}")
        else:
            self.progress_bar.set_fraction(0.0)
            if "Błąd" in result_text:
                self.status_label.set_text(result_text)
            else:
                self.status_label.set_text("❌ Wystąpił błąd podczas kompresji.")

class GCompressApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.github.gcompress")

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = GCompressWindow(application=self)
        win.present()

if __name__ == "__main__":
    app = GCompressApp()
    sys.exit(app.run(sys.argv))