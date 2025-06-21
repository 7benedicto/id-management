from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from .models import Course, Student, AMISStudent, LossReport
from .forms import StudentForm, ReportLostIDForm, FetchStudentForm
from collections import defaultdict


def index(request):
    return render(request, 'index.html')


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_dup(user):
                return redirect('dup_dashboard')
            elif is_pc_officer(user):
                return redirect('pc_officer_dashboard')
            elif is_management(user):
                return redirect('management_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


# Role check functions
def is_dup(user):
    return user.groups.filter(name='DUP').exists()


def is_pc_officer(user):
    return user.groups.filter(name='PC Officer').exists()


def is_management(user):
    return user.groups.filter(name='Management').exists()


# Role-based views
@login_required
@user_passes_test(is_dup)
def dup_dashboard(request):
    return render(request, 'dup_dashboard.html')


@login_required
@user_passes_test(is_pc_officer)
def pc_officer_dashboard(request):
    return render(request, 'pc_officer_dashboard.html')


@login_required
@user_passes_test(is_management)
def management_dashboard(request):
    return render(request, 'management_dashboard.html')


def upload_students(request):
    courses = Course.objects.all()

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'upload_student.html', {'courses': courses, 'message': 'Student uploaded successfully!'})
        else:
            form = StudentForm()

    return render(request, 'upload_student.html', {'courses': courses})


def verify_students(request):
    # Fetch students who are not yet verified
    unverified_students = Student.objects.filter(is_verified=False)

    if request.method == "POST":
        # Get the student ID from the POST request
        student_id = request.POST.get('student_id')
        try:
            # Fetch the student and mark as verified
            student = Student.objects.get(id=student_id)
            student.is_verified = True
            student.save()
            return redirect('verify_students')
        except Student.DoesNotExist:
            # Handle the case where the student does not exist
            return render(request, 'verify_students.html', {
                'unverified_students': unverified_students,
                'error_message': 'Student not found'
            })

    return render(request, 'verify_students.html', {'unverified_students': unverified_students})


def view_report(request):
    # Calculate the number of students verified
    verified_students_count = AMISStudent.objects.filter(is_verified=True).count()

    # Calculate the number of IDs printed
    ids_printed_count = AMISStudent.objects.filter(id_printed=True).count()

    # Calculate the number of IDs lost
    ids_lost_count = AMISStudent.objects.filter(id_lost=True).count()

    # Calculate the number of IDs replaced
    ids_replacement_requested_count = AMISStudent.objects.filter(id_replacement_requested=True).count()

    #  these counts passed to the template
    context = {
        'verified_students_count': verified_students_count,
        'ids_printed_count': ids_printed_count,
        'ids_lost_count': ids_lost_count,
        'ids_replacement_requested_count': ids_replacement_requested_count,
    }

    return render(request, 'view_report.html', context)


def print_ids(request):
    students = Student.objects.filter(is_verified=True, id_printed=False)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = Student.objects.get(id=student_id)
        student.id_printed = True
        student.save()
        return redirect('pc_officer_dashboard')

    return render(request, 'print_ids.html', {'students': students})


def view_verified_students(request):
    verified_students = AMISStudent.objects.filter(is_verified=True).order_by('course', 'year_of_study')

    # Group students by course and year of study
    grouped_students = {}
    for student in verified_students:
        if student.course not in grouped_students:
            grouped_students[student.course] = {}
        if student.year_of_study not in grouped_students[student.course]:
            grouped_students[student.course][student.year_of_study] = []
        grouped_students[student.course][student.year_of_study].append(student)

    return render(request, 'verified_students.html', {'grouped_students': grouped_students})


def view_printed_ids(request):
    printed_students = AMISStudent.objects.filter(id_printed=True).order_by('course', 'year_of_study')

    # Group students by course and year of study
    grouped_students = {}
    for student in printed_students:
        if student.course not in grouped_students:
            grouped_students[student.course] = {}
        if student.year_of_study not in grouped_students[student.course]:
            grouped_students[student.course][student.year_of_study] = []
        grouped_students[student.course][student.year_of_study].append(student)

    return render(request, 'printed_ids.html', {'grouped_students': grouped_students})


def students_by_course(request):
    students = Student.objects.filter(is_verified=True, id_printed=False)  # Verified but not printed

    # Group students by course
    grouped_students = defaultdict(list)
    for student in students:
        grouped_students[student.course].append(student)

    return render(request, 'students_by_course.html', {'grouped_students': dict(grouped_students)})


