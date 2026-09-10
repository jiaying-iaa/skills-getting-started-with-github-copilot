from fastapi.testclient import TestClient


def test_get_activities_returns_all_activities(client: TestClient):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert expected_activity in response.json()
    assert response.json()[expected_activity]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_root_redirects_to_static_index(client: TestClient):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location
