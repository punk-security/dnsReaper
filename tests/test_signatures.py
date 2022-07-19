import signatures

signatures = [getattr(signatures, signature) for signature in signatures.__all__]


def test_signatures_all_have_a_potential():
    for signature in signatures:
        assert callable(getattr(signature, "potential"))


def test_signatures_all_have_a_potential():
    for signature in signatures:
        assert callable(getattr(signature, "check"))


def test_signatures_all_have_an_INFO_string():
    for signature in signatures:
        assert type(getattr(signature, "INFO")) is str


def test_signatures_INFO_strings_are_unique():
    INFOs = [signature.INFO for signature in signatures]
    assert len(INFOs) == len(set(INFOs))
