# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Peregrine Speak application.
Creates a standalone executable with all dependencies bundled.
"""

import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()
src_dir = current_dir / 'src'
assets_dir = current_dir / 'assets'

# Define data files to include
datas = [
    (str(assets_dir), 'assets'),  # Include all assets
]

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'torch',
    'torchaudio', 
    'numpy',
    'scipy',
    'pygame',
    'sounddevice',
    'soundfile',
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'kokoro',
    'misaki',
    'pathlib',
    'threading',
    'queue',
    'tempfile',
    'logging',
    'peregrine_speak.app',
    'peregrine_speak.tts.kokoro_engine',
    'peregrine_speak.ui.home_screen',
    'peregrine_speak.ui.main_screen',
    'peregrine_speak.ui.voice_selection',
]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(current_dir), str(src_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # Exclude unnecessary packages to reduce size
        'pandas',
        'jupyter',
        'IPython',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PeregrineSpeak',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Hide console window on Windows
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(assets_dir / 'icons' / 'peregrine_ai_logo.jpeg') if (assets_dir / 'icons' / 'peregrine_ai_logo.jpeg').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PeregrineSpeak',
)
