import json


def test_search_jobs(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search",
        data=json.dumps(
            {"words": "Software Engineer", "location": "San Francisco", "offset": 0}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Successfully searched." in data["message"]
    assert "success" in data["status"]
    assert data["data"]
    assert data["data"]["words"] == "Software Engineer"
    assert data["data"]["location"] == "San Francisco"
    assert data["data"]["offset"] == 0
    assert data["data"]["jobs"]
    assert resp.content_type == "application/json"


def test_search_jobs_invalid_json(test_app):
    client = test_app.test_client()
    resp = client.post("/search", data=json.dumps({}), content_type="application/json")
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_invalid_json_keys_no_words(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search",
        data=json.dumps({"location": "San Francisco", "offset": 0}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_invalid_json_keys_no_location(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search",
        data=json.dumps({"words": "Software Engineer", "offset": 0}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_invalid_json_keys_no_offset(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search",
        data=json.dumps({"words": "Software Engineer", "location": "San Francisco"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_no_jobs(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search",
        data=json.dumps({"words": "a", "location": "a", "offset": 0}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. Can't find jobs." in data["message"]
    assert "fail" in data["status"]
    assert not data["data"]
    assert resp.content_type == "application/json"
