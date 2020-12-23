from __future__ import annotations
import typing

COMMENT_CHAR = "#"


class HostEntry:
    def __init__(self, ip: str, names: typing.List[str]):
        self.ip = ip
        self.names = names

    @staticmethod
    def parse(line: str) -> typing.Union[HostEntry]:
        line_parts = line.split()
        return HostEntry(line_parts[0], line_parts[1:])

    def has(self, **kwargs) -> bool:
        ip_filter = kwargs.get('ip')
        names_filter = kwargs.get('names')

        if ip_filter and self.ip != ip_filter:
            return False
        if names_filter and self.names != names_filter:
            return False
        return True

    @staticmethod
    def is_comment(line):
        return line.strip().startswith(COMMENT_CHAR)

    def __repr__(self):
        return f"{self.ip}\t{' '.join(self.names)}"
