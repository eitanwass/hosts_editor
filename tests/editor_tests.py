import shutil
from unittest import mock

import pytest


from hostseditor.editor import HostsEditor


def test_create_backup__both_disabled():
    hosts_editor = HostsEditor(create_backup=False)
    with pytest.raises(ValueError):
        hosts_editor.create_backup(False, False)


def test_create_backup__physical(monkeypatch):
    copy_mock = mock.Mock()
    monkeypatch.setattr('hostseditor.editor.copy', copy_mock)
    hosts_editor = HostsEditor(create_backup=False)
    hosts_editor.create_backup(True, False)

    assert copy_mock.called
    assert not hosts_editor.memory_backup


def test_create_backup__memory(preset_test_hosts):
    hosts_editor = HostsEditor(preset_test_hosts, False)
    hosts_editor.create_backup(False, True)

    assert hosts_editor.memory_backup is not None


def test_read__full_file():
    data = """127.0.0.1 name1
    0.0.0.0 name2 name3"""
    HostsEditor.read_raw = mock.Mock(return_value=data)
    hosts_editor = HostsEditor(create_backup=False)
    assert len(hosts_editor.read()) == 2


def test_read__file_with_blank_lines():
    data = """127.0.0.1 name1
    
    
    0.0.0.0 name2 name3"""
    HostsEditor.read_raw = mock.Mock(return_value=data)
    hosts_editor = HostsEditor(create_backup=False)
    assert len(hosts_editor.read()) == 2


def test_read_file_wtih_comments():
    data = """127.0.0.1 name1
    # Test Comment
    0.0.0.0 name2 name3"""
    HostsEditor.read_raw = mock.Mock(return_value=data)
    hosts_editor = HostsEditor(create_backup=False)
    assert len(hosts_editor.read()) == 2


def test_remove_entry_where__without_kwargs(preset_test_hosts):
    hosts_editor = HostsEditor(preset_test_hosts, False)
    hosts_editor.remove_entry_where()
    assert '' == hosts_editor.read_raw()


@pytest.mark.parametrize('kwargs', [
    dict(ip='127.0.0.1'),
    dict(names=['test']),
])
def test_remove_entry_where__with_kwargs(kwargs, preset_test_hosts):
    hosts_editor = HostsEditor(preset_test_hosts, False)
    hosts_editor.remove_entry_where(**kwargs)
    assert '' == hosts_editor.read_raw()
