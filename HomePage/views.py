import base64
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from .models import Teacher, Student, Parent
def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")  # "teacher" / "student" / "parent"
        captured_image = request.POST.get("captured_image")

        if user_type == "teacher":
            teacher = Teacher(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                address=request.POST.get("address"),
                department=request.POST.get("department"),
                subject=request.POST.get("subject"),
                employee_id=request.POST.get("employee_id"),
                password=request.POST.get("password"),
            )

            if captured_image:
                format, imgstr = captured_image.split(';base64,')
                ext = format.split('/')[-1]
                teacher.photo.save(f"{teacher.name}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

            teacher.save()

        elif user_type == "student":
            student = Student(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                address=request.POST.get("address"),
                course=request.POST.get("course"),
                roll_number=request.POST.get("roll_number"),
                branch=request.POST.get("branch"),
                year=request.POST.get("year"),
                parent_fullname=request.POST.get("parent_fullname"),
                guardian_teacher=request.POST.get("guardian_teacher"),
                password=request.POST.get("password"),
            )

            if captured_image:
                format, imgstr = captured_image.split(';base64,')
                ext = format.split('/')[-1]
                student.photo.save(f"{student.name}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

            student.save()

        elif user_type == "parent":
            parent = Parent(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                address=request.POST.get("address"),
                aadhaar=request.POST.get("aadhaar"),
                relation=request.POST.get("relation"),
                student_id=request.POST.get("student_id"),  # FK
                password=request.POST.get("password"),
            )

            if captured_image:
                format, imgstr = captured_image.split(';base64,')
                ext = format.split('/')[-1]
                parent.photo.save(f"{parent.name}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

            parent.save()

        return redirect('home')  # ✅ Redirect after registration success

    # GET request – render registration form
    return render(request, "register.html", {
        "teachers": Teacher.objects.all(),  # for guardian_teacher dropdown
        "students": Student.objects.all()   # for parent → student dropdown
    })


def register_success(request):
    return render(request, "register_success.html")