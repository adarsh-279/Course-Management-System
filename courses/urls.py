from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),

    # Auth
    path('login/', views.login_view, name='login'),    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),

    # Pages
    path('courses/', views.course_list, name='courses'),
    path('courses/create/', views.create_course, name='course_create'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('leave-course/<int:course_id>/', views.leave_course, name='leave_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='course_delete'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('enrollments/', views.enrollment_list, name='enrollments'),
    path('users/', views.user_list, name='users'),

    # AJAX modal endpoints
    path('api/courses/<int:course_id>/', views.course_detail_json, name='course_detail_api'),
    path('api/courses/<int:course_id>/update/', views.course_update, name='course_update_api'),
    path('api/courses/<int:course_id>/delete/', views.course_delete, name='course_delete_api'),

    path('api/students/<int:user_id>/', views.student_detail_json, name='student_detail_api'),
    path('api/students/<int:user_id>/update/', views.student_update, name='student_update_api'),
    path('api/students/<int:user_id>/delete/', views.student_delete, name='student_delete_api'),
    path('api/students/create/', views.student_create, name='student_create_api'),

    path('api/enrollments/<int:enrollment_id>/', views.enrollment_detail_json, name='enrollment_detail_api'),
    path('api/enrollments/<int:enrollment_id>/delete/', views.enrollment_delete, name='enrollment_delete_api'),
]