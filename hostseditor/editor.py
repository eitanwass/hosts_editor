import typing
from shutil import copy
from pathlib import Path

from hostseditor.entry import HostEntry
from hostseditor.utils import get_hosts_file_path, get_hosts_file_backup_path


class HostsEditor:
    def __init__(self, path: str = None, create_backup: bool = True):
        self.path = Path(path) if path else get_hosts_file_path()
        self.backup_path = get_hosts_file_backup_path(self.path)
        self.memory_backup = None

        if create_backup:
            self.create_backup()

    def create_backup(self, physical: bool = True, memory: bool = True):
        if not physical and not memory:
            raise ValueError(f"create_backup called but both backup methods are disabled")
        if physical:
            copy(str(self.path), str(self.backup_path))
        if memory:
            self.memory_backup = self.read_raw()

    # **** Read **** #

    def read_raw(self):
        # TODO: Don't assume correct path. Check if file exists first
        return Path(self.path).read_text()

    # TODO: Add param to parse comments as well.
    def read(self) -> typing.List[HostEntry]:
        return [HostEntry.parse(line)
                for line in self.read_raw().splitlines()
                if line.strip() and not HostEntry.is_comment(line)]

    # **** Remove **** #

    # TODO: Add function for where one of the names has to exist to delete entry

    def remove_entry_where(self, **kwargs):
        lines = self.read_raw().splitlines()

        lines = [line for line in lines
                 if HostEntry.is_comment(line) or not line.strip() or not HostEntry.parse(line).has(**kwargs)]

        with self.path.open('w') as f:
            f.write('\n'.join(lines))
