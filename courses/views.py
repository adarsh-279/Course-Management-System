from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Course, Enrollment
from .forms import RegisterForm


def home(request):
    return render(request, 'home.html')


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        courses = Course.objects.all()
        enrollments = Enrollment.objects.count()
        return render(request, 'admin_dashboard.html', {
            'courses': courses,
            'enrollments': enrollments
        })
    else:
        enrollments = Enrollment.objects.filter(student=request.user)
        return render(request, 'student_dashboard.html', {
            'enrollments': enrollments
        })


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