from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path("check-unique/", views.check_unique, name="check_unique"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.user_logout, name='user_logout'),
    path('logout/', views.user_logout, name='logout'), 
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),

    path('teacher/attendance/submit/', views.submit_attendance_ajax, name='submit_attendance_ajax'),
    path('submit_attendance_ajax/', views.submit_attendance_ajax, name='submit_attendance_ajax'),
    path('teacher/get_student_faces/', views.get_student_faces, name='get_student_faces'),
]
