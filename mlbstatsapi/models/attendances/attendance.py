from dataclasses import dataclass, field
from typing import Union, List
from .attributes import AttendanceTotals, AttendanceRecords
from pydantic import BaseModel


class Attendance(BaseModel):
    """
    A class to represent attendance.
    Attributes
    ----------
    copyright : str
        Copyright message
    records : List[AttendanceRecords]
        List of attendance records
    aggregatetotals : AttendanceAggregateTotals
        Attendence aggregate total numbers for query
    """
    aggregateTotals: AttendanceTotals
    records: Union[List[AttendanceRecords]] = field(default_factory=list)
