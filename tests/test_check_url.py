from find_dead_links.check_url import check_url


class TestCheckUrl:
    def test_valid_url(self):
        url = "https://www.cartong.org"
        is_reachable, err_msg = check_url(url, "")
        assert is_reachable
        assert err_msg == ""

    def test_valid_url_with_domain(self):
        url = "/contact"
        web_domain = "https://www.cartong.org"
        is_reachable, err_msg = check_url(url, web_domain)
        assert is_reachable
        assert err_msg == ""

    def test_invalid_url(self):
        url = "htp:/invalid-url"
        is_reachable, err_msg = check_url(url, "")
        assert is_reachable is False
        assert err_msg == "No connection adapters were found for 'htp:/invalid-url'"

    def test_bad_url(self):
        url = "https://www.ongcarto.org"
        is_reachable, err_msg = check_url(url, "")
        assert is_reachable is False
        assert err_msg.startswith("HTTPSConnectionPool(host='www.ongcarto.org', port=443): Max retries exceeded")

    def test_empty_url(self):
        is_reachable, err_msg = check_url("", "")
        assert is_reachable is False
        assert err_msg == "Invalid URL '': No scheme supplied. Perhaps you meant https://?"
