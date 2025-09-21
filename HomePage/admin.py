from django.contrib import admin
from .models import (
    Teacher, Student, Parent,
    MechanicalFirstYearStudent, MechanicalSecondYearStudent,
    MechanicalThirdYearStudent, MechanicalFourthYearStudent,
    ElectricalFirstYearStudent, ElectricalSecondYearStudent,
    ElectricalThirdYearStudent, ElectricalFourthYearStudent,
    Subject, Attendance
)

# -----------------------
# ✅ TEACHER ADMIN
# -----------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "gender", "department", "subject", "employee_id", "image_tag")
    search_fields = ("name", "email", "employee_id")
    list_filter = ("department", "subject", "gender")
    readonly_fields = ("image_tag",)

# -----------------------
# ✅ STUDENT ADMIN
# -----------------------
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    readonly_fields = ("subject", "date", "status")
    can_delete = False
    show_change_link = True

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "gender", "age", "course", "roll_number", "branch", "year", "image_tag")
    search_fields = ("name", "email", "roll_number")
    list_filter = ("branch", "year", "gender")
    readonly_fields = ("image_tag",)
    inlines = [AttendanceInline]  # ✅ Show attendance in student page

# -----------------------
# ✅ PARENT ADMIN
# -----------------------
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "gender", "relation", "student", "aadhaar", "image_tag")
    search_fields = ("name", "email", "aadhaar")
    list_filter = ("relation", "gender")
    readonly_fields = ("image_tag",)
    fields = ("name", "email", "phone", "gender", "address", "aadhaar", "relation", "student", "password", "photo", "image_tag")

# -----------------------
# ✅ UTILITY FUNCTIONS FOR YEARLY ADMINS
# -----------------------
def year_admin_list_display():
    return ("student", "get_gender", "get_age", "get_roll_number", "get_course", "get_branch", "get_year")

def year_admin_fields():
    return ("student",)

def year_admin_methods(cls):
    def get_roll_number(self, obj):
        return obj.student.roll_number
    get_roll_number.short_description = "Roll Number"

    def get_course(self, obj):
        return obj.student.course
    get_course.short_description = "Course"

    def get_branch(self, obj):
        return obj.student.branch
    get_branch.short_description = "Branch"

    def get_year(self, obj):
        return obj.student.year
    get_year.short_description = "Year"

    def get_gender(self, obj):
        return obj.student.gender
    get_gender.short_description = "Gender"

    def get_age(self, obj):
        return obj.student.age
    get_age.short_description = "Age"

    cls.get_roll_number = get_roll_number
    cls.get_course = get_course
    cls.get_branch = get_branch
    cls.get_year = get_year
    cls.get_gender = get_gender
    cls.get_age = get_age
    return cls

# -----------------------
# ✅ MECHANICAL YEARLY ADMINS
# -----------------------
@admin.register(MechanicalFirstYearStudent)
class MechanicalFirstYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

@admin.register(MechanicalSecondYearStudent)
class MechanicalSecondYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

@admin.register(MechanicalThirdYearStudent)
class MechanicalThirdYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

@admin.register(MechanicalFourthYearStudent)
class MechanicalFourthYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

# -----------------------
# ✅ ELECTRICAL YEARLY ADMINS
# -----------------------
@admin.register(ElectricalFirstYearStudent)
class ElectricalFirstYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

@admin.register(ElectricalSecondYearStudent)
class ElectricalSecondYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

@admin.register(ElectricalThirdYearStudent)
class ElectricalThirdYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

@admin.register(ElectricalFourthYearStudent)
class ElectricalFourthYearStudentAdmin(admin.ModelAdmin):
    list_display = year_admin_list_display()
    search_fields = ("student__roll_number", "student__name", "student__email")
    list_filter = ("student__branch", "student__year", "student__gender")
    fields = year_admin_fields()

# -----------------------
# ✅ ATTENDANCE & SUBJECT ADMIN
# -----------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "branch", "year")
    search_fields = ("name", "branch", "year")
    list_filter = ("branch", "year")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "get_roll_number", "subject", "date", "status", "get_class_type")
    search_fields = ("student__name", "student__roll_number", "subject__name")
    list_filter = ("subject__branch", "subject__year", "date", "status")
    date_hierarchy = "date"

    def get_roll_number(self, obj):
        return obj.student.roll_number
    get_roll_number.short_description = "Roll Number"

    def get_class_type(self, obj):
        return f"{obj.student.branch} {obj.student.year}"
    get_class_type.short_description = "Class"

# -----------------------
# Apply year methods to all yearly admins
# -----------------------
for admin_cls in [
    MechanicalFirstYearStudentAdmin, MechanicalSecondYearStudentAdmin,
    MechanicalThirdYearStudentAdmin, MechanicalFourthYearStudentAdmin,
    ElectricalFirstYearStudentAdmin, ElectricalSecondYearStudentAdmin,
    ElectricalThirdYearStudentAdmin, ElectricalFourthYearStudentAdmin
]:
    year_admin_methods(admin_cls)
