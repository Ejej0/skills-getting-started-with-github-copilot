def test_unregister_success(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_activity_not_found(client):
    response = client.delete(
        "/activities/Unknown Club/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_signed_up(client):
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
