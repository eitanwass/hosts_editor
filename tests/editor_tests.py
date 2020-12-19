import pytest


from hostseditor.editor import HostsEditor


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
