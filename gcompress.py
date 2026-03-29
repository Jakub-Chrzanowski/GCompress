import gi
import subprocess
import threading
import os
import sys

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib


TRANSLATIONS = {
    "en": {
        "desc": "Fast video and image compression using FFmpeg.",
        "select_file": "Select file...",
        "no_file": "No file selected",
        "selected": "Selected:\n{}",
        "quality": "Compression quality (1% - 100%):",
        "compress": "Compress",
        "analyzing": "Analyzing file...",
        "compressing": "Compressing...",
        "err_ffmpeg": "Error: FFmpeg not found. Ensure it is installed.",
        "success": "✅ Done! Saved as:\n{}",
        "err_general": "❌ An error occurred during compression."
    },
    "pl": {
        "desc": "Szybka kompresja filmów i zdjęć za pomocą FFmpeg.",
        "select_file": "Wybierz plik...",
        "no_file": "Brak wybranego pliku",
        "selected": "Wybrano:\n{}",
        "quality": "Jakość kompresji (1% - 100%):",
        "compress": "Kompresuj",
        "analyzing": "Analizowanie pliku...",
        "compressing": "Kompresowanie...",
        "err_ffmpeg": "Błąd: Nie znaleziono FFmpeg. Upewnij się, że jest zainstalowany.",
        "success": "✅ Gotowe! Zapisano jako:\n{}",
        "err_general": "❌ Wystąpił błąd podczas kompresji."
    },
    "es": {
        "desc": "Compresión rápida de video e imagen usando FFmpeg.",
        "select_file": "Seleccionar archivo...",
        "no_file": "Ningún archivo seleccionado",
        "selected": "Seleccionado:\n{}",
        "quality": "Calidad de compresión (1% - 100%):",
        "compress": "Comprimir",
        "analyzing": "Analizando archivo...",
        "compressing": "Comprimiendo...",
        "err_ffmpeg": "Error: FFmpeg no encontrado. Asegúrese de que esté instalado.",
        "success": "✅ ¡Hecho! Guardado como:\n{}",
        "err_general": "❌ Ocurrió un error durante la compresión."
    },
    "de": {
        "desc": "Schnelle Video- und Bildkomprimierung mit FFmpeg.",
        "select_file": "Datei auswählen...",
        "no_file": "Keine Datei ausgewählt",
        "selected": "Ausgewählt:\n{}",
        "quality": "Komprimierungsqualität (1% - 100%):",
        "compress": "Komprimieren",
        "analyzing": "Datei wird analysiert...",
        "compressing": "Komprimieren...",
        "err_ffmpeg": "Fehler: FFmpeg nicht gefunden. Stellen Sie sicher, dass es installiert ist.",
        "success": "✅ Fertig! Gespeichert als:\n{}",
        "err_general": "❌ Beim Komprimieren ist ein Fehler aufgetreten."
    },
    "fr": {
        "desc": "Compression vidéo et image rapide à l'aide de FFmpeg.",
        "select_file": "Sélectionner un fichier...",
        "no_file": "Aucun fichier sélectionné",
        "selected": "Sélectionné :\n{}",
        "quality": "Qualité de compression (1% - 100%) :",
        "compress": "Compresser",
        "analyzing": "Analyse du fichier...",
        "compressing": "Compression...",
        "err_ffmpeg": "Erreur : FFmpeg introuvable. Assurez-vous qu'il est installé.",
        "success": "✅ Terminé ! Enregistré sous :\n{}",
        "err_general": "❌ Une erreur s'est produite lors de la compression."
    }
}

class GCompressWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(450, 350)
        
        
        self.lang_codes = ["en", "pl", "es", "de", "fr"]
        self.current_lang = "pl" 
        self.status_state = None 
        self.last_result_file = None

        self.setup_headerbar()
        self.setup_ui()
        self.update_texts() 

    def setup_headerbar(self):
      
        header = Gtk.HeaderBar()
        self.set_titlebar(header)
        self.set_title("GCompress")

  
        lang_list = Gtk.StringList.new(["English", "Polski", "Español", "Deutsch", "Français"])
        self.lang_dropdown = Gtk.DropDown.new(model=lang_list, expression=None)
        self.lang_dropdown.set_selected(1) 
        self.lang_dropdown.connect("notify::selected", self.on_language_changed)
        
        header.pack_end(self.lang_dropdown)

    def setup_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        main_box.set_margin_top(24)
        main_box.set_margin_bottom(24)
        main_box.set_margin_start(24)
        main_box.set_margin_end(24)
        self.set_child(main_box)

        self.desc_label = Gtk.Label()
        self.desc_label.add_css_class("dim-label")
        self.desc_label.set_wrap(True)
        self.desc_label.set_justify(Gtk.Justification.CENTER)
        main_box.append(self.desc_label)

        self.file_button = Gtk.Button()
        self.file_button.set_halign(Gtk.Align.CENTER)
        self.file_button.connect("clicked", self.on_file_clicked)
        main_box.append(self.file_button)

        self.file_label = Gtk.Label()
        self.file_label.set_wrap(True)
        self.file_label.set_justify(Gtk.Justification.CENTER)
        main_box.append(self.file_label)

        quality_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.quality_label = Gtk.Label()
        self.quality_label.set_halign(Gtk.Align.START)
        quality_box.append(self.quality_label)

        self.quality_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1)
        self.quality_scale.set_value(70)
        self.quality_scale.set_draw_value(True)
        quality_box.append(self.quality_scale)
        main_box.append(quality_box)

        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_fraction(0.0)
        main_box.append(self.progress_bar)

        self.compress_button = Gtk.Button()
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

    def _(self, key):
       
        return TRANSLATIONS[self.current_lang].get(key, key)

    def on_language_changed(self, dropdown, pspec):
        selected_index = dropdown.get_selected()
        self.current_lang = self.lang_codes[selected_index]
        self.update_texts()

    def update_texts(self):
     
        self.desc_label.set_text(self._("desc"))
        self.file_button.set_label(self._("select_file"))
        self.quality_label.set_text(self._("quality"))
        self.compress_button.set_label(self._("compress"))

        
        if self.selected_file:
            self.file_label.set_text(self._("selected").format(os.path.basename(self.selected_file)))
        else:
            self.file_label.set_text(self._("no_file"))

        
        if self.status_state == "analyzing":
            self.status_label.set_text(self._("analyzing"))
        elif self.status_state == "compressing":
            self.status_label.set_text(self._("compressing"))
        elif self.status_state == "success" and self.last_result_file:
            self.status_label.set_text(self._("success").format(os.path.basename(self.last_result_file)))
        elif self.status_state == "err_ffmpeg":
            self.status_label.set_text(self._("err_ffmpeg"))
        elif self.status_state == "err_general":
            self.status_label.set_text(self._("err_general"))

    def on_file_clicked(self, button):
        dialog = Gtk.FileDialog()
        dialog.open(self, None, self.on_file_selected)

    def on_file_selected(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                self.selected_file = file.get_path()
                self.file_label.set_text(self._("selected").format(os.path.basename(self.selected_file)))
                self.status_label.set_text("")
                self.status_state = None
                self.progress_bar.set_fraction(0.0)
                self.compress_button.set_sensitive(True)
        except GLib.Error:
            pass

    def on_compress_clicked(self, button):
        if not self.selected_file: return
        
        self.compress_button.set_sensitive(False)
        self.file_button.set_sensitive(False)
        self.quality_scale.set_sensitive(False)
        self.lang_dropdown.set_sensitive(False) # Blokada zmiany języka podczas pracy
        self.progress_bar.set_fraction(0.0)
        
        self.status_state = "analyzing"
        self.status_label.set_text(self._("analyzing"))

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
                crf = int(35 - ((quality_val - 1) / 99) * 17)
                cmd = ['ffmpeg', '-y', '-i', input_file, '-vcodec', 'libx264', '-crf', str(crf), '-preset', 'fast', '-progress', 'pipe:1', output_file]
            else:
                qv = int(15 - ((quality_val - 1) / 99) * 13)
                cmd = ['ffmpeg', '-y', '-i', input_file, '-q:v', str(qv), output_file]
            
            GLib.idle_add(self.update_status_state, "compressing")

            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            for line in self.process.stdout:
                if is_video and duration > 0 and "out_time_ms=" in line:
                    try:
                        time_ms = int(line.split('=')[1].strip())
                        progress = (time_ms / 1000000.0) / duration
                        progress = min(max(progress, 0.0), 1.0)
                        GLib.idle_add(self.update_progress, progress)
                    except ValueError:
                        pass

            self.process.wait()
            success = self.process.returncode == 0
            if success:
                self.last_result_file = output_file
                GLib.idle_add(self.on_compress_finished, True, "success")
            else:
                GLib.idle_add(self.on_compress_finished, False, "err_general")

        except FileNotFoundError:
            GLib.idle_add(self.on_compress_finished, False, "err_ffmpeg")

    def update_status_state(self, state):
        self.status_state = state
        self.status_label.set_text(self._(state))

    def update_progress(self, fraction):
        self.progress_bar.set_fraction(fraction)

    def on_compress_finished(self, success, final_state):
        self.compress_button.set_sensitive(True)
        self.file_button.set_sensitive(True)
        self.quality_scale.set_sensitive(True)
        self.lang_dropdown.set_sensitive(True) # Odblokowanie wyboru języka
        
        self.status_state = final_state
        if success:
            self.progress_bar.set_fraction(1.0)
            self.status_label.set_text(self._("success").format(os.path.basename(self.last_result_file)))
        else:
            self.progress_bar.set_fraction(0.0)
            self.status_label.set_text(self._(final_state))

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