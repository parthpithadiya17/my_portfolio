import json

from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.utils.text import slugify
from django.views.decorators.http import require_POST


from .models import ContactMessage, Project, Blog
from .services.cv import build_cv_context
from .services.notifications import send_contact_email, send_contact_telegram


def can_manage_blogs(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm("myapp.add_blog")
        or user.has_perm("myapp.change_blog")
    )


def home(request):
    context = build_cv_context()
    projects = Project.objects.order_by("-created_at")
    blogs = Blog.objects.order_by("-created_at")[:3]
    context.update({"projects": projects, "blogs": blogs})
    return render(request, "myapp/premium_home.html", context)


@require_POST
def contact_api(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    company = data.get("company", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not subject or not message:
        return JsonResponse({"status": "error", "message": "Required fields are missing"}, status=400)

    try:
        validate_email(email)
    except Exception:
        return JsonResponse({"status": "error", "message": "Invalid email address"}, status=400)

    try:
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            company=company,
            message=message,
        )
    except Exception:
        return JsonResponse({"status": "error", "message": "DB error"})

    try:
        send_contact_email(contact_message)
        send_contact_telegram(contact_message)
    except Exception as e:
        print("NOTIFICATION ERROR:", e)

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=502)

    return JsonResponse({"status": "success"})


def contact_page(request):
    return render(request, "myapp/contact.html", build_cv_context())


def blog_list(request):
    context = build_cv_context()
    blogs = Blog.objects.filter(is_published=True).order_by("-created_at")
    context.update(
        {
            "blogs": blogs,
            "can_manage_blogs": can_manage_blogs(request.user),
        }
    )
    return render(request, "myapp/blog_list.html", context)


def blog_detail(request, slug):
    context = build_cv_context()
    blog = get_object_or_404(Blog, slug=slug)
    context.update(
        {
            "blog": blog,
            "can_manage_blogs": can_manage_blogs(request.user),
        }
    )
    return render(request, "myapp/blog_detail.html", context)


def clean_quill_content(content):
    content = (content or "").strip()

    # If it's JSON (Quill Delta)
    if content.startswith('{"ops"'):
        try:
            data = json.loads(content)
            html = ""

            for op in data.get("ops", []):
                html += op.get("insert", "")

            return html
        except json.JSONDecodeError:
            return content

    return content


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin)
def blog_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        content = clean_quill_content(content)
        Blog.objects.create(
            title=title,
            slug=slugify(title),
            content=content,
        )
        return redirect("/blog/")

    return render(request, "myapp/blog_edit.html")


@user_passes_test(is_admin)
def blog_edit(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if request.method == "POST":
        blog.title = request.POST.get("title")
        blog.content = request.POST.get("content")

        blog.content = clean_quill_content(blog.content)
        blog.save()
        return redirect("/blog/")

    return render(request, "myapp/blog_edit.html", {"blog": blog})
