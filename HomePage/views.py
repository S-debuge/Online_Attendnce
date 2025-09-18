import base64
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .models import Teacher, Student, Parent
def home(request):
    return render(request, "home.html")

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
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, roll_number, course, branch, year, parent_fullname, guardian_teacher, password, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields and capture a photo for Student Registration.")
                    return redirect('register')

                student = Student(
                    name=name, email=email, phone=phone, address=address,
                    roll_number=roll_number, course=course, branch=branch,
                    year=year, parent_fullname=parent_fullname,
                    guardian_teacher=guardian_teacher, password=password
                )

                if photo_data.startswith("data:image"):
                    format, imgstr = photo_data.split(';base64,')
                    ext = format.split('/')[-1]
                    student.photo.save(f"{roll_number}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

                student.save()
                messages.success(request, "✅ Student Registered Successfully!")
                return redirect('register_success')

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
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, department, subject, employee_id, password, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields and capture a photo for Teacher Registration.")
                    return redirect('register')

                teacher = Teacher(
                    name=name, email=email, phone=phone, address=address,
                    department=department, subject=subject, employee_id=employee_id, password=password
                )

                if photo_data.startswith("data:image"):
                    format, imgstr = photo_data.split(';base64,')
                    ext = format.split('/')[-1]
                    teacher.photo.save(f"{employee_id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

                teacher.save()
                messages.success(request, "✅ Teacher Registered Successfully!")
                return redirect('register_success')

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
                photo_data = request.POST.get('photo_data')

                if not all([name, email, phone, address, aadhaar, relation, student_id, password, photo_data]):
                    messages.error(request, "⚠️ Please fill all fields and capture a photo for Parent Registration.")
                    return redirect('register')

                parent = Parent(
                    name=name, email=email, phone=phone, address=address,
                    aadhaar=aadhaar, relation=relation, student_id=student_id, password=password
                )

                if photo_data.startswith("data:image"):
                    format, imgstr = photo_data.split(';base64,')
                    ext = format.split('/')[-1]
                    parent.photo.save(f"{aadhaar}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

                parent.save()
                messages.success(request, "✅ Parent Registered Successfully!")
                return redirect('register_success')

        except Exception as e:
            messages.error(request, f"❌ Error: {e}")
            return redirect('register')

    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'register.html', {'teachers': teachers, 'students': students})
    
# views.py
from django.http import JsonResponse
from .models import Teacher, Student, Parent

def check_unique(request):
    field_type = request.GET.get("type")
    value = request.GET.get("value")
    exists = False

    if field_type == "teacher_email":
        exists = Teacher.objects.filter(email=value).exists()
    elif field_type == "employee_id":
        exists = Teacher.objects.filter(employee_id=value).exists()
    elif field_type == "student_email":
        exists = Student.objects.filter(email=value).exists()
    elif field_type == "roll_number":
        exists = Student.objects.filter(roll_number=value).exists()
    elif field_type == "parent_email":
        exists = Parent.objects.filter(email=value).exists()
    elif field_type == "aadhaar":
        exists = Parent.objects.filter(aadhaar=value).exists()

    return JsonResponse({"exists": exists})


def register_success(request):
    return render(request, "register_success.html")





from django.contrib import messages
from .models import Student, Teacher, Parent

def login_view(request):
    if request.method == 'POST':
        user_type = None
        user = None

        # Detect which form is submitted
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

        # Authenticate
        if user:
            if user.password == password:
                # Store user info in session
                request.session['user_type'] = user_type
                request.session['user_id'] = user.id

                # Redirect to separate dashboards
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

    return render(request, 'home.html')  # your login page template



#dashboard views
def student_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = Student.objects.get(id=user_id)
    return render(request, 'student_dashboard.html', {'user': user})

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


#user login code

def user_login(request):
    if request.method == "POST":
        # Determine which form submitted
        student_id = request.POST.get('student_id')
        teacher_id = request.POST.get('teacher_id')
        parent_id = request.POST.get('parent_id')
        password = request.POST.get('password')

        # Student login
        if student_id:
            try:
                student = Student.objects.get(email=student_id)  # or use roll_number
                if student.password == password:
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "Invalid Student ID or password.")
            except Student.DoesNotExist:
                messages.error(request, "Student not found.")

        # Teacher login
        elif teacher_id:
            try:
                teacher = Teacher.objects.get(email=teacher_id)  # or use employee_id
                if teacher.password == password:
                    return redirect('teacher_dashboard')
                else:
                    messages.error(request, "Invalid Teacher ID or password.")
            except Teacher.DoesNotExist:
                messages.error(request, "Teacher not found.")

        # Parent login
        elif parent_id:
            try:
                parent = Parent.objects.get(email=parent_id)  # or use student relation
                if parent.password == password:
                    return redirect('parent_dashboard')
                else:
                    messages.error(request, "Invalid Parent ID or password.")
            except Parent.DoesNotExist:
                messages.error(request, "Parent not found.")

    return redirect('home')

def student_dashboard(request):
    return render(request, "student_dashboard.html")

def teacher_dashboard(request):
    return render(request, "teacher_dashboard.html")

def parent_dashboard(request):
    return render(request, "parent_dashboard.html")