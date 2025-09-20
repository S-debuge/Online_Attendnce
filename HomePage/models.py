from django.db import models
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver


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
# ✅ MECHANICAL BRANCH-YEAR MODELS
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


# -----------------------
# ✅ ELECTRICAL BRANCH-YEAR MODELS
# -----------------------
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
# ✅ AUTO CREATE BRANCH-YEAR STUDENTS
# -----------------------
@receiver(post_save, sender=Student)
def save_branch_year_student(sender, instance, created, **kwargs):
    if not created:
        return

    course = instance.course.strip().upper()
    branch = instance.branch.strip().lower()
    year = instance.year.strip().lower()

    if course == "BE":
        # Mechanical branch
        if branch == "mechanical":
            if year == "first year":
                MechanicalFirstYearStudent.objects.get_or_create(student=instance)
            elif year == "second year":
                MechanicalSecondYearStudent.objects.get_or_create(student=instance)
            elif year == "third year":
                MechanicalThirdYearStudent.objects.get_or_create(student=instance)
            elif year == "fourth year":
                MechanicalFourthYearStudent.objects.get_or_create(student=instance)
        # Electrical branch
        elif branch == "electrical":
            if year == "first year":
                ElectricalFirstYearStudent.objects.get_or_create(student=instance)
            elif year == "second year":
                ElectricalSecondYearStudent.objects.get_or_create(student=instance)
            elif year == "third year":
                ElectricalThirdYearStudent.objects.get_or_create(student=instance)
            elif year == "fourth year":
                ElectricalFourthYearStudent.objects.get_or_create(student=instance)
