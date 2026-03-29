#!/usr/bin/env python3
"""
iTunes Song Reader and File Opener for Windows 11
Continuously monitors iTunes and opens a file based on the artist name when the song changes.
"""

import os
import time
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# --- COM / pythoncom imports with proper type stubs ---
try:
    import win32com.client as win32com_client  # type: ignore[import]
    _win32com_client = win32com_client
    COM_AVAILABLE = True
except ImportError:
    _win32com_client = None
    COM_AVAILABLE = False

try:
    import pythoncom  # type: ignore[import]
    _co_init:   Optional[Callable[[], None]] = pythoncom.CoInitialize
    _co_uninit: Optional[Callable[[], None]] = pythoncom.CoUninitialize
    PYTHONCOM_AVAILABLE = True
except ImportError:
    _co_init   = None
    _co_uninit = None
    PYTHONCOM_AVAILABLE = False


# Configuration file path
CONFIG_FILE = Path.home() / "itunes_monitor_config.json"


def _co_initialize() -> None:
    """Initialize COM for the current thread if pythoncom is available."""
    if callable(_co_init):
        _co_init()


def _co_uninitialize() -> None:
    """Uninitialize COM for the current thread if pythoncom is available."""
    if callable(_co_uninit):
        try:
            _co_uninit()
        except Exception:
            pass


def load_config() -> dict:
    """Load configuration from file."""
    default_config = {
        'directory': str(Path.home() / 'Desktop'),
        'show_artist': True,
        'show_grouping': True,
        'show_song': True,
        'show_year': True,
        'check_interval': 2
    }

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Ensure all keys exist
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except (IOError, json.JSONDecodeError):
            return default_config
    return default_config


def save_config(config: dict) -> bool:
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except IOError:
        return False


