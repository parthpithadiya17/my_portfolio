import sqlite3
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from myapp.models import Blog, Project


class Command(BaseCommand):
    help = "Import users and blogs from the old SQLite database into the configured database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--sqlite-path",
            default=str(settings.BASE_DIR / "db.sqlite3"),
            help="Path to the old SQLite database.",
        )
        parser.add_argument(
            "--skip-users",
            action="store_true",
            help="Do not import auth users.",
        )
        parser.add_argument(
            "--skip-blogs",
            action="store_true",
            help="Do not import blog posts.",
        )
        parser.add_argument(
            "--skip-projects",
            action="store_true",
            help="Do not import projects.",
        )

    def handle(self, *args, **options):
        sqlite_path = Path(options["sqlite_path"])
        if not sqlite_path.exists():
            raise CommandError(f"SQLite database not found: {sqlite_path}")

        connection = sqlite3.connect(sqlite_path)
        connection.row_factory = sqlite3.Row

        if not options["skip_users"]:
            self.import_users(connection)

        if not options["skip_blogs"]:
            self.import_blogs(connection)

        if not options["skip_projects"]:
            self.import_projects(connection)

        connection.close()

    def import_users(self, connection):
        User = get_user_model()
        rows = connection.execute(
            """
            SELECT username, password, email, first_name, last_name,
                   is_staff, is_active, is_superuser, date_joined, last_login
            FROM auth_user
            """
        ).fetchall()

        created = 0
        updated = 0
        for row in rows:
            user, was_created = User.objects.update_or_create(
                username=row["username"],
                defaults={
                    "password": row["password"],
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "is_staff": bool(row["is_staff"]),
                    "is_active": bool(row["is_active"]),
                    "is_superuser": bool(row["is_superuser"]),
                    "date_joined": self.parse_datetime(row["date_joined"]) or timezone.now(),
                    "last_login": self.parse_datetime(row["last_login"]),
                },
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(f"Users imported: {created} created, {updated} updated."))

    def import_blogs(self, connection):
        rows = connection.execute(
            """
            SELECT title, slug, content, created_at, is_published, image
            FROM myapp_blog
            """
        ).fetchall()

        created = 0
        updated = 0
        for row in rows:
            blog, was_created = Blog.objects.update_or_create(
                slug=row["slug"],
                defaults={
                    "title": row["title"],
                    "content": row["content"],
                    "created_at": self.parse_datetime(row["created_at"]) or timezone.now(),
                    "is_published": bool(row["is_published"]),
                    "image": row["image"] or None,
                },
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(f"Blogs imported: {created} created, {updated} updated."))

    def import_projects(self, connection):
        rows = connection.execute(
            """
            SELECT title, slug, description, tech_stack, github_url, live_url,
                   image, is_featured, created_at
            FROM myapp_project
            """
        ).fetchall()

        created = 0
        updated = 0
        for row in rows:
            project, was_created = Project.objects.update_or_create(
                slug=row["slug"],
                defaults={
                    "title": row["title"],
                    "description": row["description"],
                    "tech_stack": row["tech_stack"],
                    "github_url": row["github_url"] or None,
                    "live_url": row["live_url"] or None,
                    "image": row["image"] or None,
                    "is_featured": bool(row["is_featured"]),
                    "created_at": self.parse_datetime(row["created_at"]) or timezone.now(),
                },
            )
            created += int(was_created)
            updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(f"Projects imported: {created} created, {updated} updated."))

    @staticmethod
    def parse_datetime(value):
        if not value:
            return None

        parsed = parse_datetime(value)
        if parsed and timezone.is_naive(parsed):
            return timezone.make_aware(parsed)
        return parsed
