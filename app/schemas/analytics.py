from pydantic import BaseModel


class StudentCountOut(BaseModel):
    total_students: int
    active_students: int
    by_department: list[dict] = []


class AverageCGPAOut(BaseModel):
    overall_average_cgpa: float
    by_department: list[dict] = []


class PlacementRateOut(BaseModel):
    total_students: int
    placed_students: int
    placement_rate_percent: float
    average_package_lpa: float | None
    by_department: list[dict] = []


class AveragePackageOut(BaseModel):
    average_package_lpa: float | None
    median_package_lpa: float | None
    min_package_lpa: float | None
    max_package_lpa: float | None


class DepartmentPerformanceOut(BaseModel):
    department_id: int
    department_name: str
    student_count: int
    average_cgpa: float | None
    placement_rate: float | None


class AttendanceSummaryOut(BaseModel):
    overall_average_attendance: float
    below_75_percent_count: int
    by_department: list[dict] = []


class HigherStudiesSummaryOut(BaseModel):
    total: int
    by_country: list[dict] = []
    by_degree_type: list[dict] = []
