# Creating a GitHub Release with Executable

This guide shows you how to distribute your compiled `.exe` file alongside the source code on GitHub using Releases.

---

## Why Use GitHub Releases?

✅ **Best Practice:** Keep the `.exe` out of version control (binary files shouldn't be in Git)  
✅ **Clean Repository:** Source code stays clean and small  
✅ **Easy Downloads:** Users can download pre-built executables without cloning the repo  
✅ **Version Tracking:** Each release is versioned and documented  

---

## Part 1: Build Your Executable

### 1. Build on Windows

On your Windows machine:

```bash
# Navigate to project folder
cd path\to\itunes-dj-assistant-for-windows

# Run the build script
build.bat
```

Or manually:
```bash
pip install pyinstaller pywin32 --upgrade
pyinstaller itunes_dj_assistant.spec --clean
```

### 2. Locate Your Executable

After building, you'll have:
```
dist\
├── iTunes DJ Assistant.exe           ← Main executable
└── [various DLL and support files]
```

### 3. Create Distribution ZIP

**Important:** The `.exe` needs the supporting files to run!

**On Windows:**
1. Navigate to the `dist\` folder
2. Select ALL files in the folder
3. Right-click → **Send to** → **Compressed (zipped) folder**
4. Rename to: `iTunes-Monitor-v1.0.0-Windows.zip`

**Or use 7-Zip/WinRAR:**
```bash
# In the dist\ folder
7z a iTunes-Monitor-v1.0.0-Windows.zip *
```

---

## Part 2: Create GitHub Release

### Option A: Using GitHub Website (Easiest)

1. **Go to your repository on GitHub.com**
   ```
   https://github.com/yourusername/itunes-dj-assistant-for-windows
   ```

2. **Click "Releases"** (right sidebar)

3. **Click "Create a new release"**

4. **Choose a tag:**
   - Click "Choose a tag" dropdown
   - Type: `v1.0.0` (or your version number)
   - Click "Create new tag: v1.0.0 on publish"

5. **Fill in release details:**
   - **Release title:** `v1.0.0 - First Release`
   - **Description:**
     ```markdown
     ## iTunes DJ Assistant v1.0.0
     
     First stable release of iTunes DJ Assistant!
     
     ### 🎉 Features
     - GUI-based configuration
     - Real-time iTunes monitoring
     - Customizable display fields
     - Auto HTML generation
     - Smart file search
     
     ### 📥 Download
     
     **For most users:** Download the `.zip` file below and extract it.
     No Python installation required!
     
     **For developers:** Clone the repository to access the source code.
     
     ### 📋 Requirements
     - Windows 10 or 11
     - iTunes installed
     
     ### 🚀 Quick Start
     1. Download `iTunes-Monitor-v1.0.0-Windows.zip`
     2. Extract the ZIP file
     3. Run `iTunes DJ Assistant.exe`
     4. Configure and enjoy!
     
     ### 📝 Changelog
     - Initial release
     - Full GUI implementation
     - PyInstaller packaging
     ```

6. **Attach files:**
   - Click "Attach binaries by dropping them here or selecting them"
   - Upload `iTunes-Monitor-v1.0.0-Windows.zip`

7. **Publish:**
   - ✅ Check "Set as the latest release" (if it's your newest)
   - Click **"Publish release"**

### Option B: Using PyCharm

1. **Tag your commit:**
   - **VCS** → **Git** → **Tag...**
   - Tag name: `v1.0.0`
   - Message: "First stable release"
   - Click **Create Tag**

2. **Push the tag:**
   - **VCS** → **Git** → **Push**
   - Check ✅ **"Push Tags"**
   - Click **Push**

3. **Create release on GitHub:**
   - Go to GitHub.com
   - Follow steps 2-7 from Option A above

---

## Part 3: Update Your README

Add download instructions to your `README.md`:

```markdown
## 🚀 Quick Start

### Option 1: Download Pre-Built Executable (Recommended for Users)

1. Go to [Releases](https://github.com/yourusername/itunes-dj-assistant-for-windows/releases)
2. Download the latest `iTunes-Monitor-vX.X.X-Windows.zip`
3. Extract the ZIP file to a folder
4. Run `iTunes DJ Assistant.exe`
5. No Python installation required!

### Option 2: Run from Source (For Developers)

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
```

Commit and push this change:
```bash
git add README.md
git commit -m "Update README with download instructions"
git push
```

---

## Part 4: Verify Everything Works

### For End Users (Testing the .exe):

1. Download your release ZIP from GitHub
2. Extract to a **new folder** (not your dev folder)
3. Run `iTunes DJ Assistant.exe`
4. Verify it works correctly

### For Developers (Testing source):

1. Clone your repository to a **new folder**
2. Follow the "Run from Source" instructions
3. Verify the source code works

---

## Part 5: Future Releases

### When to Create a New Release

Create a new release when you:
- ✅ Add significant new features
- ✅ Fix important bugs
- ✅ Make breaking changes
- ✅ Improve performance

Don't create a release for:
- ❌ Minor documentation updates
- ❌ Small README changes
- ❌ Code formatting changes

### Version Numbering

Use [Semantic Versioning](https://semver.org/):

```
v1.2.3
  │ │ │
  │ │ └─ PATCH: Bug fixes, minor changes
  │ └─── MINOR: New features, backwards compatible
  └───── MAJOR: Breaking changes
```

Examples:
- `v1.0.0` - First release
- `v1.0.1` - Bug fix
- `v1.1.0` - Added new feature
- `v2.0.0` - Major rewrite

### Creating a New Release

1. **Update version in code** (if applicable)
2. **Build new executable:**
   ```bash
   pyinstaller itunes_dj_assistant.spec --clean
   ```
3. **Create new ZIP:**
   ```
   iTunes-Monitor-v1.1.0-Windows.zip
   ```
4. **Create GitHub Release:**
   - Tag: `v1.1.0`
   - Title: `v1.1.0 - Feature Update`
   - Describe changes in release notes
   - Upload new ZIP
5. **Mark as latest release**

---

## Part 6: Best Practices

### ✅ Do's

- **Include changelog** in every release
- **Test the executable** before releasing
- **Use clear version numbers** (v1.0.0, v1.1.0, etc.)
- **Write descriptive release notes**
- **Include system requirements** in release notes
- **Keep old releases** available (don't delete them)

### ❌ Don'ts

- **Don't commit `.exe` files** to the repository
- **Don't commit `dist/` or `build/` folders**
- **Don't skip version numbers**
- **Don't release untested builds**
- **Don't forget to push tags** before creating releases

---

## Part 7: Advanced: Automating Releases

### Using GitHub Actions (Optional)

You can automate building and releasing with GitHub Actions. Create `.github/workflows/release.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pyinstaller pywin32
    
    - name: Build with PyInstaller
      run: |
        pyinstaller itunes_dj_assistant.spec --clean
    
    - name: Create ZIP
      run: |
        Compress-Archive -Path dist\* -DestinationPath iTunes-Monitor-${{ github.ref_name }}-Windows.zip
    
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: iTunes-Monitor-${{ github.ref_name }}-Windows.zip
        body: |
          ## iTunes DJ Assistant ${{ github.ref_name }}
          
          Auto-built release
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Then just push a tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub will automatically build and create the release!

---

## Quick Reference: Release Checklist

- [ ] Build executable with `build.bat`
- [ ] Test the executable
- [ ] Create distribution ZIP
- [ ] Update version number in README/code
- [ ] Commit and push all changes
- [ ] Create and push Git tag
- [ ] Create GitHub Release
- [ ] Upload ZIP file
- [ ] Write release notes
- [ ] Publish release
- [ ] Test download link
- [ ] Announce release (if applicable)

---

## Example Release Notes Template

```markdown
## iTunes DJ Assistant vX.X.X

[Brief description of the release]

### ✨ New Features
- Feature 1 description
- Feature 2 description

### 🐛 Bug Fixes
- Fix for issue #1
- Fix for issue #2

### 🔧 Improvements
- Performance improvement
- UI enhancement

### 📥 Installation

**Windows Users:**
1. Download `iTunes-Monitor-vX.X.X-Windows.zip` below
2. Extract the ZIP file
3. Run `iTunes DJ Assistant.exe`

**Developers:**
```bash
git clone https://github.com/yourusername/itunes-dj-assistant-for-windows.git
cd itunes-dj-assistant-for-windows
git checkout vX.X.X
pip install -r requirements.txt
python itunes_dj_assistant_for_windows.py
```

### 📋 Requirements
- Windows 10 or 11
- iTunes installed

### ⚠️ Known Issues
- Issue 1 (if any)
- Issue 2 (if any)

### 🙏 Contributors
Thanks to everyone who contributed!
```

---

## Support

If you have questions about creating releases:
- Check [GitHub Docs - Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- Open an issue in your repository
- Check the PyInstaller documentation

---

**Your users will love the easy download option! 🎉**
