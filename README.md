# hosts_editor

An API for editing `hosts` file.\
Exposes API for:
- Adding entries.
- Selectively remove entries by attributes.
- Reading entries.
- Backup / Restore.

Supports Windows and Linux.\
Should support both x86 and x64 systems (Tested only on x64 systems though).\
Tested on: Windows 10 x64, Linux Ubuntu 20 x64

examples: 
```
import hostseditor # pip install hosts_editor
hosts = hostseditor.HostsEditor(create_backup=False)
print( list(hosts.read()) )
hosts.write_entry( hostseditor.HostsEntry('127.0.0.1', ['qwer.local', 'qwer2.local']) ) # add
hosts.write_entry( hostseditor.HostsEntry('127.0.0.1', ['asd.local']) )
print( list(hosts.read()) )
hosts.remove_entry_where(names=['qwer.local', 'qwer2.local']) # remove
hosts.remove_entry_where(names=['asd.local'])
```
