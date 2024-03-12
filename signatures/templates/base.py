import detection_enums


class Base:
    def potential(self, *args, **kwargs):
        raise NotImplementedError()

    async def check(self, *args, **kwargs):
        raise NotImplementedError()

    def __init__(
        self, info, confidence=detection_enums.CONFIDENCE.CONFIRMED, more_info_url=""
    ):
        if type(info) != str:
            raise ValueError("INFO is not string")
        self.INFO = info

        if type(confidence) != detection_enums.CONFIDENCE:
            raise ValueError("CONFIDENCE is not a valid enum")
        self.CONFIDENCE = confidence

        self.more_info_url = more_info_url
