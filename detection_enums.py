from enum import Enum


class CONFIDENCE(Enum):
    CONFIRMED = "is confirmed possible"
    POTENTIAL = "may be possible"
    UNLIKELY = "maybe be possible (although unlikely)"
