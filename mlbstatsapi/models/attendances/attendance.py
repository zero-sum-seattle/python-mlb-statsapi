from typing import List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import AttendanceTotals, AttendanceRecords


class Attendance(MLBBaseModel):
    """
    A class to represent attendance.

    Attributes
    ----------
    records : List[AttendanceRecords]
        List of attendance records.
    aggregate_totals : AttendanceTotals
        Attendance aggregate total numbers for query.
    """
    aggregate_totals: AttendanceTotals = Field(alias="aggregatetotals")
    records: List[AttendanceRecords] = []
