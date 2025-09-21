import base64
from datetime import date
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse

from .models import (
    Student, Teacher, Parent,
    MechanicalFirstYearStudent, MechanicalSecondYearStudent,
    MechanicalThirdYearStudent, MechanicalFourthYearStudent,
    ElectricalFirstYearStudent, ElectricalSecondYearStudent,
    ElectricalThirdYearStudent, ElectricalFourthYearStudent,
    MechanicalFirstYearTeacher, MechanicalSecondYearTeacher,
    MechanicalThirdYearTeacher, MechanicalFourthYearTeacher,
    ElectricalFirstYearTeacher, ElectricalSecondYearTeacher,
    ElectricalThirdYearTeacher, ElectricalFourthYearTeacher,
    Subject, Attendance
)


# ----------------------- HELPER -----------------------
def calculate_age(dob):
    """Calculate age from date of birth."""
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def save_photo(instance, photo_data, filename_prefix):
    """Save base64 photo to model instance."""
    if photo_data and photo_data.startswith("data:image"):
        format, imgstr = photo_data.split(';base64,')
        ext = format.split('/')[-1]
        instance.photo.save(f"{filename_prefix}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)


# ----------------------- HOME -----------------------
def home(request):
    return render(request, "home.html")


# ----------------------- REGISTER -----------------------
def register(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        try:
            # ------------------ STUDENT FORM ------------------
            if form_type == "student":
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                roll_number = request.POST.get('roll_number')
                course = request.POST.get('course')
                branch = request.POST.get('branch')
                year = request.POST.get('year')
                parent_fullname = request.POST.get('parent_fullname')
                guardian_teacher_name = request.POST.get('guardian_teacher')
                password = request.POST.get('password')
                gender = request.POST.get('gender')
                dob_str = request.POST.get('dob')
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, roll_number, course, branch, year,
                            parent_fullname, guardian_teacher_name, password, gender, dob_str, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields and capture a photo for Student Registration.")
                    return redirect('register')

                dob = date.fromisoformat(dob_str)
                age = calculate_age(dob)

                # Get actual Teacher instance for guardian
                guardian_teacher = Teacher.objects.filter(name=guardian_teacher_name).first()

                student = Student(
                    name=name, email=email, phone=phone, address=address,
                    roll_number=roll_number, course=course, branch=branch,
                    year=year, parent_fullname=parent_fullname,
                    guardian_teacher=guardian_teacher, password=password,
                    gender=gender, age=age, dob=dob
                )

                save_photo(student, photo_data, roll_number)

                try:
                    student.save()

                    # ---------------- Branch-Year info ----------------
                    branch_lower = branch.strip().lower()
                    year_lower = year.strip().lower()

                    # Mechanical Students
                    if branch_lower == "mechanical":
                        if "first" in year_lower:
                            MechanicalFirstYearStudent.objects.get_or_create(student=student)
                        elif "second" in year_lower:
                            MechanicalSecondYearStudent.objects.get_or_create(student=student)
                        elif "third" in year_lower:
                            MechanicalThirdYearStudent.objects.get_or_create(student=student)
                        elif "fourth" in year_lower:
                            MechanicalFourthYearStudent.objects.get_or_create(student=student)
                    # Electrical Students
                    elif branch_lower == "electrical":
                        if "first" in year_lower:
                            ElectricalFirstYearStudent.objects.get_or_create(student=student)
                        elif "second" in year_lower:
                            ElectricalSecondYearStudent.objects.get_or_create(student=student)
                        elif "third" in year_lower:
                            ElectricalThirdYearStudent.objects.get_or_create(student=student)
                        elif "fourth" in year_lower:
                            ElectricalFourthYearStudent.objects.get_or_create(student=student)

                    # ---------------- AUTO CREATE ATTENDANCE ----------------
                    subjects = Subject.objects.filter(branch=branch, year=year)
                    for subject in subjects:
                        Attendance.objects.get_or_create(
                            student=student,
                            subject=subject,
                            date=date.today(),
                            defaults={"status": "Absent"}
                        )

                    messages.success(request, "✅ Student Registered Successfully!")
                    return redirect('register_success')

                except IntegrityError:
                    messages.error(request, "❌ Duplicate Entry: Email, Name, or Roll Number already exists.")
                    return redirect('register')

            # ------------------ TEACHER FORM ------------------
            elif form_type == "teacher":
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                department = request.POST.get('department')
                year = request.POST.get('year')
                subject = request.POST.get('subject')
                employee_id = request.POST.get('employee_id')
                password = request.POST.get('password')
                gender = request.POST.get('gender')
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, department, year, subject, employee_id, password, gender, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields and capture a photo for Teacher Registration.")
                    return redirect('register')

                teacher = Teacher(
                    name=name, email=email, phone=phone, address=address,
                    department=department, subject=subject,
                    employee_id=employee_id, password=password,
                    gender=gender, year=year
                )

                save_photo(teacher, photo_data, employee_id)

                try:
                    teacher.save()

                    dept_lower = department.strip().lower()
                    year_lower = year.strip().lower()

                    # Mechanical Teachers
                    if dept_lower == "mechanical":
                        if "first" in year_lower:
                            MechanicalFirstYearTeacher.objects.get_or_create(teacher=teacher)
                        elif "second" in year_lower:
                            MechanicalSecondYearTeacher.objects.get_or_create(teacher=teacher)
                        elif "third" in year_lower:
                            MechanicalThirdYearTeacher.objects.get_or_create(teacher=teacher)
                        elif "fourth" in year_lower:
                            MechanicalFourthYearTeacher.objects.get_or_create(teacher=teacher)
                    # Electrical Teachers
                    elif dept_lower == "electrical":
                        if "first" in year_lower:
                            ElectricalFirstYearTeacher.objects.get_or_create(teacher=teacher)
                        elif "second" in year_lower:
                            ElectricalSecondYearTeacher.objects.get_or_create(teacher=teacher)
                        elif "third" in year_lower:
                            ElectricalThirdYearTeacher.objects.get_or_create(teacher=teacher)
                        elif "fourth" in year_lower:
                            ElectricalFourthYearTeacher.objects.get_or_create(teacher=teacher)

                    messages.success(request, "✅ Teacher Registered Successfully!")
                    return redirect('register_success')

                except IntegrityError:
                    messages.error(request, "❌ Duplicate Entry: Email, Name, or Employee ID already exists.")
                    return redirect('register')

            # ------------------ PARENT FORM ------------------
            elif form_type == "parent":
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                aadhaar = request.POST.get('aadhaar')
                relation = request.POST.get('relation')
                student_id = request.POST.get('student_id')
                password = request.POST.get('password')
                gender = request.POST.get('gender')
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, aadhaar, relation, student_id, password, gender, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields and capture a photo for Parent Registration.")
                    return redirect('register')

                # Link actual Student instance
                student = Student.objects.filter(id=student_id).first()

                parent = Parent(
                    name=name, email=email, phone=phone, address=address,
                    aadhaar=aadhaar, relation=relation,
                    student=student, password=password,
                    gender=gender
                )

                save_photo(parent, photo_data, aadhaar)

                try:
                    parent.save()
                    messages.success(request, "✅ Parent Registered Successfully!")
                    return redirect('register_success')

                except IntegrityError:
                    messages.error(request, "❌ Duplicate Entry: Email or Aadhaar already exists.")
                    return redirect('register')

        except Exception as e:
            messages.error(request, f"❌ Error: {e}")
            return redirect('register')

    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'register.html', {'teachers': teachers, 'students': students})


# ----------------------- AJAX UNIQUE CHECK -----------------------
def check_unique(request):
    field = request.GET.get("field")
    value = request.GET.get("value")
    exists = False

    if field == "student_email":
        exists = Student.objects.filter(email=value).exists()
    elif field == "student_roll_number":
        exists = Student.objects.filter(roll_number=value).exists()
    elif field == "teacher_email":
        exists = Teacher.objects.filter(email=value).exists()
    elif field == "teacher_employee_id":
        exists = Teacher.objects.filter(employee_id=value).exists()
    elif field == "parent_email":
        exists = Parent.objects.filter(email=value).exists()
    elif field == "parent_aadhaar":
        exists = Parent.objects.filter(aadhaar=value).exists()

    return JsonResponse({"exists": exists})


# ----------------------- REGISTER SUCCESS -----------------------
def register_success(request):
    return render(request, "register_success.html")


# ----------------------- LOGIN VIEW -----------------------
def login_view(request):
    if request.method == 'POST':
        user_type = None
        user = None
        identifier = request.POST.get('student_id') or request.POST.get('teacher_id') or request.POST.get('parent_id')
        password = request.POST.get('password')

        if 'student_id' in request.POST:
            user_type = 'student'
            try:
                user = Student.objects.get(email=identifier)
            except Student.DoesNotExist:
                try:
                    user = Student.objects.get(roll_number=identifier)
                except Student.DoesNotExist:
                    user = None

        elif 'teacher_id' in request.POST:
            user_type = 'teacher'
            try:
                user = Teacher.objects.get(email=identifier)
            except Teacher.DoesNotExist:
                try:
                    user = Teacher.objects.get(employee_id=identifier)
                except Teacher.DoesNotExist:
                    user = None

        elif 'parent_id' in request.POST:
            user_type = 'parent'
            try:
                user = Parent.objects.get(email=identifier)
            except Parent.DoesNotExist:
                user = None

        if user:
            if user.password == password:
                request.session['user_type'] = user_type
                request.session['user_id'] = user.id
                request.session['logged_in'] = True

                if user_type == 'student':
                    return redirect('student_dashboard')
                elif user_type == 'teacher':
                    return redirect('teacher_dashboard')
                else:
                    return redirect('parent_dashboard')
            else:
                messages.error(request, 'Incorrect password.')
        else:
            messages.error(request, 'User not found.')

    return render(request, 'home.html')


# ----------------------- LOGOUT -----------------------
def user_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


# ----------------------- DASHBOARDS -----------------------
def student_dashboard(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'student':
        return redirect('login')
    user_id = request.session.get('user_id')
    user = Student.objects.get(id=user_id)
    attendance_records = Attendance.objects.filter(student=user).order_by('-date')
    return render(request, 'student_dashboard.html', {
        'user': user,
        'attendance_records': attendance_records,
        'photo_url': user.photo.url if user.photo else None
    })


def teacher_dashboard(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'teacher':
        return redirect('login')
    user_id = request.session.get('user_id')
    user = Teacher.objects.get(id=user_id)
    return render(request, 'teacher_dashboard.html', {
        'user': user,
        'photo_url': user.photo.url if user.photo else None
    })


def parent_dashboard(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'parent':
        return redirect('login')
    user_id = request.session.get('user_id')
    user = Parent.objects.get(id=user_id)
    return render(request, 'parent_dashboard.html', {
        'user': user,
        'photo_url': user.photo.url if user.photo else None
    })
