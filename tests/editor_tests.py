from unittest import mock

import pytest

from hostseditor import HostsEntry
from hostseditor.editor import HostsEditor
from tests.conftest import TEST_HOSTS_CONTENT, TEST_HOSTS_CONTENT_NO_DATA, TEST_HOSTS_CONTENT_NO_LOCAL


DATA_TWO_ENTRIES_COMMENT_BLANK_LINE = """127.0.0.1 name1
# Test Comment

0.0.0.0 name2 name3"""


def test_create_backup__both_disabled(tmpfile):
    hosts_editor = HostsEditor(str(tmpfile), create_backup=False)
    with pytest.raises(ValueError):
        hosts_editor.create_backup(False, False)


def test_create_backup__physical(monkeypatch, tmpfile):
    copy_mock = mock.Mock()
    monkeypatch.setattr('hostseditor.editor.copy', copy_mock)
    hosts_editor = HostsEditor(str(tmpfile), create_backup=False)
    hosts_editor.create_backup(True, False)

    assert copy_mock.called
    assert not hosts_editor._memory_backup


def test_create_backup__memory(tmpfile):
    tmpfile.write_text(TEST_HOSTS_CONTENT)
    hosts_editor = HostsEditor(str(tmpfile), False)
    hosts_editor.create_backup(False, True)

    assert hosts_editor._memory_backup is not None


@pytest.mark.parametrize(('physical_backup', 'memory_backup'), [
    (True, False),
    (False, True),
    (True, True)
])
def test_restore_backup(tmpfile, physical_backup, memory_backup):
    tmpfile.write_text(TEST_HOSTS_CONTENT)
    hosts_editor = HostsEditor(str(tmpfile), False)
    hosts_editor.create_backup(physical=physical_backup, memory=memory_backup)
    hosts_editor["test_ip"] = "test_host"

    assert hosts_editor.read_raw() != TEST_HOSTS_CONTENT

    hosts_editor.restore_backup()

    assert hosts_editor.read_raw() == TEST_HOSTS_CONTENT


def test_read__file_with_non_data_lines(tmpfile):
    """ Checks if read function returns only valid data lines. """
    tmpfile.write_text(DATA_TWO_ENTRIES_COMMENT_BLANK_LINE)
    hosts_editor = HostsEditor(str(tmpfile), create_backup=False)
    assert len(hosts_editor.read()) == 2


def test_write_entry(tmpfile):
    """Test writing an entry to the hosts file. """
    entry_ip = "1.1.1.1"
    entry_names = ["name0", "name1"]
    print(tmpfile)
    hosts_editor = HostsEditor(str(tmpfile), False)
    hosts_editor.write_entry(HostsEntry(entry_ip, entry_names))
    assert f"{entry_ip}\t{' '.join(entry_names)}" == hosts_editor.read_raw()


def test_setting_entry(tmpfile):
    """Test writing an entry to the hosts file. """
    entry_ip = "1.1.1.1"
    entry_names = ["name0", "name1"]
    print(tmpfile)
    hosts_editor = HostsEditor(str(tmpfile), False)
    hosts_editor[entry_ip] = entry_names
    assert f"{entry_ip}\t{' '.join(entry_names)}" == hosts_editor.read_raw()


def test_remove_entry_where__without_kwargs(tmpfile):
    """Suppose to remove every entry"""
    tmpfile.write_text(TEST_HOSTS_CONTENT)
    hosts_editor = HostsEditor(str(tmpfile), create_backup=False)
    hosts_editor.remove_entry_where()
    assert TEST_HOSTS_CONTENT_NO_DATA == hosts_editor.read_raw()


@pytest.mark.parametrize(('kwargs', 'expected'), [
    (dict(ip='127.0.0.1'), TEST_HOSTS_CONTENT_NO_LOCAL),
    (dict(names=['test']), TEST_HOSTS_CONTENT_NO_LOCAL),
])
def test_remove_entry_where__with_kwargs(kwargs, expected, tmpfile):
    tmpfile.write_text(TEST_HOSTS_CONTENT)
    hosts_editor = HostsEditor(str(tmpfile), False)
    hosts_editor.remove_entry_where(**kwargs)
    assert expected == hosts_editor.read_raw()
