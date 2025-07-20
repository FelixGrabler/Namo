import asyncio
import aiohttp
import os
from typing import Optional
from datetime import datetime
import json

from utils.logging_config import APP_LOGGER


class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    async def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Send a message to Telegram."""
        if not self.bot_token or not self.chat_id:
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
                        APP_LOGGER.error(
                            f"Failed to send Telegram notification: {response.status}"
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
        """Send a formatted error notification to Telegram."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"""
🚨 <b>NAMO API ERROR</b> 🚨

<b>Time:</b> {timestamp}
<b>Context:</b> {context if context else 'Unknown'}
<b>Error Type:</b> {error_details.get('exception_type', 'Unknown')}
<b>Error Message:</b> {error_details.get('exception_message', 'No message')}

<b>Traceback:</b>
<pre>{error_details.get('traceback', 'No traceback available')[:1000]}</pre>

#NamoAPI #Error #Backend
"""

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
        message = f"""
✅ <b>NAMO API STARTED</b>

<b>Time:</b> {timestamp}
<b>Status:</b> API is now running
<b>Environment:</b> {os.getenv('ENVIRONMENT', 'development')}

#NamoAPI #Startup #Backend
"""
        return await self.send_message(message)

    async def send_critical_error_notification(self, error_message: str) -> bool:
        """Send a critical error notification."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""
🔥 <b>CRITICAL ERROR - NAMO API</b> 🔥

<b>Time:</b> {timestamp}
<b>Message:</b> {error_message}

This requires immediate attention!

#NamoAPI #Critical #Emergency
"""
        return await self.send_message(message)


# Global instance
telegram_notifier = TelegramNotifier()
