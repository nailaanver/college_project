from students.models import Student

MAX_SEMESTER = 6

def promote_students_of_semester(semester_number):
    """
    Promote ALL students of a given semester to next semester
    ONLY when admin clicks.
    """

    if semester_number >= MAX_SEMESTER:
        return 0, "Final semester students cannot be promoted"

    students = Student.objects.filter(semester=semester_number)

    if not students.exists():
        return 0, "No students in this semester"

    updated_count = students.update(semester=semester_number + 1)

    return updated_count, "Promotion successful"
