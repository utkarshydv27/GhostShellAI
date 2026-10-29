import app as ghost_app

def test_home():
    response = ghost_app.app.test_client().get('/')
    assert response.status_code == 200 and b'GhostShell' in response.data

def test_status(monkeypatch):
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self): return {'models': [{'name': 'qwen2.5:1.5b'}]}
    monkeypatch.setattr(ghost_app.requests, 'get', lambda *a, **k: FakeResponse())
    data = ghost_app.app.test_client().get('/api/status').get_json()
    assert data['ollama'] and data['model_available']

def test_offline(monkeypatch):
    def fail(*a, **k): raise ghost_app.requests.ConnectionError('offline')
    monkeypatch.setattr(ghost_app.requests, 'get', fail)
    assert ghost_app.app.test_client().get('/api/status').get_json()['ollama'] is False

def test_empty_prompt():
    response = ghost_app.app.test_client().post('/api/whisper', json={'message': ' '})
    assert response.status_code == 400

def test_fallback_story():
    assert 'yesterday.txt' in ghost_app.fallback('story')

def test_memories():
    response = ghost_app.app.test_client().get('/api/memories')
    assert response.status_code == 200
    assert isinstance(response.get_json()['events'], list)
