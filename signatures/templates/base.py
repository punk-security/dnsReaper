import detection_enums


class Base:
    def potential(self, *args, **kwargs):
        raise NotImplementedError()

    def check(self, *args, **kwargs):
        raise NotImplementedError()

    def __init__(self, info, confidence):
        if type(info) != str:
            raise ValueError("INFO is not string")
        self.INFO = info
        if type(confidence) != detection_enums.CONFIDENCE:
            raise ValueError("CONFIDENCE is not a valid enum")
        self.CONFIDENCE = confidence
