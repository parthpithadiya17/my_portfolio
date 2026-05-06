import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings


SKILL_GROUPS = (
    ("Languages & Frameworks", "braces", "languages_frameworks"),
    ("Databases", "database", "databases"),
    ("Tools & DevOps", "container", "tools_devops"),
    ("Backend Concepts", "workflow", "concepts"),
    ("Data Libraries", "bar-chart-3", "data_libraries"),
)


@lru_cache(maxsize=1)
def load_cv():
    data_path = Path(settings.CV_DATA_PATH)
    with data_path.open(encoding="utf-8") as cv_file:
        return json.load(cv_file)


def build_skill_groups(cv):
    skills = cv.get("skills", {})
    return [
        {
            "label": label,
            "icon": icon,
            "items": skills.get(key, []),
        }
        for label, icon, key in SKILL_GROUPS
    ]


def build_contact_links(cv):
    contact = cv.get("contact_links", {})
    email = contact.get("email", "")
    phone = contact.get("phone", "")

    return [
        {
            "label": "Email",
            "value": email,
            "href": f"mailto:{email}" if email else "#contact",
            "icon": "mail",
        },
        {
            "label": "Phone",
            "value": phone,
            "href": f"tel:{phone.replace(' ', '')}" if phone else "#contact",
            "icon": "phone",
        },
        {
            "label": "Location",
            "value": contact.get("location", ""),
            "href": "#contact",
            "icon": "map-pin",
        },
        {
            "label": "LinkedIn",
            "value": "parth-pithadiya",
            "href": contact.get("linkedin", "#"),
            "icon": "fa-linkedin",
            "type": "fa",
        },
        {
            "label": "GitHub",
            "value": "parth-pithadiya",
            "href": contact.get("github", "#"),
            "icon": "fa-github",
            "type": "fa",
        },
    ]


def build_cv_context():
    cv = load_cv()
    return {
        "cv": cv,
        "skill_groups": build_skill_groups(cv),
        "contact_links": build_contact_links(cv),
    }
