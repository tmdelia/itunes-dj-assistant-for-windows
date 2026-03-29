# iTunes DJ Assistant for Windows

A Python application that monitors iTunes playback and automatically displays track information. When a song changes, it searches for existing files (images, PDFs, documents) based on the track metadata and opens them automatically. If no file is found, it generates a beautifully styled HTML page with the track details.

Perfect for tango DJs, music educators, dancers, and anyone who wants visual feedback of their currently playing music.

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://github.com/yourusername/itunes-dj-assistant-for-windows/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/yourusername/itunes-dj-assistant-for-windows/total.svg)](https://github.com/yourusername/itunes-dj-assistant-for-windows/releases)

---

## 📥 Download

**[Download Latest Release →](https://github.com/tmdelia/itunes-dj-assistant-for-windows/releases/latest)**

Pre-built executable available - no Python installation needed!

---

## ✨ Features

- **🎨 User-Friendly GUI** - Easy configuration through a graphical interface
- **📊 Real-Time Monitoring** - Live log display showing all activity
- **🎯 Customizable Display** - Choose which metadata to show (Artist, Grouping, Song, Year)
- **🔍 Smart File Search** - Automatically finds and opens matching files
- **📄 Auto HTML Generation** - Creates styled HTML pages when no file exists
- **💾 Settings Persistence** - Your preferences are saved and remembered
- **🔄 Auto-Reconnect** - Reconnects automatically if iTunes restarts
- **🎭 Tango-Friendly** - Built with tango music organization in mind
- **🎨 Custom Icons** - Add your own icon to the executable

## 🖼️ Screenshots

### Configuration Tab
Configure your monitoring directory and choose which information to display.

### Monitor Log Tab
Real-time activity log with all monitoring events displayed in an easy-to-read format.

## 📋 Requirements

- **Windows 10 or 11**
- **Python 3.6+** (for running from source)
- **iTunes** installed and running
- **pywin32** package

## 🚀 Quick Start

### Option 1: Download Executable (Recommended for Most Users)

**No Python installation required!**

1. Go to [**Releases**](https://github.com/tmdelia/itunes-dj-assistant-for-windows/releases)
2. Download the latest `iTunes-DJ-Assistant-vX.X.X-Windows.zip`
3. Extract the ZIP file to any folder
4. Run `iTunes DJ Assistant.exe`
5. Done! ✨

### Option 2: Run from Source (For Developers)

**Requires Python 3.6+**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/itunes-dj-assistant-for-windows.git
   cd itunes-dj-assistant-for-windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python itunes_dj_assistant_for_windows.py
   ```

4. **(Optional) Build your own executable**
   ```bash
   build.bat
   ```
   See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for details.

## 🛠️ Building from Source

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed instructions on creating a Windows executable using PyInstaller.

**Quick build:**
```bash
pip install pyinstaller pywin32
pyinstaller itunes_dj_assistant.spec --clean
```

Or simply double-click `build.bat` on Windows.

**Adding a custom icon:**
See the instructions at the top of `itunes_dj_assistant.spec` for how to add your own icon to the executable.

## 📖 Usage

### Initial Setup

1. **Launch the application**
2. **Configure settings** in the Configuration tab:
   - Click **Browse** to select your media directory
   - Check which metadata fields to display
   - Set check interval (1-10 seconds)
3. **Click Start Monitoring**

### How It Works

When a song changes in iTunes:

1. **Searches for existing files** matching the track metadata
   - Looks for: `.jpg`, `.png`, `.txt`, `.pdf`, `.doc`, `.docx`, `.html`, `.rtf`
   - Filename format: `[Artist] [Grouping] [Song].ext`

2. **If found:** Opens the file automatically

3. **If not found:** Creates and opens an HTML file with:
   - Artist name (9em font - very large)
   - Grouping (4em font - medium-large)  
   - Song title (7em font - large, in quotes)
   - Year (3em font - medium)
   - All on black background with white text

### iTunes Grouping Field

The Grouping field is perfect for additional categorization:

1. In iTunes, right-click a song → **Get Info**
2. Go to **Details** tab
3. Fill in **Grouping** field
   - For tango: "Tango Singer", "Orchestra", "Bandoneon"
   - For jazz: "Jazz Vocalist", "Quartet", "Big Band"
   - Any categorization you like!

## 🎭 Example Use Cases

### Tango DJs
- Auto-display orchestra and singer names during milongas
- Project current track info to screens
- Perfect for cortinas and tandas
- Professional presentation for dancers

### Music Educators
- Show historical context during lessons
- Track listening exercises visually
- Create automatic study materials
- Display composer and period information

### Dance Studios
- Display current track for practice sessions
- Organize music by style and era
- Auto-show choreographer credits
- Professional studio presentation

### General DJs & Performers
- Display track info for audience
- Auto-documentation of playlists
- Professional event setup
- Playlist management tool

## ⚙️ Configuration Options

### Display Fields
Choose any combination:
- ✅ **Artist Name** - The performer/artist
- ✅ **Grouping** - iTunes grouping field (custom category)
- ✅ **Song Name** - The track title
- ✅ **Year** - Recording year

**Note:** Year is shown in HTML but excluded from filenames for cleaner file management.

### Check Interval
- Range: 1-10 seconds
- Default: 2 seconds
- Lower = more responsive, Higher = less CPU usage

### Directory Structure Example

```
C:\Users\YourName\Music\Tango\
├── Carlos Gardel Tango Singer.jpg
├── Astor Piazzolla Bandoneon.pdf
├── Anibal Troilo Orquesta Tipica.png
└── [Auto-generated HTML files]
```

## 🔧 Configuration File

Settings are saved to:
```
C:\Users\YourName\itunes_monitor_config.json
```

To reset: Delete this file and restart the application.

## 🐛 Troubleshooting

### "pywin32 package is not installed"
```bash
pip install pywin32
python -m pywin32_postinstall -install
```

### "Cannot connect to iTunes"
- Make sure iTunes is installed and running
- The app will auto-reconnect when iTunes starts

### "Directory does not exist"
- Use the Browse button to select a valid folder
- Create the folder first if it doesn't exist

### Executable flagged by antivirus
- This is a false positive common with PyInstaller
- Add an exclusion for the `dist\` folder

### Application won't start
- Right-click `iTunes DJ Assistant.exe` → Run as Administrator
- Check Windows Defender/Firewall settings

## 📝 File Naming Convention

Files are named using selected metadata fields in this order:
```
[Artist] [Grouping] [Song].extension
```

Examples:
- All fields: `Carlos Gardel Tango Singer Por una Cabeza.html`
- No grouping: `Carlos Gardel Por una Cabeza.html`
- Only artist + song: Same as above
- Only song: `Por una Cabeza.html`

**Note:** Double spaces are automatically avoided when grouping is empty.

## 🎨 HTML Output Styling

Auto-generated HTML files feature:
- Black background with white text
- Centered, responsive layout
- Large, readable fonts
- Professional appearance
- Mobile-friendly design

## 🔒 Privacy & Security

- ✅ All data stays on your computer
- ✅ No internet connection required
- ✅ No telemetry or data collection
- ✅ Open source - inspect the code yourself

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for DJs and the tango community
- Inspired by the need for better music organization
- Thanks to all contributors and testers

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/itunes-dj-assistant-for-windows/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/itunes-dj-assistant-for-windows/discussions)

## 🗺️ Roadmap

Future enhancements being considered:
- [ ] Support for other media players (Spotify, Foobar2000, etc.)
- [ ] Multiple directory monitoring
- [ ] Playlist-specific configurations
- [ ] Theme customization
- [ ] Export playlists with metadata
- [ ] macOS support
- [ ] Web-based remote control for DJs
- [ ] Automatic cortina detection

---

**Made with ❤️ for DJs and music lovers**

**Star ⭐ this repo if you find it useful!**
