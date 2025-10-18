from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🔹 Home & Auth routes
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('check-unique/', views.check_unique, name='check_unique'),
    path('login/', views.login_view, name='login'),

    # 🔹 Single unified logout for all (students, teachers, parents)
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    # 🔹 Dashboards
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),

    # 🔹 Attendance & Face Recognition
    path('teacher/attendance/submit/', views.submit_attendance_ajax, name='submit_attendance_ajax'),
    path('teacher/get_student_faces/', views.get_student_faces, name='get_student_faces'),
    path('auto_mark_attendance/', views.auto_mark_attendance, name='auto_mark_attendance'),
]
