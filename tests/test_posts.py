def test_get_posts_returns_200_and_list(http_get, base_url):
    r = http_get(f"{base_url}/posts", expected_status=200)

    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_single_post_has_expected_fields(http_get, base_url):
    r = http_get(f"{base_url}/posts/1", expected_status=200)
    data = r.json()

    assert "userId" in data
    assert "id" in data
    assert "title" in data
    assert "body" in data
    assert data["id"] == 1
