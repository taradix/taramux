"""Service fixtures."""

import ssl
from http.client import HTTPSConnection

import pytest
from pytest_xdocker.compose import ComposeServer, find_compose_files


@pytest.fixture(scope="session")
def env_vars():
    """Environment variables for the services."""
    return {
        "SERVER_HOSTNAME": "test.local",
        "IPV4_NETWORK": "172.22.250",
        "IPV6_NETWORK": "fd4d:6169:6c63:7465::/64",
    }


@pytest.fixture(scope="session")
def env_file(env_vars, request):
    """Environment file containing `env_vars`.

    Cached for troubleshooting purposes.
    """
    env_file = request.config.cache.mkdir("taramux") / "env"
    with env_file.open("w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")

    return env_file


@pytest.fixture(scope="session")
def nginx_service(env_file, process, request):
    """Nginx service fixture."""
    server = ComposeServer(
        "start worker process",
        env_file=env_file,
        compose_files=find_compose_files(request.config.rootdir),
        process=process,
    )
    with server.run("nginx") as service:
        yield service


@pytest.fixture
def nginx_client(nginx_service):
    """Client to the nginx service fixture, over the self-signed dev cert."""
    client = HTTPSConnection(nginx_service.ip, timeout=5, context=ssl._create_unverified_context())  # noqa: S323
    yield client
    client.close()
