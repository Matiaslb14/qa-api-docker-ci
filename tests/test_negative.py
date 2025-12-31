def test_unknown_route_returns_404(http_get, base_url):
    r = http_get(f"{base_url}/this-route-does-not-exist")
    assert r.status_code == 404


def test_post_not_found_behavior(http_get, base_url):
    # JSONPlaceholder a veces responde 200 con {} para IDs inexistentes.
    r = http_get(f"{base_url}/posts/999999")

    assert r.status_code in (200, 404)
    if r.status_code == 200:
        assert r.json() == {}
