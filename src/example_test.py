# Run all tests with 'py.test'
# This will discover all tests within files whose names end with '_test'

# Very basic test
def double(x):
    return x * 2

def test_double():
    """All test methods must start with 'test_'"""
    assert double(2) == 4

# An example that uses "pytest.raises" funcion
import pytest

def fails():
    raise SystemExit(1)

def test_exception_raising():
    with pytest.raises(SystemExit):
        fails()

# For more examples, see: http://pytest.org/latest/getting-started.html
