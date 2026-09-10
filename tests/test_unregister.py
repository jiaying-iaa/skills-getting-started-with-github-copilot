def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity}"
    }
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity = "Unknown Club"
    email = "test.unknown@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_not_found_for_unknown_participant(client):
    # Arrange
    activity = "Soccer Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_requires_email(client):
    # Arrange
    activity = "Soccer Club"

    # Act
    response = client.delete(f"/activities/{activity}/signup")

    # Assert
    assert response.status_code == 422


def test_signup_and_unregister_complete_lifecycle(client):
    # Arrange
    activity = "Soccer Club"
    email = "test.lifecycle@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )
    unregister_response = client.delete(
        f"/activities/{activity}/signup", params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
