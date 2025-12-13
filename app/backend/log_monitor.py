#!/usr/bin/env python3
"""
Log monitoring script for Namo API.
Shows real-time information about log files and can trigger rotation.
"""

import sys
import os
import time
from pathlib import Path

# Add the backend directory to Python path (works both locally and in Docker)
backend_dir = Path(__file__).parent.absolute()
sys.path.append(str(backend_dir))

from utils.logging_config import (
    get_log_files_info,
    get_log_config_info,
    force_log_rotation,
)


def format_size(size_mb):
    """Format file size with appropriate units."""
    if size_mb < 1:
        return f"{size_mb * 1024:.1f} KB"
    return f"{size_mb:.1f} MB"


def print_log_status():
    """Print current log file status."""
    print("\n" + "=" * 60)
    print("📊 NAMO API LOG STATUS")
    print("=" * 60)

    # Configuration info
    config = get_log_config_info()
    print(f"📁 Logs Directory: {config['logs_directory']}")
    print(f"📏 Max File Size: {config['max_file_size_mb']} MB")
    print(f"🔄 Backup Count: {config['backup_count']}")
    print(f"📈 Log Level: {config['log_level']}")
    print(f"💻 Console Logging: {'✅' if config['console_logging'] else '❌'}")
    print(f"💾 Max Disk Usage: ~{config['estimated_max_disk_usage_mb']} MB")

    print("\n📄 LOG FILES:")
    print("-" * 60)

    # File info
    files = get_log_files_info()
    total_size = 0

    for log_type, info in files.items():
        if info["exists"]:
            size_mb = info["size_mb"]
            total_size += size_mb
            percentage = (size_mb / config["max_file_size_mb"]) * 100

            # Progress bar
            bar_length = 20
            filled_length = int(bar_length * percentage / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)

            print(
                f"{log_type:12} │ {format_size(size_mb):>8} │ [{bar}] {percentage:5.1f}%"
            )

            # Show rotated files if they exist
            if "rotated_files" in info:
                for rotated in info["rotated_files"]:
                    total_size += rotated["size_mb"]
                    print(
                        f"  {rotated['file']:10} │ {format_size(rotated['size_mb']):>8} │ (archived)"
                    )
        else:
            print(
                f"{log_type:12} │ {'Not yet created':>8} │ [░░░░░░░░░░░░░░░░░░░░]   0.0%"
            )

    print("-" * 60)
    print(f"Total Size: {format_size(total_size)}")

    # Check if any files are near rotation threshold
    warnings = []
    for log_type, info in files.items():
        if info["exists"]:
            percentage = (info["size_mb"] / config["max_file_size_mb"]) * 100
            if percentage > 80:
                warnings.append(f"{log_type} is {percentage:.1f}% full")

    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   • {warning}")


def main():
    """Main monitoring function."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "rotate":
            print("🔄 Manually rotating logs...")
            success = force_log_rotation()
            if success:
                print("✅ Log rotation completed successfully!")
            else:
                print("❌ Log rotation failed!")
            return

        elif command == "watch":
            print("👀 Watching logs (press Ctrl+C to stop)...")
            try:
                while True:
                    os.system("clear" if os.name == "posix" else "cls")
                    print_log_status()
                    print(f"\n🕐 Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print("Press Ctrl+C to stop watching...")
                    time.sleep(5)
            except KeyboardInterrupt:
                print("\n👋 Stopped watching logs.")
            return

        elif command == "help":
            print("📖 Namo API Log Monitor")
            print("Usage:")
            print("  python log_monitor.py          - Show current status")
            print("  python log_monitor.py rotate   - Manually rotate logs")
            print("  python log_monitor.py watch    - Watch logs in real-time")
            print("  python log_monitor.py help     - Show this help")
            return

        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python log_monitor.py help' for usage information.")
            return

    # Default: show current status
    print_log_status()
    print(f"\n💡 Tip: Use 'python log_monitor.py help' for more options")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
