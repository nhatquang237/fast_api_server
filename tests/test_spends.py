import pytest
from test_base import TestBase, test_account, test_data

insert_id = None
class TestSpends(TestBase):
    login_token = None

    @pytest.fixture
    def headers(self) -> dict:
        if not self.login_token:
            # Login with testing account to get token
            response = self.client.post("/login", data=test_account)
            self.login_token = response.json()['access_token']

        headers = {
            "Authorization": f"Bearer {self.login_token}"
        }

        # Give out headers as required material for testing authenticated request
        yield headers

    @pytest.mark.spend
    def test_get_data(self, headers):

        response = self.client.get("/data", headers=headers)

        assert response.status_code == 200
        received_data = response.json()

        assert "shareholderData" in received_data
        assert received_data["shareholderData"]['_id']
        assert received_data["shareholderData"]['names']

        assert "spendData" in received_data
        assert len(received_data["spendData"]) > 0

    @pytest.mark.spend
    def test_add_data(self, headers):
        response = self.client.post("/add", json=[test_data], headers=headers)
        assert response.status_code == 200

        global insert_id
        insert_id = response.json()

        assert insert_id != ""

    @pytest.mark.spend
    def test_update_data(self, headers):
        test_data["name"] = "Test update spend"
        test_data["id"] = insert_id
        response = self.client.put("/update", json=[test_data], headers=headers)
        assert response.status_code == 200
        assert response.json() == "Database updated successfully"

    @pytest.mark.spend
    def test_delete_data(self, headers):
        data = {"ids": [insert_id]}
        response = self.client.patch("/delete", json=data, headers=headers)
        assert response.status_code == 200
        assert response.json().startswith("Database value updated successfully")
