from django.db import models
from django.utils.html import format_html


class Teacher(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ✅ Unique
    email = models.EmailField(unique=True)  # ✅ Unique
    phone = models.CharField(max_length=20)
    address = models.TextField()
    department = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20, unique=True)  # ✅ Unique
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        """Show teacher photo preview in admin panel"""
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'


class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ✅ Unique
    email = models.EmailField(unique=True)  # ✅ Unique
    phone = models.CharField(max_length=20)
    address = models.TextField()
    course = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=20, unique=True)  # ✅ Unique
    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    parent_fullname = models.CharField(max_length=100)
    guardian_teacher = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        """Show student photo preview in admin panel"""
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'


class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # ✅ Unique
    phone = models.CharField(max_length=20)
    address = models.TextField()
    aadhaar = models.CharField(max_length=20, unique=True)  # ✅ Unique
    relation = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')  # ✅ FIXED
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='parents/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relation})"  # ✅ Better display in admin

    def image_tag(self):
        """Show parent photo preview in admin panel"""
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'
