#!/usr/bin/env python3
"""
Simple path verification script for Docker compatibility.
"""

import sys
import os
from pathlib import Path


def test_paths():
    """Test that paths work correctly in both local and Docker environments."""
    print("🔍 Path Verification Test")
    print("=" * 40)

    # Current working directory
    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")

    # Script location
    script_dir = Path(__file__).parent.absolute()
    print(f"Script directory: {script_dir}")

    # Expected logs directory
    logs_dir = script_dir / "logs"
    print(f"Logs directory: {logs_dir}")
    print(f"Logs directory exists: {logs_dir.exists()}")

    # Test creating the logs directory
    try:
        logs_dir.mkdir(exist_ok=True)
        print("✅ Logs directory created/verified")
    except Exception as e:
        print(f"❌ Failed to create logs directory: {e}")
        return False

    # Test writing to logs directory
    test_file = logs_dir / "test.txt"
    try:
        test_file.write_text("Test log file")
        print("✅ Can write to logs directory")
        test_file.unlink()  # Clean up
        print("✅ Test file cleaned up")
    except Exception as e:
        print(f"❌ Failed to write to logs directory: {e}")
        return False

    # Test Python path
    sys.path.append(str(script_dir))
    print(f"✅ Added to Python path: {script_dir}")

    # Test importing utils
    try:
        from utils.logging_config import LOGS_DIR

        print(f"✅ Successfully imported logging config")
        print(f"   LOGS_DIR from config: {LOGS_DIR}")
        print(f"   LOGS_DIR exists: {LOGS_DIR.exists()}")
    except Exception as e:
        print(f"❌ Failed to import logging config: {e}")
        return False

    print("\n🎉 All path tests passed!")
    return True


if __name__ == "__main__":
    success = test_paths()
    sys.exit(0 if success else 1)
