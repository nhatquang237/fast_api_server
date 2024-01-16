import pytest

from test_base import TestBase
from unittest.mock import patch


from utility import get_random_six_digit_str, get_oid_str

class TestLogin(TestBase):

    @pytest.mark.utility
    def test_get_random_six_digit_str(self):
        # Test length of 100 cases
        results = (get_random_six_digit_str() for _ in range(100))
        assert all((len(code) == 6 for code in results))

    @pytest.mark.utility
    @patch('random.randint')
    def test_get_six_specific_digit_str(self, mock_randint):
        # Mock the random function to allways return 1
        mock_randint.return_value = 1
        assert get_random_six_digit_str() == "111111"
        assert mock_randint.call_count == 6
