import platform

from hostseditor.utils import get_hosts_file_path


# TODO: Add test for windows machines.


def test_get_hosts_file_path__linux():
    if platform.system() == 'Linux':
        assert '/etc/hosts' == str(get_hosts_file_path())
