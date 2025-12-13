#!/usr/bin/env python3
"""
Test script to demonstrate the logging and Telegram notification system.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to Python path (works both locally and in Docker)
backend_dir = Path(__file__).parent.absolute()
sys.path.append(str(backend_dir))

from utils.telegram_notifier import telegram_notifier
from utils.error_utils import send_telegram_alert, handle_error
from utils.logging_config import APP_LOGGER, ERROR_LOGGER


async def test_telegram_notifications():
    """Test Telegram notification functionality."""
    print("Testing Telegram notifications...")

    # Test basic message
    print("1. Testing basic message...")
    success = await telegram_notifier.send_message(
        "🧪 Testing Namo API logging system!"
    )
    print(f"   Basic message: {'✅ Success' if success else '❌ Failed'}")

    # Test startup notification
    print("2. Testing startup notification...")
    success = await telegram_notifier.send_startup_notification()
    print(f"   Startup notification: {'✅ Success' if success else '❌ Failed'}")

    # Test error notification
    print("3. Testing error notification...")
    try:
        # Simulate an error
        raise ValueError("This is a test error for demonstration")
    except Exception as e:
        error_details = {
            "timestamp": "2025-01-21T10:30:15.123456",
            "exception_type": type(e).__name__,
            "exception_message": str(e),
            "traceback": "Traceback (test): ValueError: This is a test error for demonstration",
        }
        success = await telegram_notifier.send_error_notification(
            error_details, "Test error context"
        )
        print(f"   Error notification: {'✅ Success' if success else '❌ Failed'}")

    # Test critical alert
    print("4. Testing critical alert...")
    success = await telegram_notifier.send_critical_error_notification(
        "Test critical error - system requires attention!"
    )
    print(f"   Critical alert: {'✅ Success' if success else '❌ Failed'}")

    # Test custom alert
    print("5. Testing custom alert...")
    await send_telegram_alert(
        "📊 Logging system test completed successfully!", is_critical=False
    )
    print("   Custom alert: ✅ Sent")


def test_logging():
    """Test logging functionality."""
    print("\nTesting logging functionality...")

    # Test app logging
    APP_LOGGER.info("Test info message from logging test")
    APP_LOGGER.warning("Test warning message from logging test")
    print("✅ App logging test completed")

    # Test error logging
    try:
        # Simulate an error for logging
        raise RuntimeError("Test runtime error for logging demonstration")
    except Exception as e:
        from utils.logging_config import log_exception

        error_details = log_exception(ERROR_LOGGER, e, "Logging test context")
        print("✅ Error logging test completed")
        print(f"   Error logged with ID: {error_details.get('timestamp')}")


def test_error_utils():
    """Test error utility functions."""
    print("\nTesting error utilities...")

    try:
        # Simulate an error that would normally trigger handle_error
        raise ConnectionError("Test database connection error")
    except Exception as e:
        try:
            # Test handle_error but don't raise HTTPException
            from utils.error_utils import handle_error

            error_details = handle_error(
                e,
                "Test error utilities",
                send_telegram=False,  # Don't spam Telegram during test
                raise_http_exception=False,
            )
            print("✅ Error utilities test completed")
            print(f"   Error handled with timestamp: {error_details.get('timestamp')}")
        except Exception as util_error:
            print(f"❌ Error utilities test failed: {util_error}")


def test_log_rotation():
    """Test log rotation functionality."""
    print("\nTesting log rotation...")

    from utils.logging_config import (
        get_log_files_info,
        get_log_config_info,
        force_log_rotation,
    )

    # Test configuration info
    config_info = get_log_config_info()
    print(f"✅ Log configuration:")
    print(f"   Max file size: {config_info['max_file_size_mb']} MB")
    print(f"   Backup count: {config_info['backup_count']}")
    print(f"   Total files per log type: {config_info['total_files_per_log']}")
    print(
        f"   Estimated max disk usage: {config_info['estimated_max_disk_usage_mb']} MB"
    )

    # Test file info
    files_info = get_log_files_info()
    print(f"✅ Current log files:")
    for log_file, info in files_info.items():
        if info["exists"]:
            print(f"   {log_file}: {info['size_mb']} MB")
            if "rotated_files" in info:
                for rotated in info["rotated_files"]:
                    print(f"     {rotated['file']}: {rotated['size_mb']} MB")
        else:
            print(f"   {log_file}: Not created yet")

    # Test manual rotation
    print("✅ Testing manual log rotation...")
    rotation_success = force_log_rotation()
    print(f"   Manual rotation: {'✅ Success' if rotation_success else '❌ Failed'}")


async def main():
    """Main test function."""
    print("🧪 Namo API Logging System Test")
    print("=" * 40)

    # Check if Telegram is configured
    telegram_configured = bool(
        os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID")
    )

    if telegram_configured:
        print("📱 Telegram configuration found - testing notifications...")
        await test_telegram_notifications()
    else:
        print("⚠️  Telegram not configured - skipping notification tests")
        print("   To enable Telegram notifications:")
        print("   1. Set TELEGRAM_BOT_TOKEN in your .env file")
        print(
            "   2. Set TELEGRAM_CHAT_ID in your .env file"
        )  # Test logging (always available)
    test_logging()

    # Test log rotation
    test_log_rotation()

    # Test error utilities
    test_error_utils()

    # Test log rotation
    test_log_rotation()

    print("\n" + "=" * 40)
    print("🎉 Logging system test completed!")
    print("\nLog files should be created in the logs/ directory:")
    print("   - logs/app.log")
    print("   - logs/errors.log")
    print("   - logs/requests.log (created when API receives requests)")


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv

    load_dotenv()

    asyncio.run(main())
