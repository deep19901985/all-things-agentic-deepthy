import pytest

from models import validate_incident_text


def test_incident_text_rejects_oversize_input():
    with pytest.raises(ValueError, match="under 8,000"):
        validate_incident_text("x" * 8_001)

