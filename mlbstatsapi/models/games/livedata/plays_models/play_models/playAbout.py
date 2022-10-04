from dataclasses import dataclass

@dataclass
class PlaysPlayAbout:
    atBatIndex:         int
    halfInning:         str
    isTopInning:        bool
    inning:             int
    startTime:          str
    endTime:            str
    isComplete:         bool
    isScoringPlay:      bool
    hasReview:          bool
    hasOut:             bool
    captivatingIndex:   int
