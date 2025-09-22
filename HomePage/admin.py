from django.contrib import admin
from .models import (
    Teacher, Student, Parent,
    MechanicalFirstYearStudent, MechanicalSecondYearStudent,
    MechanicalThirdYearStudent, MechanicalFourthYearStudent,
    ElectricalFirstYearStudent, ElectricalSecondYearStudent,
    ElectricalThirdYearStudent, ElectricalFourthYearStudent,
    MechanicalFirstYearTeacher, MechanicalSecondYearTeacher,
    MechanicalThirdYearTeacher, MechanicalFourthYearTeacher,
    ElectricalFirstYearTeacher, ElectricalSecondYearTeacher,
    ElectricalThirdYearTeacher, ElectricalFourthYearTeacher,
    Subject, Attendance, Department
)

# -----------------------
# ✅ TEACHER ADMIN
# -----------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "gender", "department", "year", "subject", "employee_id", "photo")
    search_fields = ("name", "email", "employee_id")
    list_filter = ("department", "year", "subject", "gender")
    readonly_fields = ("photo",)


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
    list_display = ("name", "email", "phone", "gender", "age", "dob", "course", "roll_number", "branch", "year", "photo")
    search_fields = ("name", "email", "roll_number")
    list_filter = ("branch", "year", "gender")
    readonly_fields = ("photo",)
    inlines = [AttendanceInline]


# -----------------------
# ✅ PARENT ADMIN
# -----------------------
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "gender", "relation", "student", "aadhaar", "photo")
    search_fields = ("name", "email", "aadhaar")
    list_filter = ("relation", "gender")
    readonly_fields = ("photo",)
    fields = ("name", "email", "phone", "gender", "address", "aadhaar", "relation", "student", "password", "photo")


# -----------------------
# ✅ UTILITY FUNCTIONS FOR YEARLY STUDENTS
# -----------------------
def year_admin_list_display():
    return ("student", "get_gender", "get_age", "get_dob", "get_roll_number", "get_course", "get_branch", "get_year")


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

    def get_dob(self, obj):
        return obj.student.dob
    get_dob.short_description = "DOB"

    cls.get_roll_number = get_roll_number
    cls.get_course = get_course
    cls.get_branch = get_branch
    cls.get_year = get_year
    cls.get_gender = get_gender
    cls.get_age = get_age
    cls.get_dob = get_dob
    return cls


# -----------------------
# ✅ YEARLY STUDENT ADMINS
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
# ✅ UTILITY FUNCTION FOR YEARLY TEACHERS
# -----------------------
def add_teacher_methods(cls):
    def get_department(self, obj):
        return obj.teacher.department
    get_department.short_description = "Department"

    def get_year(self, obj):
        return obj.teacher.year
    get_year.short_description = "Year"

    def get_email(self, obj):
        return obj.teacher.email
    get_email.short_description = "Email"

    def get_phone(self, obj):
        return obj.teacher.phone
    get_phone.short_description = "Phone"

    def get_employee_id(self, obj):
        return obj.teacher.employee_id
    get_employee_id.short_description = "Employee ID"

    cls.get_department = get_department
    cls.get_year = get_year
    cls.get_email = get_email
    cls.get_phone = get_phone
    cls.get_employee_id = get_employee_id

    cls.list_display = ('teacher', 'get_department', 'get_year', 'get_email', 'get_phone', 'get_employee_id')
    cls.search_fields = ("teacher__name", "teacher__email", "teacher__employee_id")
    cls.list_filter = ("teacher__department", "teacher__year")
    return cls


# -----------------------
# ✅ YEARLY TEACHER ADMINS
# -----------------------
@admin.register(MechanicalFirstYearTeacher)
class MechanicalFirstYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(MechanicalFirstYearTeacherAdmin)

@admin.register(MechanicalSecondYearTeacher)
class MechanicalSecondYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(MechanicalSecondYearTeacherAdmin)

@admin.register(MechanicalThirdYearTeacher)
class MechanicalThirdYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(MechanicalThirdYearTeacherAdmin)

@admin.register(MechanicalFourthYearTeacher)
class MechanicalFourthYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(MechanicalFourthYearTeacherAdmin)

@admin.register(ElectricalFirstYearTeacher)
class ElectricalFirstYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(ElectricalFirstYearTeacherAdmin)

@admin.register(ElectricalSecondYearTeacher)
class ElectricalSecondYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(ElectricalSecondYearTeacherAdmin)

@admin.register(ElectricalThirdYearTeacher)
class ElectricalThirdYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(ElectricalThirdYearTeacherAdmin)

@admin.register(ElectricalFourthYearTeacher)
class ElectricalFourthYearTeacherAdmin(admin.ModelAdmin):
    pass
add_teacher_methods(ElectricalFourthYearTeacherAdmin)


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
    list_display = ('student', 'branch', 'student_class', 'subject', 'date', 'status')
    list_filter = ('date', 'subject', 'student__branch', 'student__year', 'status')
    search_fields = ('student__name', 'subject__name', 'student__roll_number')
    date_hierarchy = 'date'
    
    def get_roll_number(self, obj):
        return obj.student.roll_number
    get_roll_number.short_description = "Roll Number"

    def get_class_type(self, obj):
        return f"{obj.student.branch} {obj.student.year}"
    get_class_type.short_description = "Class"


# -----------------------
# Apply year methods to all yearly student admins
# -----------------------
for admin_cls in [
    MechanicalFirstYearStudentAdmin, MechanicalSecondYearStudentAdmin,
    MechanicalThirdYearStudentAdmin, MechanicalFourthYearStudentAdmin,
    ElectricalFirstYearStudentAdmin, ElectricalSecondYearStudentAdmin,
    ElectricalThirdYearStudentAdmin, ElectricalFourthYearStudentAdmin
]:
    year_admin_methods(admin_cls)


# -----------------------
# ✅ REGISTER DEPARTMENT
# -----------------------
admin.site.register(Department)
