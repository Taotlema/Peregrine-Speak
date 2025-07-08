#!/bin/bash
"""
Build script for creating distributable Peregrine Speak packages.
This script creates standalone executables for different platforms.
"""

set -e  # Exit on error

echo "🚀 Starting Peregrine Speak build process..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root."
    exit 1
fi

# Create build directory
BUILD_DIR="build"
DIST_DIR="dist"
RELEASE_DIR="releases"

echo "📁 Creating build directories..."
mkdir -p "$BUILD_DIR"
mkdir -p "$DIST_DIR" 
mkdir -p "$RELEASE_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements-build.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install -r requirements-build.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf "$DIST_DIR/PeregrineSpeak"
rm -rf "$BUILD_DIR"/*

# Run PyInstaller
echo "🔨 Building executable with PyInstaller..."
pyinstaller peregrine_speak.spec --clean --noconfirm

# Check if build was successful
if [ ! -d "$DIST_DIR/PeregrineSpeak" ]; then
    echo "❌ Build failed! PeregrineSpeak directory not found in dist/"
    exit 1
fi

# Get version info
VERSION=$(python -c "import sys; sys.path.insert(0, 'src'); from peregrine_speak.app import PeregrineApp; print('v1.0.0')")
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Create release package
PACKAGE_NAME="PeregrineSpeak-${VERSION}-${PLATFORM}-${ARCH}"
PACKAGE_PATH="$RELEASE_DIR/$PACKAGE_NAME"

echo "📦 Creating release package: $PACKAGE_NAME"

# Copy built application
cp -r "$DIST_DIR/PeregrineSpeak" "$PACKAGE_PATH"

# Create launcher script
cat > "$PACKAGE_PATH/run_peregrine_speak.sh" << 'EOF'
#!/bin/bash
# Peregrine Speak Launcher Script

cd "$(dirname "$0")"

# Set library paths (Linux)
export LD_LIBRARY_PATH="$PWD:$LD_LIBRARY_PATH"

# Run the application
./PeregrineSpeak "$@"
EOF

chmod +x "$PACKAGE_PATH/run_peregrine_speak.sh"

# Create Windows batch file
cat > "$PACKAGE_PATH/run_peregrine_speak.bat" << 'EOF'
@echo off
REM Peregrine Speak Launcher Script for Windows

cd /d "%~dp0"
PeregrineSpeak.exe %*
EOF

# Copy documentation
echo "📚 Adding documentation..."
cp README.md "$PACKAGE_PATH/"
cp requirements.txt "$PACKAGE_PATH/"

# Create installation guide
cat > "$PACKAGE_PATH/INSTALLATION.md" << 'EOF'
# Peregrine Speak - Installation Guide

## Quick Start

### Linux/macOS
1. Extract the package
2. Open terminal in the extracted folder
3. Run: `./run_peregrine_speak.sh`

### Windows
1. Extract the package
2. Double-click `run_peregrine_speak.bat`
3. Or double-click `PeregrineSpeak.exe` directly

## System Requirements

- **Operating System**: Linux, macOS, or Windows 10+
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for models and cache
- **Audio**: Working audio output device
- **Network**: Internet connection for first-time voice model download

## First Run

On first launch, Peregrine Speak will:
1. Download AI voice models (~500MB)
2. Initialize the speech engine
3. Display the welcome screen

This may take 2-5 minutes depending on your internet connection.

## Troubleshooting

### No Audio Output
- Check system volume and audio device
- Try different audio output device in system settings
- Restart the application

### Slow Performance
- Close other applications to free up memory
- On first run, wait for model download to complete
- Use shorter text segments for faster processing

### Application Won't Start
- Check that you have audio drivers installed
- Try running from terminal to see error messages:
  - Linux/macOS: `./PeregrineSpeak`
  - Windows: Open Command Prompt and run `PeregrineSpeak.exe`

## Support

For additional help:
- Check README.md for detailed documentation
- Visit our GitHub repository for issues and updates
- Review system requirements above

Enjoy natural AI speech synthesis with Peregrine Speak! 🦅🗣️
EOF

# Create archive
echo "📦 Creating compressed archive..."
cd "$RELEASE_DIR"
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"
zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME" >/dev/null 2>&1 || echo "⚠️ zip not available, skipping .zip creation"

cd ..

# Calculate sizes
TAR_SIZE=$(du -h "$RELEASE_DIR/${PACKAGE_NAME}.tar.gz" | cut -f1)
echo "✅ Build completed successfully!"
echo ""
echo "📋 Build Summary:"
echo "   Package: $PACKAGE_NAME"
echo "   Location: $RELEASE_DIR/"
echo "   Archive size: $TAR_SIZE"
echo "   Files created:"
echo "     - ${PACKAGE_NAME}.tar.gz"
echo "     - ${PACKAGE_NAME}/ (directory)"
echo ""
echo "🚀 Ready for distribution!"
echo "   Users can download and extract the archive, then run:"
echo "   Linux/macOS: ./run_peregrine_speak.sh"
echo "   Windows: run_peregrine_speak.bat"
