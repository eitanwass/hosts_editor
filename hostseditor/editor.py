import typing
from shutil import copy
from pathlib import Path

from hostseditor.utils import get_hosts_file_path, get_hosts_file_backup_path


COMMENT_CHAR = "#"


class HostEntry:
    def __init__(self, ip: str, names: typing.List[str]):
        self.ip = ip
        self.names = names


class HostsEditor:
    def __init__(self, path: str = None, create_backup: bool = True):
        self.path = path or get_hosts_file_path()
        self.backup = None

        if create_backup:
            self.create_backup()

    def create_backup(self, physical: bool = True, memory: bool = True):
        if not physical and not memory:
            print(f"create_backup called but both backup methods are disabled")
        if physical:
            copy(str(self.path), str(get_hosts_file_backup_path()))
        if memory:
            self.backup = self.read_raw()

    def read_raw(self):
        return Path(self.path).read_text()

    # TODO: Add param to parse comments as well.
    def read(self) -> typing.List[HostEntry]:
        return [HostEntry(line.split()[0], line.split()[1:])
                for line in self.read_raw().splitlines()
                if line and not line.strip().startswith(COMMENT_CHAR)]
