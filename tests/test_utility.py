import pytest
from test_base import TestBase
from utility import get_random_six_digit_str

class TestLogin(TestBase):

    @pytest.mark.utility
    def test_get_random_six_digit_str(self):
        results = (get_random_six_digit_str() for _ in range(100))
        assert all((len(code) for code in results))
