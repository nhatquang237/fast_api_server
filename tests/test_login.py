import pytest
from test_base import TestBase, test_account



class TestLogin(TestBase):

    @pytest.mark.login
    def test_register(self):
        response = self.client.post("/register", json=test_account)
        assert response.status_code == 200
        assert isinstance(response.json(), str)

    @pytest.mark.login
    def test_dulicate_register(self):
        response = self.client.post("/register", json=test_account)
        assert response.status_code == 400
        assert response.json() in (None, 'None')

    @pytest.mark.login
    def test_login(self):
        response = self.client.post("/login", data=test_account)
        result = response.json()
        assert response.status_code == 200
        assert result["access_token"] is not None
        assert result["token_type"] == "bearer"

    @pytest.mark.login
    def test_username_check(self):
        response = self.client.post("/check", json=test_account)
        assert response.status_code == 200
        assert response.json() is True
