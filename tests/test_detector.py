from app.detector import path_entropy, event_features

def test_entropy_empty():
    assert path_entropy("") == 0.0

def test_features_shape():
    e = {"src_ip": "198.51.100.1", "status_code": 401, "event_type": "login_failed",
         "path": "/login", "user_agent": "test", "bytes_sent": 12}
    assert len(event_features(e)) == 8
