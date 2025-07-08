#!/usr/bin/env python3
"""
Quick setup script for Peregrine Speak development environment.
This script helps users set up the development environment quickly.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Peregrine Speak Quick Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Please run this script from the project root.")
        return False
    
    # Create virtual environment
    if not Path(".venv").exists():
        if not run_command(f"{sys.executable} -m venv .venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation command
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate && "
        pip_cmd = ".venv\\Scripts\\pip"
    else:  # Linux/macOS
        activate_cmd = "source .venv/bin/activate && "
        pip_cmd = ".venv/bin/pip"
    
    # Upgrade pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Test the installation
    print("\n🧪 Testing installation...")
    test_cmd = f"{activate_cmd}python test_kokoro_integration.py"
    
    print("Running test (this may take a few minutes on first run)...")
    try:
        result = subprocess.run(test_cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ Test completed successfully!")
        print("\n" + "="*50)
        print("🎉 Setup completed successfully!")
        print("\nTo run Peregrine Speak:")
        if os.name == 'nt':
            print("  1. .venv\\Scripts\\activate")
        else:
            print("  1. source .venv/bin/activate")
        print("  2. python main.py")
        print("\nOr use the quick start:")
        if os.name == 'nt':
            print("  .venv\\Scripts\\activate && python main.py")
        else:
            print("  source .venv/bin/activate && python main.py")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Test failed: {e.stderr}")
        print("\nSetup completed but test failed. You may need to:")
        print("- Check your internet connection")
        print("- Ensure audio drivers are installed")
        print("- Try running manually: python test_kokoro_integration.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
