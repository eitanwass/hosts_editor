import pytest
from pathlib import Path


TEST_HOSTS_CONTENT = "127.0.0.1   test"


@pytest.fixture
def preset_test_hosts(tmp_path) -> str:
    hosts = Path(tmp_path) / 'hosts'
    hosts.write_text(TEST_HOSTS_CONTENT)
    return str(hosts)
