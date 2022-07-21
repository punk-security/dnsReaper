import signatures
import detection_enums

signatures = [getattr(signatures, signature).test for signature in signatures.__all__]


def test_signatures_all_have_a_potential():
    for signature in signatures:
        assert callable(getattr(signature, "potential"))


def test_signatures_all_have_a_check():
    for signature in signatures:
        assert callable(getattr(signature, "check"))


def test_signatures_all_have_an_INFO_string():
    for signature in signatures:
        assert type(getattr(signature, "INFO")) is str


def test_signatures_all_have_an_INFO_string():
    for signature in signatures:
        assert type(getattr(signature, "CONFIDENCE")) is detection_enums.CONFIDENCE


def test_signatures_INFO_strings_are_unique():
    INFOs = [signature.INFO for signature in signatures]
    assert len(INFOs) == len(set(INFOs))