def get_current_itunes_track() -> Optional[dict]:
    """
    Get the currently playing track information from iTunes on Windows.
    Returns a dictionary with track info or None if nothing is playing.
    """
    if not COM_AVAILABLE or _win32com_client is None:
        return None

    _co_initialize()
    try:
        itunes = _win32com_client.Dispatch("iTunes.Application")

        if itunes.PlayerState == 1:  # 1 = playing
            current_track = itunes.CurrentTrack
            if current_track:
                return {
                    'artist': current_track.Artist,
                    'song': current_track.Name,
                    'album': current_track.Album,
                    'grouping': current_track.Grouping,
                    'year': current_track.Year,
                }
        return None
    except Exception:
        return None
    finally:
        _co_uninitialize()


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be used as a filename.
    Removes/replaces characters that aren't safe for Windows filenames.
    """
    replacements = {
        '<': '_', '>': '_', ':': '_', '"': '_',
        '/': '_', '\\': '_', '|': '_', '?': '_', '*': '_',
        'á': 'a', 'Á': 'A', 'é': 'e', 'í': 'i',
        'ó': 'o', 'ú': 'u', 'ü': 'u',
    }
    sanitized = name
    for old, new in replacements.items():
        sanitized = sanitized.replace(old, new)
    return sanitized.strip('. ')


def create_and_open_html(track_info: dict, config: dict, base_directory: Path) -> tuple:
    """
    Create an HTML file with selected track information, then open it.
    Returns: Tuple of (success: bool, result: str or Path)
    """
    if not isinstance(base_directory, Path):
        base_directory = Path(base_directory)

    # Build filename from selected fields (year excluded)
    filename_parts = []
    if config['show_artist'] and track_info['artist']:
        filename_parts.append(sanitize_filename(track_info['artist']))
    if config['show_grouping'] and track_info['grouping']:
        filename_parts.append(sanitize_filename(track_info['grouping']))
    if config['show_song'] and track_info['song']:
        filename_parts.append(sanitize_filename(track_info['song']))

    filename = " ".join(filename_parts) + ".html"
    filepath = base_directory / filename

    # Build HTML body with selected fields (year included in display)
    html_parts = []
    if config['show_artist'] and track_info['artist']:
        html_parts.append('<div class="artist">' + track_info['artist'] + '</div>')
    if config['show_grouping'] and track_info['grouping']:
        html_parts.append('<div class="grouping">' + track_info['grouping'] + '</div>')
    if config['show_song'] and track_info['song']:
        html_parts.append('<div class="song">"' + track_info['song'] + '"</div>')
    if config['show_year'] and track_info['year']:
        html_parts.append('<div class="year">' + str(track_info['year']) + '</div>')

    html_body = "\n    ".join(html_parts)

    html_content = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '    <title>Now Playing</title>\n'
        '    <style>\n'
        '        body {\n'
        '            background-color: black;\n'
        '            color: white;\n'
        '            font-family: Arial, sans-serif;\n'
        '            margin: 0;\n'
        '            display: flex;\n'
        '            flex-direction: column;\n'
        '            align-items: center;\n'
        '            justify-content: center;\n'
        '            min-height: 100vh;\n'
        '        }\n'
        '        .artist  { font-size: 9em; margin-bottom: 10px; text-align: center; }\n'
        '        .grouping { font-size: 4em; text-align: center; margin-bottom: 75px; }\n'
        '        .song    { font-size: 7em; text-align: center; }\n'
        '        .year    { font-size: 3em; text-align: center; }\n'
        '    </style>\n'
        '</head>\n'
        '<body>\n'
        '    ' + html_body + '\n'
        '</body>\n'
        '</html>\n'
    )

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        os.startfile(str(filepath))
        return True, filepath
    except (IOError, OSError) as e:
        return False, str(e)


def open_file_for_track(track_info: dict, config: dict, base_directory: Path) -> tuple:
    """
    Search for and open a file matching the track info.
    Returns: Tuple of (found: bool, result: Path or str or None, search_string: str)
    """
    if not isinstance(base_directory, Path):
        base_directory = Path(base_directory)

    # Build search string (year excluded)
    search_parts = []
    if config['show_artist'] and track_info['artist']:
        search_parts.append(sanitize_filename(track_info['artist']))
    if config['show_grouping'] and track_info['grouping']:
        search_parts.append(sanitize_filename(track_info['grouping']))
    if config['show_song'] and track_info['song']:
        search_parts.append(sanitize_filename(track_info['song']))

    search_string = " ".join(search_parts)
    extensions = ['.jpg', '.png', '.txt', '.pdf', '.doc', '.docx', '.html', '.rtf']
    found_file = None

    # Exact match first
    for ext in extensions:
        filepath = base_directory / (search_string + ext)
        if filepath.exists():
            found_file = filepath
            break

    # Case-insensitive fallback
    if not found_file and base_directory.exists():
        try:
            search_lower = search_string.lower()
            for file in base_directory.iterdir():
                if file.is_file() and search_lower in file.name.lower():
                    found_file = file
                    break
        except OSError:
            pass

    if found_file:
        try:
            os.startfile(str(found_file))
            return True, found_file, search_string
        except OSError as e:
            return False, str(e), search_string

    return False, None, search_string


def get_timestamp() -> str:
    """Get current timestamp for logging."""
    return datetime.now().strftime("%H:%M:%S")


class MonitorGUI:
    """Main GUI for iTunes monitor with configuration and log display."""

    def __init__(self) -> None:
        self.config = load_config()
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None

        self.root = tk.Tk()
        self.root.title("iTunes Monitor")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # tk variables
        self.dir_var      = tk.StringVar(value=self.config['directory'])
        self.artist_var   = tk.BooleanVar(value=self.config['show_artist'])
        self.grouping_var = tk.BooleanVar(value=self.config['show_grouping'])
        self.song_var     = tk.BooleanVar(value=self.config['show_song'])
        self.year_var     = tk.BooleanVar(value=self.config['show_year'])
        self.interval_var = tk.StringVar(value=str(self.config['check_interval']))

        # Widgets (assigned in setup methods)
        self.start_btn:     Optional[ttk.Button]       = None
        self.stop_btn:      Optional[ttk.Button]       = None
        self.log_text:      Optional[scrolledtext.ScrolledText] = None
        self.status_label:  Optional[ttk.Label]        = None
        self.config_frame:  Optional[ttk.Frame]        = None
        self.log_frame:     Optional[ttk.Frame]        = None
        self.notebook:      Optional[ttk.Notebook]     = None

        # Build UI
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.config_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.config_frame, text="Configuration")

        self.log_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.log_frame, text="Monitor Log")

        self.setup_config_tab()
        self.setup_log_tab()
        self.setup_status_bar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_config_tab(self) -> None:
        """Setup the configuration tab."""
        ttk.Label(self.config_frame, text="Monitor Directory:",
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky="w", pady=(0, 5))

        dir_frame = ttk.Frame(self.config_frame)
        dir_frame.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 20))

        ttk.Entry(dir_frame, textvariable=self.dir_var, width=50).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(dir_frame, text="Browse...", command=self.browse_directory).grid(row=0, column=1)

        ttk.Label(self.config_frame, text="Information to Display:",
                  font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky="w", pady=(0, 10))

        options_frame = ttk.Frame(self.config_frame)
        options_frame.grid(row=3, column=0, columnspan=2, sticky="we", pady=(0, 20))

        ttk.Checkbutton(options_frame, text="Artist Name", variable=self.artist_var).grid(
            row=0, column=0, sticky="w", pady=5)
        ttk.Checkbutton(options_frame, text="Grouping",    variable=self.grouping_var).grid(
            row=1, column=0, sticky="w", pady=5)
        ttk.Checkbutton(options_frame, text="Song Name",   variable=self.song_var).grid(
            row=2, column=0, sticky="w", pady=5)
        ttk.Checkbutton(options_frame, text="Year",        variable=self.year_var).grid(
            row=3, column=0, sticky="w", pady=5)

        ttk.Label(self.config_frame, text="Check Interval (seconds):",
                  font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky="w", pady=(0, 5))
        ttk.Spinbox(self.config_frame, from_=1, to=10,
                    textvariable=self.interval_var, width=10).grid(
            row=5, column=0, sticky="w", pady=(0, 20))

        button_frame = ttk.Frame(self.config_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self.start_btn = ttk.Button(button_frame, text="Start Monitoring",
                                    command=self.start_monitoring, width=20)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(button_frame, text="Stop Monitoring",
                                   command=self.stop_monitoring, width=20, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)

    def setup_log_tab(self) -> None:
        """Setup the log display tab."""
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, wrap="word", width=80, height=30,
            font=('Courier', 9), bg='black', fg='white')
        self.log_text.pack(fill="both", expand=True)

        ttk.Button(self.log_frame, text="Clear Log", command=self.clear_log).pack(pady=(10, 0))

    def setup_status_bar(self) -> None:
        """Setup the status bar."""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        self.status_label = ttk.Label(status_frame, text="Ready",
                                      relief="sunken", anchor="w")
        self.status_label.pack(fill="x")

    def browse_directory(self) -> None:
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(
            initialdir=self.dir_var.get(),
            title="Select Monitor Directory"
        )
        if directory:
            self.dir_var.set(directory)

    def log(self, message: str) -> None:
        """Add a message to the log."""
        if self.log_text is not None:
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()

    def clear_log(self) -> None:
        """Clear the log text area."""
        if self.log_text is not None:
            self.log_text.delete(1.0, tk.END)

    def update_status(self, message: str) -> None:
        """Update the status bar."""
        if self.status_label is not None:
            self.status_label.config(text=message)

    def start_monitoring(self) -> None:
        """Validate settings and start monitoring."""
        if not COM_AVAILABLE:
            messagebox.showerror("Error",
                "pywin32 package is not installed.\n\nPlease run: pip install pywin32")
            return

        if not any([self.artist_var.get(), self.grouping_var.get(),
                    self.song_var.get(), self.year_var.get()]):
            messagebox.showerror("Error",
                "Please select at least one information field to display.")
            return

        directory = Path(self.dir_var.get())
        if not directory.exists():
            messagebox.showerror("Error", f"Directory does not exist:\n{directory}")
            return
        if not directory.is_dir():
            messagebox.showerror("Error", f"Path is not a directory:\n{directory}")
            return

        try:
            check_interval = float(self.interval_var.get())
            if check_interval < 1 or check_interval > 10:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Check interval must be between 1 and 10 seconds.")
            return

        self.config = {
            'directory':     str(directory),
            'show_artist':   self.artist_var.get(),
            'show_grouping': self.grouping_var.get(),
            'show_song':     self.song_var.get(),
            'show_year':     self.year_var.get(),
            'check_interval': check_interval
        }
        save_config(self.config)

        self.clear_log()
        if self.notebook is not None and self.log_frame is not None:
            self.notebook.select(self.log_frame)

        if self.start_btn is not None:
            self.start_btn.config(state="disabled")
        if self.stop_btn is not None:
            self.stop_btn.config(state="normal")

        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_itunes, daemon=True)
        self.monitor_thread.start()

    def stop_monitoring(self) -> None:
        """Stop monitoring."""
        self.monitoring = False
        if self.start_btn is not None:
            self.start_btn.config(state="normal")
        if self.stop_btn is not None:
            self.stop_btn.config(state="disabled")
        self.update_status("Stopped")
        self.log("\n" + "=" * 70)
        self.log("Monitoring stopped by user")
        self.log("=" * 70)

    def monitor_itunes(self) -> None:
        """Monitor iTunes for song changes (runs in separate thread)."""
        _co_initialize()

        base_directory = Path(self.config['directory'])
        check_interval = self.config['check_interval']

        self.log("=" * 70)
        self.log("iTunes Monitor - Running")
        self.log("=" * 70)
        self.log(f"Monitoring directory: {base_directory.absolute()}")
        self.log(f"Check interval: {check_interval} seconds")
        self.log("\nDisplaying:")
        if self.config['show_artist']:   self.log("  ✓ Artist Name")
        if self.config['show_grouping']: self.log("  ✓ Grouping")
        if self.config['show_song']:     self.log("  ✓ Song Name")
        if self.config['show_year']:     self.log("  ✓ Year")
        self.log("\nPress 'Stop Monitoring' button to stop\n")
        self.log("=" * 70)
        self.update_status("Monitoring...")

        last_song = None
        itunes = None
        connection_errors = 0
        max_connection_errors = 5

        try:
            while self.monitoring:
                try:
                    if itunes is None:
                        try:
                            if _win32com_client is None:
                                break
                            itunes = _win32com_client.Dispatch("iTunes.Application")
                            if connection_errors > 0:
                                self.log(f"\n[{get_timestamp()}] ✓ Reconnected to iTunes")
                                self.update_status("Connected to iTunes")
                            connection_errors = 0
                        except Exception as e:
                            connection_errors += 1
                            if connection_errors == 1:
                                self.log(f"\n[{get_timestamp()}] ✗ Cannot connect to iTunes: {e}")
                                self.log("Waiting for iTunes to start...")
                                self.update_status("Waiting for iTunes...")
                            elif connection_errors >= max_connection_errors:
                                self.log(f"[{get_timestamp()}] Failed to connect after "
                                         f"{max_connection_errors} attempts")
                                self.log("Make sure iTunes is installed and try starting it manually.")
                                self.update_status("iTunes connection failed")
                            time.sleep(check_interval)
                            continue

                    if itunes.PlayerState == 1:  # playing
                        current_track = itunes.CurrentTrack
                        if current_track:
                            current_song = current_track.Name
                            if current_song != last_song:
                                track_info = {
                                    'artist':   current_track.Artist,
                                    'song':     current_song,
                                    'album':    current_track.Album,
                                    'grouping': current_track.Grouping,
                                    'year':     current_track.Year,
                                }

                                self.log(f"\n[{get_timestamp()}] ♪ New track detected:")
                                self.log(f"  Artist:   {track_info['artist']}")
                                self.log(f"  Song:     {track_info['song']}")
                                self.log(f"  Album:    {track_info['album']}")
                                self.log(f"  Grouping: {track_info['grouping']}")
                                self.log(f"  Year:     {track_info['year']}")
                                self.log("-" * 70)
                                self.update_status(f"Playing: {track_info['song']}")

                                file_found, result, search_string = open_file_for_track(
                                    track_info, self.config, base_directory)

                                if file_found:
                                    self.log(f"Opening file: {result}")
                                elif result is None:
                                    self.log(f"No file found for: {search_string}")
                                    self.log(f"In directory: {base_directory.absolute()}")
                                    self.log("Creating HTML file instead...")
                                    html_success, html_result = create_and_open_html(
                                        track_info, self.config, base_directory)
                                    if html_success:
                                        self.log(f"Created HTML file: {html_result}")
                                    else:
                                        self.log(f"Error creating HTML file: {html_result}")
                                else:
                                    self.log(f"Error opening file: {result}")

                                last_song = current_song
                                self.log("-" * 70)
                                self.log("Listening for next song change...")

                    elif itunes.PlayerState == 0:  # stopped
                        if last_song is not None:
                            self.log(f"\n[{get_timestamp()}] iTunes playback stopped")
                            self.update_status("iTunes stopped")
                            last_song = None

                except Exception as e:
                    error_msg = str(e)
                    if "The RPC server is unavailable" in error_msg or "Invalid class string" in error_msg:
                        if itunes is not None:
                            self.log(f"\n[{get_timestamp()}] ✗ Lost connection to iTunes")
                            self.update_status("Lost connection to iTunes")
                        itunes = None
                        last_song = None
                    else:
                        self.log(f"\n[{get_timestamp()}] Error: {e}")

                time.sleep(check_interval)

        finally:
            _co_uninitialize()

    def on_closing(self) -> None:
        """Handle window close event."""
        if self.monitoring:
            if messagebox.askokcancel("Quit", "Monitoring is active. Do you want to stop and quit?"):
                self.monitoring = False
                if self.monitor_thread is not None:
                    self.monitor_thread.join(timeout=2)
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self) -> None:
        """Run the GUI."""
        self.root.mainloop()


def main() -> None:
    """Main function to run the script."""
    gui = MonitorGUI()
    gui.run()


if __name__ == '__main__':
    main()
