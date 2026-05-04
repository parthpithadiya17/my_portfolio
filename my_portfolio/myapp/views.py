import json
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render

from .models import ContactMessage
from django.views.decorators.csrf import csrf_exempt


def home(request):
    data_path = Path(settings.BASE_DIR).parent / "Parth_Pithadiya_CV.json"

    with data_path.open(encoding="utf-8") as cv_file:
        cv = json.load(cv_file)

    skill_groups = [
        {
            "label": "Languages & Frameworks",
            "icon": "braces",
            "items": cv["skills"]["languages_frameworks"],
        },
        {
            "label": "Databases",
            "icon": "database",
            "items": cv["skills"]["databases"],
        },
        {
            "label": "Tools & DevOps",
            "icon": "container",
            "items": cv["skills"]["tools_devops"],
        },
        {
            "label": "Backend Concepts",
            "icon": "workflow",
            "items": cv["skills"]["concepts"],
        },
        {
            "label": "Data Libraries",
            "icon": "chart-no-axes-combined",
            "items": cv["skills"]["data_libraries"],
        },
    ]
    contact_links = [
        {
            "label": "Email",
            "value": cv["contact_links"]["email"],
            "href": f"mailto:{cv['contact_links']['email']}",
            "icon": "mail",
        },
        {
            "label": "Phone",
            "value": cv["contact_links"]["phone"],
            "href": f"tel:{cv['contact_links']['phone'].replace(' ', '')}",
            "icon": "phone",
        },
        {
            "label": "Location",
            "value": cv["contact_links"]["location"],
            "href": "#contact",
            "icon": "map-pin",
        },
        {
            "label": "LinkedIn",
            "value": "parth-pithadiya",
            "href": cv["contact_links"]["linkedin"],
            "icon": "fa-linkedin",
            "type": "fa",
        },
        {
            "label": "GitHub",
            "value": "parth-pithadiya",
            "href": cv["contact_links"]["github"],
            "icon": "fa-github",
            "type": "fa",
        },
    ]

    return render(
        request,
        "myapp/premium_home.html",
        {
            "cv": cv,
            "skill_groups": skill_groups,
            "contact_links": contact_links,
        },
    )


@csrf_exempt
def contact_api(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"}, status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid request body"}, status=400
        )

    name = (data.get("name") or "").strip()
    visitor_email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "Portfolio contact message").strip()
    message = (data.get("message") or "").strip()
    company = (data.get("company") or "").strip()
    position = (data.get("position") or "").strip()
    project_type = (data.get("project_type") or "").strip()

    if not name or not visitor_email or not message:
        return JsonResponse(
            {"status": "error", "message": "Name, email, and message are required"},
            status=400,
        )

    try:
        validate_email(visitor_email)
    except ValidationError:
        return JsonResponse(
            {"status": "error", "message": "Enter a valid email address"}, status=400
        )

    ContactMessage.objects.create(
        name=name,
        email=visitor_email,
        subject=subject,
        message=message,
    )

    email = EmailMessage(
        subject=f"Portfolio contact: {subject}",
        body=f"Message from {name} ({visitor_email}):\n\n{message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL],
        reply_to=[visitor_email],
    )

    try:
        email.send(fail_silently=False)
    except BadHeaderError:
        return JsonResponse(
            {"status": "error", "message": "Invalid email header"},
            status=400,
        )
    except Exception as error:
        return JsonResponse(
            {"status": "error", "message": f"Could not send email: {error}"},
            status=502,
        )

    return JsonResponse({"status": "success", "message": "Message sent"})

def contact_page(request):
    data_path = Path(settings.BASE_DIR) / "Parth_Pithadiya_CV.json"

    with data_path.open(encoding="utf-8") as f:
        cv = json.load(f)

    contact_links = [
        {"label": "Email", "value": cv["contact_links"]["email"]},
        {"label": "Phone", "value": cv["contact_links"]["phone"]},
        {"label": "Location", "value": cv["contact_links"]["location"]},
    ]

    return render(request, "myapp/contact.html", {
        "cv": cv,
        "contact_links": contact_links
    })