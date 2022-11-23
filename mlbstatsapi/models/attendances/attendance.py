from dataclasses import dataclass, field
from typing import Union, List
from .attributes import AttendanceTotals, AttendanceRecords

@dataclass
class Attendance:
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
    aggregatetotals: Union[AttendanceTotals, dict]
    records: Union[List[AttendanceRecords], List[dict]] = field(default_factory=list)

    def __post_init__(self):
        self.records = [AttendanceRecords(**record) for record in self.records if self.records]
        self.aggregatetotals = AttendanceTotals(**self.aggregatetotals)