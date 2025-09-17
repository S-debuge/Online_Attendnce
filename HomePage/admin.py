from django.contrib import admin
from django.utils.html import format_html
from .models import Teacher, Student, Parent

# ✅ Show image preview in admin
class PhotoPreviewMixin:
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="80" style="border-radius:8px;">', obj.photo.url)
        return "No Image"
    photo_preview.short_description = "Photo"

# ✅ Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin, PhotoPreviewMixin):
    list_display = ("name", "email", "phone", "department", "photo_preview")
    search_fields = ("name", "email", "phone", "department")
    fields = ("name", "email", "phone", "address", "department", "subject", "employee_id", "password", "photo")

# ✅ Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin, PhotoPreviewMixin):
    list_display = ("name", "email", "phone", "roll_number", "branch", "photo_preview")
    search_fields = ("name", "email", "phone", "roll_number")
    fields = ("name", "email", "phone", "address", "course", "roll_number", "branch", "year",
              "parent_fullname", "guardian_teacher", "password", "photo")

# ✅ Parent Admin
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin, PhotoPreviewMixin):
    list_display = ("name", "email", "phone", "relation", "photo_preview")
    search_fields = ("name", "email", "phone", "relation")
    fields = ("name", "email", "phone", "address", "aadhaar", "relation", "student_id", "password", "photo")
