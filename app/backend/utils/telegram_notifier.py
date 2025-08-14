import asyncio
import aiohttp
import os
from typing import Optional
from datetime import datetime
import json

from utils.logging_config import APP_LOGGER
from config import get_required_secret


class TelegramNotifier:
    def __init__(self):
        # Try to get from Docker secrets first, then fallback to env vars for dev
        try:
            self.bot_token = get_required_secret(
                "telegram_bot_token", os.getenv("TELEGRAM_BOT_TOKEN")
            )
            self.chat_id = get_required_secret(
                "telegram_chat_id", os.getenv("TELEGRAM_CHAT_ID")
            )
        except Exception as e:
            APP_LOGGER.warning(f"Failed to get telegram secrets, using env vars: {e}")
            self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if self.bot_token:
            self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        else:
            self.base_url = None

    async def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Send a message to Telegram."""
        if not self.bot_token or not self.chat_id or not self.base_url:
            APP_LOGGER.warning(
                "Telegram credentials not configured. Cannot send notification."
            )
            return False

        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": parse_mode}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, json=payload) as response:
                    if response.status == 200:
                        APP_LOGGER.info("Telegram notification sent successfully")
                        return True
                    else:
                        response_text = await response.text()
                        APP_LOGGER.error(
                            f"Failed to send Telegram notification: {response.status} - {response_text}"
                        )
                        return False
        except Exception as e:
            APP_LOGGER.error(f"Error sending Telegram notification: {str(e)}")
            return False

    def send_message_sync(self, message: str, parse_mode: str = "HTML") -> bool:
        """Synchronous wrapper for sending Telegram messages."""
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.send_message(message, parse_mode))
        except RuntimeError:
            # If no event loop is running, create a new one
            return asyncio.run(self.send_message(message, parse_mode))

    async def send_error_notification(
        self, error_details: dict, context: str = ""
    ) -> bool:
        """Send a simplified error notification to Telegram."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get error details
        error_type = error_details.get("exception_type", "Unknown Error")
        error_msg = error_details.get("exception_message", "No message")
        traceback_text = error_details.get("traceback", "")

        # Create message with traceback in code format
        message = f"""🚨 NAMO API ERROR

Time: {timestamp}
Context: {context or 'Unknown'}
Error: {error_type}
Message: {error_msg}

Traceback:
```
{traceback_text[:2000]}
```

#NamoAPI #Error"""

        return await self.send_message(message)

    def send_error_notification_sync(
        self, error_details: dict, context: str = ""
    ) -> bool:
        """Synchronous wrapper for sending error notifications."""
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(
                self.send_error_notification(error_details, context)
            )
        except RuntimeError:
            return asyncio.run(self.send_error_notification(error_details, context))

    async def send_startup_notification(self) -> bool:
        """Send a notification when the API starts up."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        env = os.getenv("ENVIRONMENT", "development")
        message = f"""✅ NAMO API STARTED

Time: {timestamp}
Environment: {env}

#NamoAPI #Startup"""
        return await self.send_message(message)

    async def send_critical_error_notification(self, error_message: str) -> bool:
        """Send a critical error notification."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""🔥 CRITICAL ERROR - NAMO API

Time: {timestamp}
Message: {error_message}

#NamoAPI #Critical"""
        return await self.send_message(message)


# Global instance
telegram_notifier = TelegramNotifier()
