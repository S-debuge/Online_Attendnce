from django.db import models
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# -----------------------
# ✅ DEPARTMENT MODEL
# -----------------------
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -----------------------
# ✅ TEACHER MODEL
# -----------------------
class Teacher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    department = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    year = models.CharField(max_length=20, default="1")  # Added year for Teacher-Year mapping
    employee_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    gender_choices = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    gender = models.CharField(max_length=10, choices=gender_choices, default='Male')

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'


# -----------------------
# ✅ STUDENT MODEL
# -----------------------
class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    course = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    parent_fullname = models.CharField(max_length=100)
    guardian_teacher = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    gender_choices = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    gender = models.CharField(max_length=10, choices=gender_choices, default='Male')
    age = models.PositiveIntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'


# -----------------------
# ✅ PARENT MODEL
# -----------------------
class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    aadhaar = models.CharField(max_length=20, unique=True)
    relation = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='parents/', blank=True, null=True)
    gender_choices = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    gender = models.CharField(max_length=10, choices=gender_choices, default='Male')

    def __str__(self):
        return f"{self.name} ({self.relation})"

    def image_tag(self):
        if self.photo:
            return format_html('<img src="{}" style="width:100px; border-radius:10px;" />', self.photo.url)
        return "-"
    image_tag.short_description = 'Photo'


# -----------------------
# ✅ BRANCH-YEAR STUDENTS
# -----------------------
class MechanicalFirstYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Mechanical First Year Student"
        verbose_name_plural = "Mechanical First Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"

class MechanicalSecondYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Mechanical Second Year Student"
        verbose_name_plural = "Mechanical Second Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"

class MechanicalThirdYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Mechanical Third Year Student"
        verbose_name_plural = "Mechanical Third Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"

class MechanicalFourthYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Mechanical Fourth Year Student"
        verbose_name_plural = "Mechanical Fourth Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"

class ElectricalFirstYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Electrical First Year Student"
        verbose_name_plural = "Electrical First Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"

class ElectricalSecondYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Electrical Second Year Student"
        verbose_name_plural = "Electrical Second Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"

class ElectricalThirdYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Electrical Third Year Student"
        verbose_name_plural = "Electrical Third Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"

class ElectricalFourthYearStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Electrical Fourth Year Student"
        verbose_name_plural = "Electrical Fourth Year Students"
    def __str__(self):
        return f"{self.student.name} ({self.student.roll_number})"


# -----------------------
# ✅ SUBJECT MODEL
# -----------------------
class Subject(models.Model):
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.branch} {self.year})"


# -----------------------
# ✅ ATTENDANCE MODEL
# -----------------------
class Attendance(models.Model):
    STATUS_CHOICES = (('Present', 'Present'), ('Absent', 'Absent'))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.date} - {self.status}"


# -----------------------
# ✅ SIGNAL TO CREATE BRANCH-YEAR RECORDS & ATTENDANCE
# -----------------------
@receiver(post_save, sender=Student)
def save_branch_year_student(sender, instance, created, **kwargs):
    if not created:
        return

    course = instance.course.strip().upper()
    branch = instance.branch.strip().lower()
    year = instance.year.strip().lower()

    # Branch-Year Mapping for Students
    if course == "BE":
        if branch == "mechanical":
            if year == "first year":
                MechanicalFirstYearStudent.objects.get_or_create(student=instance)
            elif year == "second year":
                MechanicalSecondYearStudent.objects.get_or_create(student=instance)
            elif year == "third year":
                MechanicalThirdYearStudent.objects.get_or_create(student=instance)
            elif year == "fourth year":
                MechanicalFourthYearStudent.objects.get_or_create(student=instance)
        elif branch == "electrical":
            if year == "first year":
                ElectricalFirstYearStudent.objects.get_or_create(student=instance)
            elif year == "second year":
                ElectricalSecondYearStudent.objects.get_or_create(student=instance)
            elif year == "third year":
                ElectricalThirdYearStudent.objects.get_or_create(student=instance)
            elif year == "fourth year":
                ElectricalFourthYearStudent.objects.get_or_create(student=instance)

    # Auto-create attendance for all subjects
    subjects = Subject.objects.filter(branch=instance.branch, year=instance.year)
    for subject in subjects:
        Attendance.objects.get_or_create(student=instance, subject=subject, date=date.today())


# -----------------------
# ✅ TEACHER-YEAR MODELS
# -----------------------
class MechanicalFirstYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"

class MechanicalSecondYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"

class MechanicalThirdYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"

class MechanicalFourthYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"

class ElectricalFirstYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"

class ElectricalSecondYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"

class ElectricalThirdYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"

class ElectricalFourthYearTeacher(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.department} - {self.teacher.year})"


# -----------------------
# ✅ SIGNAL TO AUTO CREATE TEACHER-YEAR RECORD
# -----------------------
@receiver(post_save, sender=Teacher)
def save_teacher_year(sender, instance, created, **kwargs):
    if not created:
        return

    dept = instance.department.strip().lower()
    year = instance.year.strip().lower()

    if dept == "mechanical":
        if year == "1st year":
            MechanicalFirstYearTeacher.objects.get_or_create(teacher=instance)
        elif year == "2nd year":
            MechanicalSecondYearTeacher.objects.get_or_create(teacher=instance)
        elif year == "3rd year":
            MechanicalThirdYearTeacher.objects.get_or_create(teacher=instance)
        elif year == "4th year":
            MechanicalFourthYearTeacher.objects.get_or_create(teacher=instance)
    elif dept == "electrical":
        if year == "1st year":
            ElectricalFirstYearTeacher.objects.get_or_create(teacher=instance)
        elif year == "2nd year":
            ElectricalSecondYearTeacher.objects.get_or_create(teacher=instance)
        elif year == "3rd year":
            ElectricalThirdYearTeacher.objects.get_or_create(teacher=instance)
        elif year == "4th year":
            ElectricalFourthYearTeacher.objects.get_or_create(teacher=instance)
