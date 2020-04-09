import logging
import socket
from .exceptions import *
from .parsers import EasyParser


class bird(object):

    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.logger = logging.getLogger(__name__)

        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(self.socket_path)
        # Read welcome
        self.socket.recv(1024)

    def _send_command(self, command):
        command = command + '\n'
        try:
            self.socket.send(command.encode())
        except BrokenPipeError:
            self.socket.connect(self.socket_path)
            self.socket.recv(1024)
            self.socket.send(command.encode())

        data = str()
        while True:
            data += self.socket.recv(1024).decode()
            if data.splitlines()[-1].startswith(('00', '80', '90')):
                break
        return data

    def show_status(self):
        command = 'show status'
        return self.command(command)

    def configure_check(self, file=None):
        command = "configure check"
        if file:
            command += f' "{file}"'
        self.command(command)
        # If the config is wrong an exception would be raised.
        return True

    def command(self, command):
        """
        Use this if you want to send a direct command.
        This will be parsed.
        :param command: str
        :return: obj
        """
        data = self._send_command(command)
        return EasyParser(data).parse()

    def raw_command(self, command, parse_basic=False):
        """
        Use this if you want to send a direct command.
        This basic parsing is optional.
        :param command: str
        :param parse_basic: bool
        :return: obj
        """
        data = self._send_command(command)

        if parse_basic:
            return EasyParser(data).objects_by_code
        return data
