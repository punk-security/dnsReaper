from pyclbr import Function
import signatures

signatures = [getattr(signatures, signature) for signature in signatures.__all__]

for signature in signatures:
    assert callable(getattr(signature, "potential"))
    assert callable(getattr(signature, "check"))
    assert type(getattr(signature, "INFO")) is str
