from __future__ import annotations
import typing
from shutil import copy
from pathlib import Path

from hostseditor.utils import get_hosts_file_path, get_hosts_file_backup_path


COMMENT_CHAR = "#"


class HostEntry:
    def __init__(self, ip: str, names: typing.List[str]):
        self.ip = ip
        self.names = names

    @staticmethod
    def parse(line) -> typing.Union[HostEntry, None]:
        if line and not line.strip().startswith(COMMENT_CHAR):
            return HostEntry(line.split()[0], line.split()[1:])
        return None

    def has(self, **kwargs) -> bool:
        ip_filter = kwargs.get('ip')
        names_filter = kwargs.get('names')

        if ip_filter and self.ip != ip_filter:
            return False
        if names_filter and self.names != names_filter:
            return False
        return True

    def __repr__(self):
        return f"{self.ip}\t{' '.join(self.names)}"


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
        return Path(self.path).read_text()

    # TODO: Add param to parse comments as well.
    def read(self) -> typing.List[HostEntry]:
        return [HostEntry.parse(line)
                for line in self.read_raw().splitlines()
                if line.strip() and not self._is_comment(line)]

    # **** Remove **** #

    # TODO: Add function for where one of the names has to exist to delete entry

    def remove_entry_where(self, **kwargs):
        with self.path.open('r') as f:
            lines = f.readlines()

        with self.path.open('w') as f:
            for line in lines:
                if self._is_comment(line):
                    f.write(line)
                elif HostEntry.parse(line).has(**kwargs):
                    # Remove it
                    continue
                else:
                    f.write(line)

    # **** Private Utils **** #

    def _parse(self):
        pass

    @staticmethod
    def _is_comment(line):
        return line.strip().startswith(COMMENT_CHAR)
