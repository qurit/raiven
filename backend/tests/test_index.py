def test_index(client):
    res: Response = client.get('/hello')
    assert res.status_code == 200, "User should be able to log on"