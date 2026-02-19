# iTunes DJ Assistant - PyInstaller spec file
# 
# CUSTOM ICON INSTRUCTIONS:
# ========================
# To add your own icon to the executable:
# 1. Get or create a .ico file (must be .ico format, not .png or .jpg)
# 2. Place the icon file in the same folder as this spec file
# 3. Uncomment the icon line below (remove the # at the start)
# 4. Change 'icon.ico' to your icon filename
# 5. Rebuild with: pyinstaller itunes_dj_assistant.spec --clean
#
# To convert PNG/JPG to ICO:
# - Use online converter: https://convertio.co/png-ico/
# - Or use GIMP, Photoshop, or other image editor
# - Recommended sizes: 16x16, 32x32, 48x48, 256x256 pixels
#
# Run with: pyinstaller itunes_dj_assistant.spec

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['itunes_dj_assistant_for_windows.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'win32com',
        'win32com.client',
        'win32com.server',
        'pythoncom',
        'pywintypes',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='iTunes DJ Assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # No console window - GUI only
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',    # UNCOMMENT THIS LINE and set your icon filename
)
