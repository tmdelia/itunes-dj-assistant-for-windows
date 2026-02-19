# Building iTunes DJ Assistant for Windows

## Prerequisites

All of the following must be done on a **Windows machine** — PyInstaller
builds platform-specific executables and cannot cross-compile.

---

## Step 1 — Install Python

If Python is not already installed:

1. Download from https://www.python.org/downloads/
2. Run the installer
3. **Check "Add Python to PATH"** before clicking Install

Verify the install:
```cmd
python --version
```

---

## Step 2 — Place Files Together

Make sure these files are in the same folder:

```
your-folder\
├── itunes_dj_assistant_for_windows.py
├── itunes_dj_assistant.spec
├── build.bat
└── (optional) icon.ico        ← Your custom icon
```

---

## Step 3 — (Optional) Add Custom Icon

To customize the executable icon:

1. **Get or create a .ico file**
   - Must be `.ico` format (not `.png` or `.jpg`)
   - Recommended sizes: 16x16, 32x32, 48x48, 256x256 pixels
   - Convert PNG to ICO: https://convertio.co/png-ico/

2. **Place icon file in project folder**
   - Name it `icon.ico` or choose your own name

3. **Edit `itunes_dj_assistant.spec`**
   - Open the file in any text editor
   - Find this line near the bottom:
     ```python
     icon='icon.ico',    # UNCOMMENT THIS LINE and set your icon filename
     ```
   - It's already uncommented! Just change `icon.ico` to your filename if different
   - Save the file

4. **Rebuild** (the build script will use your icon)

---

## Step 4 — Build

**Option A: One-click (recommended)**

Double-click `build.bat`. It will automatically:
- Install PyInstaller and pywin32
- Configure pywin32
- Build the executable

**Option B: Manual**

Open Command Prompt in your folder and run:

```cmd
pip install pyinstaller pywin32 --upgrade
pyinstaller itunes_dj_assistant.spec --clean
```

---

## Step 5 — Find Your Executable

After a successful build, your executable is at:

```
your-folder\
└── dist\
    └── iTunes DJ Assistant.exe    <-- this is your app
```

The `dist\` folder also contains supporting files that must stay
alongside the `.exe`. To distribute, zip the entire `dist\` folder.

---

## Distributing to Another Machine

The target machine needs **no Python installation**. Just copy and run
`iTunes DJ Assistant.exe`.

**Requirements on the target machine:**
- Windows 10 or 11
- iTunes installed
- No other software needed

---

## Troubleshooting

### "Failed to execute script"
- Right-click `iTunes DJ Assistant.exe` → Run as administrator
- Check Windows Defender isn't blocking it

### Missing win32com / pythoncom errors
Run this after installing pywin32:
```cmd
python -m pywin32_postinstall -install
```
Then rebuild.

### Antivirus flags the .exe
This is a false positive common with PyInstaller builds.
Add an exclusion in your antivirus for the `dist\` folder.

### Build fails with "ModuleNotFoundError"
Make sure you're running `build.bat` from the folder containing
the script, not from a different directory.

### Icon not showing
- Make sure the icon file exists in the project folder
- Check the filename matches what's in `itunes_dj_assistant.spec`
- The line `icon='icon.ico'` should NOT have a `#` at the start
- Rebuild after making changes

### Icon looks blurry
Your .ico file should contain multiple sizes (16x16, 32x32, 48x48, 256x256).
Use a proper ICO converter, not just renaming a PNG file.

---

## Clean Rebuild

To start fresh, delete these folders before running `build.bat`:
```
build\
dist\
__pycache__\
```

---

## Icon Tips

### Creating a Good Icon

- **Size:** Include 16x16, 32x32, 48x48, and 256x256 in one .ico file
- **Design:** Simple, recognizable shapes work best at small sizes
- **Colors:** High contrast works better than subtle gradients
- **Testing:** Test at 16x16 size — that's how it appears in taskbar

### Icon Resources

Free icon tools:
- **IcoFX** - Free ICO editor for Windows
- **GIMP** - Free, can export to ICO format
- **Online converters:** https://convertio.co/png-ico/

Free icon libraries:
- **IconArchive** - https://iconarchive.com/
- **Flaticon** - https://flaticon.com/ (check license)
- **Icons8** - https://icons8.com/ (check license)

### Example: Music/DJ Icons

Search for:
- "music note icon"
- "DJ icon"  
- "headphones icon"
- "turntable icon"
- "vinyl record icon"

Download as PNG, then convert to ICO with multiple sizes.


## Prerequisites

All of the following must be done on a **Windows machine** — PyInstaller
builds platform-specific executables and cannot cross-compile.

---

## Step 1 — Install Python

If Python is not already installed:

1. Download from https://www.python.org/downloads/
2. Run the installer
3. **Check "Add Python to PATH"** before clicking Install

Verify the install:
```cmd
python --version
```

---

## Step 2 — Place Files Together

Make sure these three files are in the same folder:

```
your-folder\
├── itunes_file_opener_windows.py
├── itunes_monitor.spec
└── build.bat
```

---

## Step 3 — Build

**Option A: One-click (recommended)**

Double-click `build.bat`. It will automatically:
- Install PyInstaller and pywin32
- Configure pywin32
- Build the executable

**Option B: Manual**

Open Command Prompt in your folder and run:

```cmd
pip install pyinstaller pywin32 --upgrade
pyinstaller itunes_dj_assistant.spec --clean
```

---

## Step 4 — Find Your Executable

After a successful build, your executable is at:

```
your-folder\
└── dist\
    └── iTunes Monitor.exe    <-- this is your app
```

The `dist\` folder also contains supporting files that must stay
alongside the `.exe`. To distribute, zip the entire `dist\` folder.

---

## Optional: Add a Custom Icon

1. Prepare a `.ico` file (e.g. `icon.ico`) in the same folder
2. Open `itunes_monitor.spec` and find this line:
   ```python
   # icon='icon.ico',
   ```
3. Uncomment it (remove the `#`) and save
4. Rebuild with `build.bat`

You can convert a PNG to ICO free at https://convertio.co/png-ico/

---

## Distributing to Another Machine

The target machine needs **no Python installation**. Just copy and run
`iTunes Monitor.exe`.

**Requirements on the target machine:**
- Windows 10 or 11
- iTunes installed
- No other software needed

---

## Troubleshooting

### "Failed to execute script"
- Right-click `iTunes Monitor.exe` → Run as administrator
- Check Windows Defender isn't blocking it

### Missing win32com / pythoncom errors
Run this after installing pywin32:
```cmd
python -m pywin32_postinstall -install
```
Then rebuild.

### Antivirus flags the .exe
This is a false positive common with PyInstaller builds.
Add an exclusion in your antivirus for the `dist\` folder.

### Build fails with "ModuleNotFoundError"
Make sure you're running `build.bat` from the folder containing
the script, not from a different directory.

---

## Clean Rebuild

To start fresh, delete these folders before running `build.bat`:
```
build\
dist\
__pycache__\
```
