import tempfile

import pytest
from pathlib import Path


TEST_HOSTS_CONTENT = """127.0.0.1   test

# Comment for a line
0.0.0.0 tester tester2"""

TEST_HOSTS_CONTENT_NO_DATA = "\n# Comment for a line"

TEST_HOSTS_CONTENT_NO_LOCAL = """\n# Comment for a line
0.0.0.0 tester tester2"""


@pytest.fixture
def tmpfile(tmp_path) -> Path:
    file = tmp_path / "temp_hosts"
    file.write_text("")
    return Path(file)
