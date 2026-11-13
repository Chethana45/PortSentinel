import pytest
from app.process_inspector import terminate_process

def test_termination_requires_confirmation():
    with pytest.raises(PermissionError):
        terminate_process(999999, "anything", False)
