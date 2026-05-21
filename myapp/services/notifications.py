import logging

import requests
from django.conf import settings
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)


def send_contact_email(message):
    if not settings.CONTACT_EMAIL:
        logger.warning("CONTACT_EMAIL is not configured; skipping contact email.")
        return

    email_msg = EmailMessage(
        subject=f"Portfolio Contact: {message.subject}",
        body=(
            f"Name: {message.name}\n"
            f"Email: {message.email}\n"
            f"Company: {message.company or '-'}\n\n"
            f"Message:\n{message.message}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL],
        reply_to=[message.email],
    )
    email_msg.send(fail_silently=False)


def send_contact_telegram(message):
    if not settings.TELEGRAM_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.info("Telegram credentials are not configured; skipping Telegram notification.")
        return

    response = requests.post(
        f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": (
                "New portfolio message\n\n"
                f"Name: {message.name}\n"
                f"Email: {message.email}\n"
                f"Company: {message.company or '-'}\n"
                f"Type: {message.subject}\n\n"
                f"{message.message}"
            ),
        },
        timeout=10,
    )
    response.raise_for_status()
