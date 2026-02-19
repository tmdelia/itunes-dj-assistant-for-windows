@echo off
echo ============================================================
echo  iTunes DJ Assistant - PyInstaller Build Script
echo ============================================================
echo.

:: Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Check pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available.
    pause
    exit /b 1
)

:: Install/upgrade required packages
echo [1/3] Installing required packages...
pip install pyinstaller pywin32 --upgrade
if errorlevel 1 (
    echo ERROR: Failed to install packages.
    pause
    exit /b 1
)

:: Run PyInstaller post-install script (required for pywin32)
echo.
echo [2/3] Configuring pywin32...
python -c "import pywin32_postinstall; pywin32_postinstall.install()" >nul 2>&1

:: Build the executable
echo.
echo [3/3] Building executable with PyInstaller...
pyinstaller itunes_dj_assistant.spec --clean
if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller build failed.
    echo Check the output above for details.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  BUILD SUCCESSFUL!
echo ============================================================
echo.
echo  Your executable is located at:
echo  dist\iTunes DJ Assistant.exe
echo.
echo  You can distribute this single .exe file - no Python
echo  installation required on the target machine.
echo.
echo  NOTE: To add a custom icon, see instructions in
echo        itunes_dj_assistant.spec
echo ============================================================
echo.
pause
