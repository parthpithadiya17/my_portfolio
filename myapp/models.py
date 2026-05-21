from django.db import models
from django.utils.text import slugify
from django.utils.html import strip_tags
import math
import json


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.role} at {self.company}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    company = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()
    tech_stack = models.CharField(max_length=300)

    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)

    image = models.ImageField(upload_to="projects/", blank=True, null=True)

    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def tech_list(self):
        return [tech.strip() for tech in self.tech_stack.split(",") if tech.strip()]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_published = models.BooleanField(default=True)

    image = models.ImageField(upload_to="blogs/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def read_time(self):
        words = len(strip_tags(self.content).split())
        return max(1, math.ceil(words / 200))

    def get_clean_content(self):
        if self.content.startswith('{"ops"'):
            try:
                data = json.loads(self.content)
            except json.JSONDecodeError:
                return self.content

            return "".join(op.get("insert", "") for op in data.get("ops", [])).replace("\n", "<br>")
        return self.content

    def __str__(self):
        return self.title
