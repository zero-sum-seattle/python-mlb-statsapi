from dataclasses import dataclass, field
from typing import Union, Dict, List, Any
from .attributes import AttendanceAggregateTotals, AttendanceRecords

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
    aggregateTotals : AttendanceAggregateTotals
        Attendence aggregate total numbers for query
    """
    aggregateTotals: Union[AttendanceAggregateTotals, Dict[str, Any]]
    records: Union[List[AttendanceRecords], List[Dict[str, Any]]] = field(default_factory=list)


    def __post_init__(self):
        self.records = [AttendanceRecords(**record) for record in self.records if self.records]
        self.aggregateTotals = AttendanceAggregateTotals(**self.aggregateTotals)