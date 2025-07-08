@echo off
REM Build script for Windows - Creates distributable Peregrine Speak packages

echo Starting Peregrine Speak build process...

REM Check if we're in the right directory
if not exist "main.py" (
    echo Error: main.py not found. Please run this script from the project root.
    pause
    exit /b 1
)

REM Create build directories
echo Creating build directories...
if not exist "build" mkdir build
if not exist "dist" mkdir dist
if not exist "releases" mkdir releases

REM Check if virtual environment exists
if not exist ".venv" (
    echo Error: Virtual environment not found. Please run:
    echo    python -m venv .venv
    echo    .venv\Scripts\activate
    echo    pip install -r requirements-build.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install build dependencies
echo Installing build dependencies...
pip install -r requirements-build.txt

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist\PeregrineSpeak" rmdir /s /q "dist\PeregrineSpeak"
if exist "build" rmdir /s /q "build" && mkdir build

REM Run PyInstaller
echo Building executable with PyInstaller...
pyinstaller peregrine_speak.spec --clean --noconfirm

REM Check if build was successful
if not exist "dist\PeregrineSpeak" (
    echo Build failed! PeregrineSpeak directory not found in dist/
    pause
    exit /b 1
)

REM Create release package
set VERSION=v1.0.0
set PLATFORM=windows
set ARCH=x64
set PACKAGE_NAME=PeregrineSpeak-%VERSION%-%PLATFORM%-%ARCH%
set PACKAGE_PATH=releases\%PACKAGE_NAME%

echo Creating release package: %PACKAGE_NAME%

REM Copy built application
xcopy "dist\PeregrineSpeak" "%PACKAGE_PATH%\" /E /I /Y

REM Copy documentation
echo Adding documentation...
copy README.md "%PACKAGE_PATH%\"
copy requirements.txt "%PACKAGE_PATH%\"

REM Create installation guide (same content as Linux version)
echo Creating installation guide...
(
echo # Peregrine Speak - Installation Guide
echo.
echo ## Quick Start
echo.
echo ### Windows
echo 1. Extract the package
echo 2. Double-click `PeregrineSpeak.exe`
echo.
echo ### Alternative
echo 1. Extract the package  
echo 2. Double-click `run_peregrine_speak.bat`
echo.
echo ## System Requirements
echo.
echo - **Operating System**: Windows 10 or higher
echo - **Memory**: 4GB RAM minimum, 8GB recommended
echo - **Storage**: 2GB free space for models and cache
echo - **Audio**: Working audio output device
echo - **Network**: Internet connection for first-time voice model download
echo.
echo ## First Run
echo.
echo On first launch, Peregrine Speak will:
echo 1. Download AI voice models ^(~500MB^)
echo 2. Initialize the speech engine
echo 3. Display the welcome screen
echo.
echo This may take 2-5 minutes depending on your internet connection.
echo.
echo Enjoy natural AI speech synthesis with Peregrine Speak! 🦅🗣️
) > "%PACKAGE_PATH%\INSTALLATION.md"

REM Create archive using PowerShell
echo Creating compressed archive...
powershell -command "Compress-Archive -Path 'releases\%PACKAGE_NAME%' -DestinationPath 'releases\%PACKAGE_NAME%.zip' -Force"

echo Build completed successfully!
echo.
echo Build Summary:
echo    Package: %PACKAGE_NAME%
echo    Location: releases\
echo    Files created:
echo      - %PACKAGE_NAME%.zip
echo      - %PACKAGE_NAME%\ ^(directory^)
echo.
echo Ready for distribution!
echo Users can download and extract the archive, then run PeregrineSpeak.exe

pause
