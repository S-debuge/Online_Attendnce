import base64
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from .models import (
    Student, Teacher, Parent,
    MechanicalFirstYearStudent, MechanicalSecondYearStudent,
    MechanicalThirdYearStudent, MechanicalFourthYearStudent,
    ElectricalFirstYearStudent, ElectricalSecondYearStudent,
    ElectricalThirdYearStudent, ElectricalFourthYearStudent,
    Subject, Attendance
)

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
                guardian_teacher = request.POST.get('guardian_teacher')
                password = request.POST.get('password')
                gender = request.POST.get('gender')
                age = request.POST.get('age')
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, roll_number, course, branch, year,
                            parent_fullname, guardian_teacher, password, gender, age, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields, select gender and age, and capture a photo for Student Registration.")
                    return redirect('register')

                try:
                    student = Student(
                        name=name, email=email, phone=phone, address=address,
                        roll_number=roll_number, course=course, branch=branch,
                        year=year, parent_fullname=parent_fullname,
                        guardian_teacher=guardian_teacher, password=password,
                        gender=gender, age=age
                    )

                    if photo_data.startswith("data:image"):
                        format, imgstr = photo_data.split(';base64,')
                        ext = format.split('/')[-1]
                        student.photo.save(f"{roll_number}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

                    student.save()  # ✅ Triggers post_save signals if you use them

                    # ---------------- Branch-Year info ----------------
                    course_upper = course.strip().upper()
                    branch_lower = branch.strip().lower()
                    year_lower = year.strip().lower()

                    if course_upper == "BE":
                        if branch_lower == "mechanical":
                            if year_lower == "first year":
                                MechanicalFirstYearStudent.objects.get_or_create(student=student)
                            elif year_lower == "second year":
                                MechanicalSecondYearStudent.objects.get_or_create(student=student)
                            elif year_lower == "third year":
                                MechanicalThirdYearStudent.objects.get_or_create(student=student)
                            elif year_lower == "fourth year":
                                MechanicalFourthYearStudent.objects.get_or_create(student=student)
                        elif branch_lower == "electrical":
                            if year_lower == "first year":
                                ElectricalFirstYearStudent.objects.get_or_create(student=student)
                            elif year_lower == "second year":
                                ElectricalSecondYearStudent.objects.get_or_create(student=student)
                            elif year_lower == "third year":
                                ElectricalThirdYearStudent.objects.get_or_create(student=student)
                            elif year_lower == "fourth year":
                                ElectricalFourthYearStudent.objects.get_or_create(student=student)

                    # ---------------- AUTO CREATE ATTENDANCE ----------------
                    subjects = Subject.objects.filter(branch=branch, year=year)
                    for subject in subjects:
                        # Create initial attendance record for today with default "Absent"
                        Attendance.objects.get_or_create(student=student, subject=subject, date=date.today(), defaults={"status": "Absent"})

                    messages.success(request, "✅ Student Registered Successfully!")
                    return redirect('register_success')

                except IntegrityError:
                    messages.error(request, "❌ Duplicate Entry: Make sure Email, Name, and Roll Number are unique.")
                    return redirect('register')

            # ------------------ TEACHER FORM ------------------
            elif form_type == "teacher":
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                department = request.POST.get('department')
                subject = request.POST.get('subject')
                employee_id = request.POST.get('employee_id')
                password = request.POST.get('password')
                gender = request.POST.get('gender')
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, department, subject, employee_id, password, gender, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields, select gender, and capture a photo for Teacher Registration.")
                    return redirect('register')

                try:
                    teacher = Teacher(
                        name=name, email=email, phone=phone, address=address,
                        department=department, subject=subject,
                        employee_id=employee_id, password=password,
                        gender=gender
                    )

                    if photo_data.startswith("data:image"):
                        format, imgstr = photo_data.split(';base64,')
                        ext = format.split('/')[-1]
                        teacher.photo.save(f"{employee_id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

                    teacher.save()
                    messages.success(request, "✅ Teacher Registered Successfully!")
                    return redirect('register_success')

                except IntegrityError:
                    messages.error(request, "❌ Duplicate Entry: Make sure Email, Name, and Employee ID are unique.")
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
                    messages.error(request, "⚠️ Please fill all fields, select gender, and capture a photo for Parent Registration.")
                    return redirect('register')

                try:
                    parent = Parent(
                        name=name, email=email, phone=phone, address=address,
                        aadhaar=aadhaar, relation=relation,
                        student_id=student_id, password=password,
                        gender=gender
                    )

                    if photo_data.startswith("data:image"):
                        format, imgstr = photo_data.split(';base64,')
                        ext = format.split('/')[-1]
                        parent.photo.save(f"{aadhaar}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

                    parent.save()
                    messages.success(request, "✅ Parent Registered Successfully!")
                    return redirect('register_success')

                except IntegrityError:
                    messages.error(request, "❌ Duplicate Entry: Make sure Email and Aadhaar are unique.")
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

def register_success(request):
    return render(request, "register_success.html")

# ----------------------- LOGIN VIEW -----------------------
def login_view(request):
    if request.method == 'POST':
        user_type = None
        user = None

        if 'student_id' in request.POST:
            user_type = 'student'
            identifier = request.POST['student_id']
            password = request.POST['password']
            try:
                user = Student.objects.get(email=identifier)
            except Student.DoesNotExist:
                try:
                    user = Student.objects.get(roll_number=identifier)
                except Student.DoesNotExist:
                    user = None

        elif 'teacher_id' in request.POST:
            user_type = 'teacher'
            identifier = request.POST['teacher_id']
            password = request.POST['password']
            try:
                user = Teacher.objects.get(email=identifier)
            except Teacher.DoesNotExist:
                try:
                    user = Teacher.objects.get(employee_id=identifier)
                except Teacher.DoesNotExist:
                    user = None

        elif 'parent_id' in request.POST:
            user_type = 'parent'
            identifier = request.POST['parent_id']
            password = request.POST['password']
            try:
                user = Parent.objects.get(email=identifier)
            except Parent.DoesNotExist:
                user = None

        if user:
            if user.password == password:
                request.session['user_type'] = user_type
                request.session['user_id'] = user.id

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
    request.session.flush()  # Clear all session data
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # redirect to login page

# ----------------------- DASHBOARDS -----------------------
def student_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = Student.objects.get(id=user_id)
    attendance_records = Attendance.objects.filter(student=user).order_by('-date')
    return render(request, 'student_dashboard.html', {'user': user, 'attendance_records': attendance_records})

def teacher_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = Teacher.objects.get(id=user_id)
    return render(request, 'teacher_dashboard.html', {'user': user})

def parent_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = Parent.objects.get(id=user_id)
    return render(request, 'parent_dashboard.html', {'user': user})
