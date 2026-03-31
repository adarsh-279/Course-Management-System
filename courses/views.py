from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Course, Enrollment
from .forms import RegisterForm
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
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'student_dashboard.html')


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


@login_required
def enroll(request, course_id):
    course = Course.objects.get(id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('my_courses')


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {
        'enrollments': enrollments
    })