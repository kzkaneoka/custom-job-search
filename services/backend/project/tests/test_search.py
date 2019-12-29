import json


def test_search_jobs(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search",
        data=json.dumps({"words": "Software Engineer", "location": "San Francisco"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Successfully searched." in data["message"]
    assert "success" in data["status"]
    assert data["words"] == "Software Engineer"
    assert data["location"] == "San Francisco"
    assert data["offset"] == 0
    assert data["jobs"]
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
        data=json.dumps({"location": "San Francisco"}),
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
        data=json.dumps({"words": "Software Engineer"}),
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
        data=json.dumps({"words": "a", "location": "a"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. Can't find jobs." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_next(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/next",
        data=json.dumps(
            {"words": "Software Engineer", "location": "San Francisco", "offset": 0}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Successfully searched." in data["message"]
    assert "success" in data["status"]
    assert data["words"] == "Software Engineer"
    assert data["location"] == "San Francisco"
    assert data["offset"] == 10
    assert data["jobs"]
    assert resp.content_type == "application/json"


def test_search_jobs_next_invalid_json(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/next", data=json.dumps({}), content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_next_invalid_json_keys_no_words(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/next",
        data=json.dumps({"location": "San Francisco", "offset": 0}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_next_invalid_json_keys_no_location(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/next",
        data=json.dumps({"words": "Software Engineer", "offset": 0}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_next_invalid_json_keys_no_offset(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/next",
        data=json.dumps({"words": "Software Engineer", "location": "San Francisco"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_next_no_jobs(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/next",
        data=json.dumps({"words": "a", "location": "a", "offset": 0}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. Can't find jobs." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_prev(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/prev",
        data=json.dumps(
            {"words": "Software Engineer", "location": "San Francisco", "offset": 10}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Successfully searched." in data["message"]
    assert "success" in data["status"]
    assert data["words"] == "Software Engineer"
    assert data["location"] == "San Francisco"
    assert data["offset"] == 0
    assert data["jobs"]
    assert resp.content_type == "application/json"


def test_search_jobs_prev_invalid_json(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/prev", data=json.dumps({}), content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_prev_invalid_json_keys_no_words(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/prev",
        data=json.dumps({"location": "San Francisco", "offset": 10}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_prev_invalid_json_keys_no_location(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/prev",
        data=json.dumps({"words": "Software Engineer", "offset": 10}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_prev_invalid_json_keys_no_offset(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/prev",
        data=json.dumps({"words": "Software Engineer", "location": "San Francisco"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_search_jobs_prev_no_jobs(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/search/prev",
        data=json.dumps({"words": "a", "location": "a", "offset": 10}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. Can't find jobs." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"
