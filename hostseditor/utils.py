import os
import typing
from pathlib import Path


def _get_common_hosts_file_dir() -> Path:
    return Path(os.environ['DRIVERDATA']).parent / 'etc'


def get_hosts_file_path() -> Path:
    return _get_common_hosts_file_dir() / 'hosts'


def get_hosts_file_backup_path(hosts_file_path: str) -> Path:
    return Path(hosts_file_path).parent / 'hosts_backup'
