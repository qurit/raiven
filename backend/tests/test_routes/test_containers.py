def test_index(client):
    res: Response = client.get('/containers')
    assert res.status_code == 200
    assert type(res.json['containers']) is list
