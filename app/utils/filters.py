"""
Column whitelist for sorting — prevents ORDER BY injection.
"""
from fastapi import HTTPException, Query, status

# Allowed sort columns per major table
STUDENT_SORT_COLS = {
    "id", "student_uid", "roll_number", "full_name", "batch_year",
    "admission_year", "current_semester", "current_status",
    "department_id", "program_id", "created_at",
}
FACULTY_SORT_COLS = {"id", "faculty_uid", "full_name", "department_id", "status", "joining_date"}
COURSE_SORT_COLS = {"id", "course_code", "course_name", "semester", "credits", "status"}
PLACEMENT_SORT_COLS = {"id", "student_id", "company_name", "package_lpa", "placement_date", "offer_status"}
PERFORMANCE_SORT_COLS = {"id", "student_id", "semester", "sgpa", "cgpa", "academic_year", "backlogs_count"}
ENROLLMENT_SORT_COLS = {"id", "student_id", "course_id", "academic_year", "semester", "enrollment_status"}
INTERNSHIP_SORT_COLS = {"id", "student_id", "company_name", "start_date", "completion_status"}
CERTIFICATION_SORT_COLS = {"id", "student_id", "certification_name", "issue_date", "domain"}
PROJECT_SORT_COLS = {"id", "student_id", "project_title", "project_type", "status"}


def validate_sort_col(sort: str, allowed: set[str]) -> str:
    if sort not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "INVALID_PARAMETER",
                    "message": f"Sort column '{sort}' is not allowed. Allowed: {sorted(allowed)}",
                    "status": 400,
                }
            },
        )
    return sort


def sort_order_param(
    sort: str = Query(default="id", description="Column to sort by"),
    order: str = Query(default="asc", pattern="^(asc|desc)$", description="asc or desc"),
):
    return sort, order
