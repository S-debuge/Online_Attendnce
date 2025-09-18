from django.contrib import admin
from .models import Teacher, Student, Parent


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "department", "subject", "employee_id", "image_tag")
    search_fields = ("name", "email", "employee_id")
    list_filter = ("department", "subject")
    readonly_fields = ("image_tag",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "course", "roll_number", "branch", "year", "image_tag")
    search_fields = ("name", "email", "roll_number")
    list_filter = ("branch", "year")
    readonly_fields = ("image_tag",)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "relation", "student", "aadhaar", "image_tag")
    search_fields = ("name", "email", "aadhaar")
    list_filter = ("relation",)
    readonly_fields = ("image_tag",)

    # ✅ Use student dropdown properly
    fields = ("name", "email", "phone", "address", "aadhaar", "relation", "student", "password", "photo", "image_tag")
