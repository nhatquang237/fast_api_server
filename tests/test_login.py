from base_test import TestBase

test_data = {
    "username": "testuser",
    "password": "testpassword"
}

class TestLogin(TestBase):

    def test_register(self):
        response = self.client.post("/register", json=test_data)
        assert response.status_code == 200
        assert isinstance(response.json(), str)

    def test_dulicate_register(self):
        response = self.client.post("/register", json=test_data)
        assert response.status_code == 400
        assert response.json() in (None, 'None')

    def test_login(self):
        response = self.client.post("/login", data=test_data)
        result = response.json()
        assert response.status_code == 200
        assert result["access_token"] is not None
        assert result["token_type"] == "bearer"

    def test_username_check(self):
        response = self.client.post("/check", json=test_data)
        assert response.status_code == 200
        assert response.json() is True
