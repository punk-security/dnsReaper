import signatures
import pytest

all_signatures = [getattr(signatures, signature) for signature in signatures.__all__]


@pytest.mark.parametrize("signature", all_signatures)
def test_signatures_have_a_test_defined(signature):
    assert hasattr(signature, "test") == True


@pytest.mark.parametrize("signature", all_signatures)
def test_signatures_inherit_from_Base(signature):
    assert issubclass(type(signature.test), signatures.templates.base.Base)


def test_signatures_INFO_strings_are_unique():
    INFOs = [signature.test.INFO for signature in all_signatures]
    assert len(INFOs) == len(set(INFOs))
