"""Integration tests for the nginx service."""

from http.client import HTTPConnection


def test_nginx_redirects_http_to_https(nginx_service):
    """The nginx service should redirect HTTP to HTTPS."""
    client = HTTPConnection(nginx_service.ip, timeout=5)
    client.request("GET", "/test")
    response = client.getresponse()

    assert response.status == 301
    assert response.headers["location"] == f"https://{nginx_service.ip}/test"


def test_nginx_proxies_frontend(nginx_client):
    """The nginx service should proxy the default server to the frontend."""
    nginx_client.request("GET", "/")
    response = nginx_client.getresponse()

    assert response.status == 200
    assert "text/html" in response.headers["content-type"]
