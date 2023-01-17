def test_hello(client):
    response = client.get('/Test2/test2')
    assert response.data == b'Google'