def verify_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.is_verified = True
        student.payment_status = 'paid'
        student.save()
        return redirect('students_by_course')  # Redirect after verification
    return render(request, 'verify_student.html', {'student': student})


def fetch_student_from_amis(request):
    if request.method == 'POST':
        form = FetchStudentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            # Print statement for debugging
            print(f"Fetching student with ID: {student_id}")

            # Fetch student data from AMISStudent model
            amis_student = get_object_or_404(AMISStudent, student_id=student_id)

            # Create or get the corresponding entry in the Student model
            student, created = Student.objects.get_or_create(
                student_id=amis_student.student_id,
                defaults={
                    'name': amis_student.name,
                    'course': amis_student.course,
                    'year_of_study': amis_student.year_of_study,
                    'mobile': amis_student.mobile,
                }
            )

            return render(request, 'fetch_student.html', {'student': student})
    else:
        form = FetchStudentForm()

    return render(request, 'fetch_student_form.html', {'form': form})


def fetch_all_students_from_amis(request):
    # Fetch all students from the AMISStudent model
    students = AMISStudent.objects.all().order_by('course', 'year_of_study')

    # Group students by course and year of study
    grouped_students = {}
    for student in students:
        if student.course not in grouped_students:
            grouped_students[student.course] = {}
        if student.year_of_study not in grouped_students[student.course]:
            grouped_students[student.course][student.year_of_study] = []
        grouped_students[student.course][student.year_of_study].append(student)

    return render(request, 'fetch_all_students.html', {'grouped_students': grouped_students})


def print_id(request, student_id):
    # Reinsert the slash where it was removed
    student_id = student_id[:5] + '/' + student_id[5:]
    student = get_object_or_404(AMISStudent, student_id=student_id)
    student.id_printed = True
    student.save()
    return render(request, 'print_id.html', {'student': student})


def report_lost_id(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')

        # Logic to handle reporting the lost ID (e.g., mark the student's ID as lost)
        # Assuming you have a Student model or similar logic
        try:
            student = AMISStudent.objects.get(student_id=student_id)
            student.id_lost = True
            student.save()
            message = f"Student {student.name} (ID: {student_id}) has been marked as lost."
        except AMISStudent.DoesNotExist:
            message = f"No student found with ID: {student_id}"

        return render(request, 'report_lost_id.html', {'message': message})

    return render(request, 'report_lost_id.html')


def handle_lost_id(request):
    # Fetch all students who have reported a lost ID
    students_with_lost_ids = AMISStudent.objects.filter(id_lost=True, id_replacement_requested=False)

    if request.method == "POST":
        student_id = request.POST.get('student_id')
        try:
            student = AMISStudent.objects.get(student_id=student_id)
            # Mark the student as verified for a new ID
            student.id_replacement_requested = True
            student.save()
            message = f"Student {student.name} (ID: {student_id}) has been verified for a new ID."
        except AMISStudent.DoesNotExist:
            message = f"No student found with ID: {student_id}"

        return render(request, 'handle_lost_id.html', {
            'students': students_with_lost_ids,
            'message': message
        })

    return render(request, 'handle_lost_id.html', {'students': students_with_lost_ids})


def view_verified_lost_ids(request):
    # Fetch students who have reported a lost ID, have been verified, and are not yet printed
    students_ready_for_printing = AMISStudent.objects.filter(id_replacement_requested=True, id_printed=True)

    return render(request, 'verified_lost_ids.html', {'students': students_ready_for_printing})


def lost_id_report(request):
    if request.method == "POST":
        form = ReportLostIDForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lost_id_verification')
    else:
        form = ReportLostIDForm()

    return render(request, 'lost_id_report.html', {'form': form})


def lost_id_verification(request):
    # Fetch all loss reports
    lost_students = LossReport.objects.all()

    # Create a list of students with details from AMISStudent
    student_details = []
    for report in lost_students:
        try:
            # Fetch the student details from the AMISStudent model using the student_id from LossReport
            student = AMISStudent.objects.get(student_id=report.student_id)
            student_details.append({
                'name': student.name,
                'student_id': report.student_id,
                'report_file': report.report_file,
                'reported_at': report.reported_at
            })
        except AMISStudent.DoesNotExist:
            # Handle the case where the student is not found in AMISStudent
            student_details.append({
                'name': 'Unknown',
                'student_id': report.student_id,
                'report_file': report.report_file,
                'reported_at': report.reported_at
            })

    return render(request, 'lost_id_verification.html', {'student_details': student_details})

