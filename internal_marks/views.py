from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import TimeTable

from notifications.utils import create_notification
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def teacher_internal_subjects(request):
    teacher = request.user.teacher  # assuming OneToOne with User

    timetables = (
        TimeTable.objects
        .filter(teacher=teacher)
        .select_related('subject')
        .values(
            'course',
            'semester',
            'subject__id',
            'subject__name'
        )
        .distinct()
    )

    context = {
        'subjects': timetables
    }
    return render(
        request,
        'internal_marks/teacher_subject_list.html',
        context
    )

from teachers.models import Subject
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from students.models import Student
from teachers.models import Subject
from dashboard.models import TimeTable
from .models import InternalMark


@login_required
def teacher_enter_marks(request, course, semester, subject_id):
    teacher = request.user.teacher
    subject = get_object_or_404(Subject, id=subject_id)

    # 🔒 SECURITY CHECK (VERY IMPORTANT)
    has_permission = TimeTable.objects.filter(
        teacher=teacher,
        course=course,
        semester=semester,
        subject=subject
    ).exists()

    if not has_permission:
        return HttpResponseForbidden("You are not allowed to enter marks for this subject")

    # 🎓 Get students
    students = Student.objects.filter(
        course=course,
        semester=semester
    ).order_by('register_number')

    internal_marks = []

    for student in students:
        timetable = TimeTable.objects.filter(
            teacher=teacher,
            course=course,
            semester=semester,
            subject=subject
        ).first()

        internal_mark, created = InternalMark.objects.get_or_create(
            student=student,
            subject=subject,
            timetable=timetable
        )

        internal_marks.append(internal_mark)

    # 💾 SAVE MARKS
    if request.method == "POST":
        for mark in internal_marks:
            if mark.status == 'Submitted':
                continue  # 🔒 cannot edit after submit

            mark.test1 = int(request.POST.get(f"test1_{mark.id}", mark.test1) or 0)
            mark.test2 = int(request.POST.get(f"test2_{mark.id}", mark.test2) or 0)
            mark.assignment = int(request.POST.get(f"assignment_{mark.id}", mark.assignment) or 0)


            mark.save()

        # 📤 SUBMIT
        if 'submit' in request.POST:
            for mark in internal_marks:
                mark.status = 'Submitted'
                mark.save()

            # 🔔 ADMIN NOTIFICATION
            admins = User.objects.filter(is_staff=True, is_superuser=True)

            for admin in admins:
                create_notification(
                    recipient=admin,
                    title="Internal Marks Submitted",
                    message=(
                        f"{teacher.user.get_full_name()} submitted internal marks "
                        f"for {subject.name} (Course {course}, Semester {semester})."
                    ),
                    notification_type="MARKS",
                    reference_id=subject.id
                )


        return redirect('teacher-internal-subjects')

    context = {
        'subject': subject,
        'course': course,
        'semester': semester,
        'internal_marks': internal_marks,
    }

    return render(
        request,
        'internal_marks/teacher_enter_marks.html',
        context
    )


# @login_required
# def teacher_enter_marks(request, course, semester, subject_id):
#     teacher = request.user.teacher
#     subject = get_object_or_404(Subject, id=subject_id)

#     # 🔒 SECURITY CHECK (VERY IMPORTANT)
#     has_permission = TimeTable.objects.filter(
#         teacher=teacher,
#         course=course,
#         semester=semester,
#         subject=subject
#     ).exists()

#     if not has_permission:
#         return HttpResponseForbidden("You are not allowed to enter marks for this subject")

#     # 🎓 Get students
#     students = Student.objects.filter(
#         course=course,
#         semester=semester
#     ).order_by('register_number')

#     internal_marks = []

#     for student in students:
#         timetable = TimeTable.objects.filter(
#             teacher=teacher,
#             course=course,
#             semester=semester,
#             subject=subject
#         ).first()

#         internal_mark, created = InternalMark.objects.get_or_create(
#             student=student,
#             subject=subject,
#             timetable=timetable
#         )

#         internal_marks.append(internal_mark)

#     # 💾 SAVE MARKS
#     if request.method == "POST":
#         for mark in internal_marks:
#             if mark.status == 'Submitted':
#                 continue  # 🔒 cannot edit after submit

#             mark.test1 = request.POST.get(f"test1_{mark.id}", mark.test1)
#             mark.test2 = request.POST.get(f"test2_{mark.id}", mark.test2)
#             mark.assignment = request.POST.get(f"assignment_{mark.id}", mark.assignment)

#             mark.save()

#         # 📤 SUBMIT
#         if 'submit' in request.POST:
#             for mark in internal_marks:
#                 mark.status = 'Submitted'
#                 mark.save()

#         return redirect('teacher-internal-subjects')

#     context = {
#         'subject': subject,
#         'course': course,
#         'semester': semester,
#         'internal_marks': internal_marks,
#     }

#     return render(
#         request,
#         'internal_marks/teacher_enter_marks.html',
#         context
#     )
    
    
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import InternalMark
from teachers.models import Subject

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_internal_subjects(request):
    subjects = (
        InternalMark.objects
        .filter(status='Submitted')
        .values(
            'subject__id',
            'subject__name',
            'subject__course',
            'subject__semester'
        )
        .annotate(total_students=Count('id'))
        .distinct()
    )

    return render(request, 'adminpanel/internal_subjects.html', {
        'subjects': subjects
    })

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_review_marks(request, course, semester, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    internal_marks = InternalMark.objects.filter(
        subject=subject,
        student__course=course,
        student__semester=semester,
        status='Submitted'
    ).select_related('student')

    if request.method == 'POST':
        if 'approve' in request.POST:
            for mark in internal_marks:
                mark.status = 'Approved'
                mark.save()

                # 🔔 TEACHER NOTIFICATION
                if hasattr(mark.timetable.teacher, 'user') and mark.timetable.teacher.user:
                    create_notification(
                        recipient=mark.timetable.teacher.user,
                        title="Internal Marks Approved",
                        message=(
                            f"Internal marks for {subject.name} "
                            f"(Course {course}, Semester {semester}) "
                            f"have been approved by admin."
                        ),
                        notification_type="MARKS",
                        reference_id=mark.id
                    )

                # 🔔 STUDENT NOTIFICATION (PUBLISHED)
                if hasattr(mark.student, 'user') and mark.student.user:
                    create_notification(
                        recipient=mark.student.user,
                        title="Internal Marks Published",
                        message=(
                            f"Your internal marks for {subject.name} "
                            f"have been published."
                        ),
                        notification_type="MARKS",
                        reference_id=mark.id
                    )


        elif 'reject' in request.POST:
            for mark in internal_marks:
                mark.status = 'Draft'
                mark.save()

                # 🔔 TEACHER NOTIFICATION
                create_notification(
                    recipient=mark.timetable.teacher.user,
                    title="Internal Marks Rejected",
                    message=(
                        f"Internal marks for {subject.name} "
                        f"(Course {course}, Semester {semester}) "
                        f"were rejected by admin. Please revise and resubmit."
                    ),
                    notification_type="MARKS",
                    reference_id=mark.id
                )


        return redirect('admin-internal-subjects')

    return render(request, 'adminpanel/review_marks.html', {
        'subject': subject,
        'course': course,
        'semester': semester,
        'internal_marks': internal_marks
    })

