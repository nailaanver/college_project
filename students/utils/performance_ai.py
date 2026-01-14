def generate_academic_summary(attendance, internal_avg):

    if attendance >= 90 and internal_avg >= 80:
        return (
            "Excellent academic performance. Your attendance is outstanding "
            "and internal marks show strong subject understanding. "
            "Keep up the great consistency."
        )

    elif attendance >= 80 and internal_avg >= 70:
        return (
            "Very good performance. You maintain good attendance and "
            "solid internal marks. With a little more focus, you can excel."
        )

    elif attendance >= 75 and internal_avg >= 60:
        return (
            "Good progress. Attendance is acceptable and internal marks "
            "are satisfactory. Regular revision can improve results."
        )

    elif attendance >= 65 and internal_avg >= 50:
        return (
            "Average performance. Both attendance and internal marks "
            "need improvement. Better consistency is recommended."
        )

    else:
        return (
            "Academic performance needs attention. Low attendance or "
            "internal marks may affect final results. Immediate focus is required."
        )
