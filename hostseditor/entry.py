from __future__ import annotations
import typing

COMMENT_CHAR = "#"


class HostsEntry:
    """ An object representing an entry in the relevant hosts file. """
    def __init__(self, ip: str, names: typing.Union[str, typing.List[str]]):
        """
        An object representing an entry in the relevant hosts file.

        :param ip: The ip of the entry.
        :param names: The names of the hosts that this IP relates to.
        """
        self.ip = ip
        self.names = names

    @staticmethod
    def parse(line: str) -> HostsEntry:
        """
        Parse a line into an HostEntry object.

        :param line: The line in the hosts file.
        :return: The HostEntry object with the attributes of that line.
        """
        line_parts = line.split()
        return HostsEntry(line_parts[0], line_parts[1:])

    def has(self, ip: str = None, names: typing.Union[str, typing.List[str]] = None) -> bool:
        """
        Does the entry have the attributes provided.
        Acceptable attributes keys are: ip, names.

        :param ip: The IP to check if the object has.
        :param names: The names to check if the object has.
        :return: Whether the object has the provided attributes.
        """

        if ip and self.ip != ip:
            return False
        if names and self.names != names:
            return False
        return True

    @staticmethod
    def is_comment(line):
        """ Whether the provided line is a comment. """
        return line.strip().startswith(COMMENT_CHAR)

    def __repr__(self):
        """ Print the object nicely as it would in the hosts file. """
        return f"{self.ip}\t{' '.join(self.names)}"
