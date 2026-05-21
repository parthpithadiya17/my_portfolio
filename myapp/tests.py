import json
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="me@parthpithadiya.in",
    CONTACT_EMAIL="me@parthpithadiya.in",
)
class ContactApiTests(TestCase):
    def post_contact(self, payload):
        return self.client.post(
            reverse("contact_api"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_contact_api_saves_message_and_sends_email(self):
        response = self.post_contact(
            {
                "name": "Visitor",
                "email": "visitor@example.com",
                "subject": "Hello",
                "message": "I want to connect.",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ["visitor@example.com"])

    def test_contact_api_rejects_invalid_email(self):
        response = self.post_contact(
            {
                "name": "Visitor",
                "email": "not-an-email",
                "subject": "Hello",
                "message": "I want to connect.",
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_api_reports_mail_send_failure(self):
        with patch("myapp.views.EmailMessage.send", side_effect=OSError("SMTP unavailable")):
            response = self.post_contact(
                {
                    "name": "Visitor",
                    "email": "visitor@example.com",
                    "subject": "Hello",
                    "message": "I want to connect.",
                }
            )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["status"], "error")
