from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Course, Enrollment
from .forms import RegisterForm, CourseForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
        enrollments = Enrollment.objects.select_related('student', 'course').order_by('-enrolled_at')
        enrolled_students_count = Enrollment.objects.values('student').distinct().count()
        registered_users = User.objects.filter(is_staff=False)

        return render(request, 'admin_dashboard.html', {
            'courses': courses,
            'enrollments': enrollments,
            'enrolled_students_count': enrolled_students_count,
            'registered_users': registered_users,

            # helper counts for template cards
            'courses_count': courses.count(),
            'enrolled_students_count_value': enrolled_students_count,
            'registered_users_count_value': registered_users.count(),
        })
    else:
        enrollments = Enrollment.objects.filter(student=request.user)
        return render(request, 'student_dashboard.html', {
            'enrollments': enrollments
        })


@login_required
def course_list(request):
    # Student view: prefer BTech-tagged courses, fallback to all
    btech_courses = Course.objects.filter(code__icontains='BTech')
    if not request.user.is_staff and btech_courses.exists():
        courses = btech_courses
        special_note = 'Displaying BTech courses as requested.'
    else:
        courses = Course.objects.all()
        special_note = ''

    enrolled_course_ids = []
    if not request.user.is_staff:
        enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)

    return render(request, 'course_list.html', {
        'courses': courses,
        'is_admin': request.user.is_staff,
        'special_note': special_note,
        'enrolled_course_ids': list(enrolled_course_ids),
    })


from collections import defaultdict

@login_required
def enrollment_list(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    enrollments = Enrollment.objects.select_related('student', 'course')

    course_data = defaultdict(list)

    for e in enrollments:
        course_data[e.course].append(e)

    return render(request, 'enrollments.html', {
        'course_data': dict(course_data)
    })


@login_required
def user_list(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    users = User.objects.filter(is_staff=False).order_by('username')
    return render(request, 'users_list.html', {
        'users': users,
    })


@login_required
def course_detail_json(request, course_id):
    step = request.GET.get('step', 'view')
    course = get_object_or_404(Course, id=course_id)
    data = {
        'id': course.id,
        'name': course.name,
        'code': course.code,
        'description': course.description,
        'capacity': course.capacity,
        'instructor': course.instructor or '',
    }
    return JsonResponse(data)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

@login_required
def leave_course(request, course_id):
    enrollment = Enrollment.objects.filter(
        student=request.user,
        course_id=course_id
    ).first()

    if enrollment:
        enrollment.delete()

    return redirect('my_courses')

import json

@login_required
def course_update(request, course_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')

    course = get_object_or_404(Course, id=course_id)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    form = CourseForm(payload, instance=course)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Course updated'})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
def course_delete(request, course_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')

    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return JsonResponse({'success': True, 'message': 'Course deleted'})


@login_required
def student_detail_json(request, user_id):
    student = get_object_or_404(User, id=user_id, is_staff=False)
    enrolled_courses = list(student.enrollment_set.select_related('course').values('course__id', 'course__name', 'course__code'))
    return JsonResponse({
        'id': student.id,
        'username': student.username,
        'email': student.email,
        'enrolled_courses': enrolled_courses,
    })


@login_required
def student_update(request, user_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')

    student = get_object_or_404(User, id=user_id, is_staff=False)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    student.username = payload.get('username', student.username)
    student.email = payload.get('email', student.email)
    student.save()
    return JsonResponse({'success': True})


@login_required
def student_delete(request, user_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')

    student = get_object_or_404(User, id=user_id, is_staff=False)
    student.delete()
    return JsonResponse({'success': True})


@login_required
def student_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    username = payload.get('username')
    email = payload.get('email')
    password = payload.get('password')

    if not username or not email or not password:
        return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)

    student = User.objects.create_user(username=username, email=email, password=password)
    student.is_staff = False
    student.save()
    return JsonResponse({'success': True, 'id': student.id})


@login_required
def enrollment_detail_json(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    return JsonResponse({
        'id': enrollment.id,
        'student': {
            'id': enrollment.student.id,
            'username': enrollment.student.username,
            'email': enrollment.student.email,
        },
        'course': {
            'id': enrollment.course.id,
            'name': enrollment.course.name,
            'code': enrollment.course.code,
        },
        'enrolled_at': enrollment.enrolled_at.strftime('%Y-%m-%d %H:%M:%S'),
    })


@login_required
def enrollment_delete(request, enrollment_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_staff:
        return HttpResponseBadRequest('Not allowed')

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    enrollment.delete()
    return JsonResponse({'success': True})


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
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect('my_courses')

    Enrollment.objects.create(student=request.user, course=course)
    return redirect('my_courses')


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {
        'enrollments': enrollments
    })

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = None

        # ✅ safer: filter instead of get
        user_obj = User.objects.filter(email=email).first()

        if user_obj:
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

        if user is not None:
            login(request, user)

            # ✅ DEBUG print (check terminal)
            print("LOGIN SUCCESS")

            return redirect('dashboard')   # make sure this exists
        else:
            print("LOGIN FAILED")  # check terminal

            return render(request, 'login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'login.html')