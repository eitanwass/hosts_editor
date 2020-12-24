import typing
from shutil import copy
from pathlib import Path

from hostseditor.entry import HostsEntry
from hostseditor.utils import get_hosts_file_path, get_hosts_file_backup_path


class HostsEditor:
    """ An editor for hosts files. """
    def __init__(self, path: str = None, create_backup: bool = True):
        """
        Creates an editor for the hosts file.

        :param path: The path to the system's hosts file. Default None will find automatically.
        :param create_backup: Whether to backup the hosts file before any changes made. SUGGESTED.
        """
        self.path = Path(path) if path else get_hosts_file_path()
        self.path.touch(exist_ok=True)

        self.backup_path = get_hosts_file_backup_path(self.path)
        self.memory_backup = None

        if create_backup:
            self.create_backup()

    def create_backup(self, physical: bool = True, memory: bool = True):
        """
        Back up the current state of the hosts file to another file or to memory.


        :param physical: Whether to back up the file to another backup file.
        :param memory: Whether to back up the file to memory.
        :raises ValueError: If both options are disabled (because then no backup will occur).
        """
        if not physical and not memory:
            raise ValueError(f"create_backup called but both backup methods are disabled")
        if physical:
            if self.backup_path.exists():
                print(f"Overriding existing backup file at {self.backup_path}")
            copy(str(self.path), str(self.backup_path))
        if memory:
            self.memory_backup = self.read_raw()

    # **** Read **** #

    def read_raw(self) -> str:
        """
        Read the data straight from the hosts file.

        :return: The data in the hosts file as text.
        """
        return Path(self.path).read_text()

    # TODO: Add param to parse comments as well.
    def read(self) -> typing.List[HostsEntry]:
        """
        Read and parse hosts file entries.

        :return: A list of that kind of HostEntry objects representing the hosts file entries.
        """
        return [HostsEntry.parse(line)
                for line in self.read_raw().splitlines()
                if line.strip() and not HostsEntry.is_comment(line)]

    # **** Write **** #

    def write_entry(self, entry: HostsEntry):
        """
        Write an entry object to the hosts file.

        :param entry: The entry to write to the end of the file.
        """
        # TODO: Check if already exists.
        entry_str = str(entry)
        with self.path.open('a') as f:
            cur_data = self.path.read_text()
            if cur_data:
                if not self.path.read_text().endswith('\n'):
                    f.write('\n')
            f.write(entry_str)

    # **** Remove **** #

    # TODO: Add function for where one of the names has to exist to delete entry

    def remove_entry_where(self, ip: str = None, names: typing.Union[str, typing.List[str]] = None) -> None:
        """
        Remove an entry where these attributes apply completely (not partially).

        :param ip: The IP of the entry to delete.
        :param names: The names of the entry to delete.
        """
        # TODO: Return bool based on success of deleting (say, if entry does not exist return False).
        lines = self.read_raw().splitlines()

        lines = [line for line in lines
                 if HostsEntry.is_comment(line) or not line.strip() or not HostsEntry.parse(line).has(ip=ip, names=names)]

        with self.path.open('w') as f:
            f.write('\n'.join(lines))
