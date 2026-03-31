from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Course, Enrollment
from .forms import RegisterForm, CourseForm
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            role = form.cleaned_data['role']

            if role == 'admin':
                user.is_staff = True   # 🔥 makes user admin
                user.is_superuser = False
            else:
                user.is_staff = False

            user.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_staff:
        courses = Course.objects.all()
        students_count = User.objects.filter(is_staff=False).count()
        return render(request, 'admin_dashboard.html', {
                'courses': courses,
                'students': students_count
        })
    else:
        enrollments = Enrollment.objects.filter(student=request.user)
        return render(request, 'student_dashboard.html', {
            'enrollments': enrollments
        })


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {
        'courses': courses,
        'is_admin': request.user.is_staff,
    })


@login_required
def create_course(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
    else:
        form = CourseForm()

    return render(request, 'course_create.html', {'form': form})


@login_required
def delete_course(request, course_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('courses')


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('my_courses')


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {
        'enrollments': enrollments
    })