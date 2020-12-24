import typing
from time import time as cur_time
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

        self._backup_path = get_hosts_file_backup_path(self.path)
        self._memory_backup = None

        self._last_physical_backup = 0
        self._last_memory_backup = 0

        if create_backup:
            self.create_backup()

    # **** Backup **** #

    def create_backup(self, physical: bool = True, memory: bool = True):
        """
        Back up the current state of the hosts file to another file or to memory.

        :param physical: Whether to back up the file to another backup file.
        :param memory: Whether to back up the file to memory.
        :raises ValueError: If both options are disabled (because then no backup will occur).
        """
        if not physical and not memory:
            raise ValueError(f"create_backup called but both backup methods are disabled")
        if memory:
            self._memory_backup = self.read_raw()
            self._last_memory_backup = cur_time()
        if physical:
            if self._backup_path.exists():
                print(f"Overriding existing backup file at {self._backup_path}")
            copy(str(self.path), str(self._backup_path))
            self._last_physical_backup = cur_time()

    def restore_backup(self) -> None:
        """
        Restore the newest backup to the original file.
        If both physical and memory backups are at the same time, will prefer memory.
        """
        latest_backup = self._memory_backup \
            if self._last_memory_backup >= self._last_physical_backup \
            else self._backup_path.read_text()
        self.path.write_text(latest_backup)

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

    def write_entry(self, entry: HostsEntry) -> None:
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

    def __setitem__(self, ip: str, names: typing.Union[str, typing.List[str]]) -> None:
        """
        Write an entry through the use of item assignments:
        E.g. hosts_editor["127.0.0.1"] = "www.mysite.com"
        or for multiple names:
        hosts_editor["127.0.0.1"] = ["host_name0", "host_name1", ...]

        :param ip: The ip of the entry.
        :param names: The names of the hosts assigned to that IP.
        """
        self.write_entry(HostsEntry(ip, names))

    # **** Remove **** #

    # TODO: Add function for where one of the names has to exist to delete entry

    def remove_entry_where(self, ip: str = None, names: typing.Union[str, typing.List[str]] = None) -> bool:
        """
        Remove an entry where these attributes apply completely (not partially).

        :param ip: The IP of the entry to delete.
        :param names: The names of the entry to delete.
        :return: Whether a line was removed.
        """
        lines = self.read_raw().splitlines()

        data_lines = [line for line in lines
                      if HostsEntry.is_comment(line) or
                      not line.strip() or
                      not HostsEntry.parse(line).has(ip=ip, names=names)]

        with self.path.open('w') as f:
            f.write('\n'.join(data_lines))

        new_lines = self.read_raw().splitlines()

        return new_lines != lines
