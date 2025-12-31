def test_posts_contract_types(http_get, base_url):
    r = http_get(f"{base_url}/posts/1", expected_status=200)
    d = r.json()

    assert isinstance(d["userId"], int)
    assert isinstance(d["id"], int)
    assert isinstance(d["title"], str)
    assert isinstance(d["body"], str)
