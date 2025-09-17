# HomePage/models.py
from django.db import models
from django.utils.html import format_html


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    department = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    course = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    parent_fullname = models.CharField(max_length=100)
    guardian_teacher = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'


class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    aadhaar = models.CharField(max_length=20)
    relation = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='parents/', blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'
