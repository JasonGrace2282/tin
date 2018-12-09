from django import http
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile

from .models import Assignment
from .forms import AssignmentForm, FileSubmissionForm, TextSubmissionForm
from ..courses.models import Course
from ..submissions.models import Submission, upload_submission_file_path
from ..users.models import User
from ..auth.decorators import login_required, teacher_or_superuser_required


@login_required
def show_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id = assignment_id)

    if request.user.is_student:
        if assignment.course in request.user.courses.all():
            submissions = Submission.objects.filter(student = request.user, assignment = assignment).order_by("-date_submitted")
            latest_submission = (submissions.latest("date_submitted") if submissions else None)

            latest_submission_text = None
            if latest_submission:
                latest_submission_text = latest_submission.file.read().decode()
                if len(latest_submission_text) > 7500: #7.5K
                    latest_submission_text = None

            return render(
                request,
                "assignments/show.html",
                {
                    "course": assignment.course,
                    "assignment": assignment,
                    "submissions": submissions,
                    "latest_submission": latest_submission,
                    "latest_submission_text": latest_submission_text,
                },
            )
        else:
            raise http.Http404
    else:
        if request.user.is_superuser or request.user == assignment.course.teacher:
            students_and_submissions = []
            for student in assignment.course.students.all():
                student_submissions = Submission.objects.filter(student = student, assignment = assignment)
                if student_submissions:
                    students_and_submissions.append((student, student_submissions.latest("date_submitted")))
                else:
                    students_and_submissions.append((student, None))

            return render(
                request,
                "assignments/show.html",
                {
                    "course": assignment.course,
                    "assignment": assignment,
                    "students_and_submissions": students_and_submissions,
                },
            )
        else:
            raise http.Http404


@teacher_or_superuser_required
def create_view(request, course_id):
    """ Creates an assignment """
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.teacher and not request.user.is_superuser:
        raise http.Http404

    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit = False)
            assignment.course = course
            assignment.save()
            return redirect("assignments:show", assignment.id)
    else:
        form = AssignmentForm()
    return render(
        request,
        "assignments/edit_create.html",
        {
            "form": form,
            "course": course,
            "action": "add",
            "nav_item": "Create assignment",
        },
    )


@teacher_or_superuser_required
def edit_view(request, assignment_id):
    """ Edits an assignment """
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user != assignment.course.teacher and not request.user.is_superuser:
        raise http.Http404

    if request.method == "POST":
        form = AssignmentForm(data=request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect("assignments:show", assignment.id)
    else:
        form = AssignmentForm(instance=assignment)

    return render(
        request,
        "assignments/edit_create.html",
        {
            "form": form,
            "course": assignment.course,
            "assignment": assignment,
            "action": "edit",
            "nav_item": "Edit",
        },
    )


@teacher_or_superuser_required
def student_submission_view(request, assignment_id, student_id):
    assignment = get_object_or_404(Assignment, id = assignment_id)
    student = get_object_or_404(User, id = student_id)

    submissions = Submission.objects.filter(student = student, assignment = assignment).order_by("-date_submitted")
    latest_submission = (submissions.latest("date_submitted") if submissions else None)

    return render(
        request,
        "assignments/student_submission.html",
        {
            "course": assignment.course,
            "assignment": assignment,
            "student": student,
            "submissions": submissions,
            "latest_submission": latest_submission,
        },
    )


@login_required
def submit_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id = assignment_id)

    if request.user not in assignment.course.students.all():
        raise http.Http404
    student = request.user

    file_form = FileSubmissionForm()
    text_form = TextSubmissionForm()
    if request.method == "POST":
        if request.FILES.get("file"):
            file_form = FileSubmissionForm(request.POST, request.FILES)
            if file_form.is_valid():
                submission = file_form.save(commit = False)
                submission.assignment = assignment
                submission.student = student
                submission.save()
                return redirect("assignments:show", assignment.id)
        else:
            text_form = TextSubmissionForm(request.POST)
            if text_form.is_valid():
                submission = text_form.save(commit = False)
                submission.assignment = assignment
                submission.student = student
                submission.file.save(upload_submission_file_path(submission, ""), ContentFile(text_form.cleaned_data["text"]), save = False)
                submission.save()
                return redirect("assignments:show", assignment.id)

    return render(request,
        "assignments/submit.html",
        {
            "file_form": file_form,
            "text_form": text_form,
            "course": assignment.course,
            "assignment": assignment,
            "student": student,
        },
    )
