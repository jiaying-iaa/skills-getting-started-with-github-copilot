def test_signup_adds_participant(client):
    # Arrange
    activity = "Soccer Club"
    email = "test.signup@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity}"
    }
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity = "Unknown Club"
    email = "test.unknown@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"
    assert client.get("/activities").json()[activity]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_requires_email(client):
    # Arrange
    activity = "Soccer Club"

    # Act
    response = client.post(f"/activities/{activity}/signup")

    # Assert
    assert response.status_code == 422
