from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),

    # Pages
    path('courses/', views.course_list, name='courses'),
    path('courses/create/', views.create_course, name='course_create'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='course_delete'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('enrollments/', views.enrollment_list, name='enrollments'),
    path('users/', views.user_list, name='users'),
]