from datetime import datetime, timedelta
from .exceptions import *
from .status import *
import logging
import re
import ipaddress


class EasyParser(object):
    def __init__(self, raw_data, raise_on_error_code=True):
        self.logger = logging.getLogger(__name__)
        self.objects_by_code = {}
        current_status_code = None
        for line in raw_data.splitlines():
            if not line:
                continue
            if line.startswith('+'):
                # FIXME: Add async
                self.logger.error(f"Unknown line: {line}")
                continue
            if line.startswith(' ') and current_status_code:
                # Append to previous
                self.objects_by_code[current_status_code].append(line.strip())
                continue
            else:
                status_code, message = re.split(r'[- ]', line, 1)
                status_code = int(status_code)
                if status_code in exceptions_by_code.keys() and raise_on_error_code:
                    raise exceptions_by_code[status_code](message)

                current_status_code = status_code
                self.objects_by_code[status_code] = [message.strip()]

    def parse(self):
        output = {}
        for code, data in self.objects_by_code.items():
            if code not in parsers_by_code.keys():
                continue

            parser = parsers_by_code[code](data, code)
            output[parser.name if parser.name else code] = parser.value
        return output


class BirdVersionParser(object):
    def __init__(self, data, code):
        self.name = 'bird_version'
        self.value = data[0].split()[1]


class BirdDaemonStatus(object):
    def __init__(self, data, code):
        self.name = 'daemon_status'
        self.value = BirdStatus.UNKNOWN
        data = data[0]
        if data == 'Shutdown in progress':
            self.value = BirdStatus.SHUTDOWN_IN_PROGRESS
        if data == 'Reconfiguration in progress':
            self.value = BirdStatus.RECONFIGURATION_IN_PROGRESS
        if data == 'Daemon is up and running':
            self.value = BirdStatus.DAEMON_UP_AND_RUNNING


class BirdDaemonInfo(object):
    def __init__(self, data, code):
        self.name = 'daemon_info'
        self.value = {}
        for line in data:
            if line.startswith('Router ID is'):
                self.value['router_id'] = ipaddress.ip_address(line.split()[-1])
            if line.startswith('Current server time is'):
                self.value['current_server_time'] = parse_datetime(' '.join(line.split()[-2:]))
            if line.startswith('Last reboot on'):
                self.value['daemon_boot_time'] = parse_datetime(' '.join(line.split()[-2:]))
            if line.startswith('Last reconfiguration on'):
                self.value['last_reconfiguration_time'] = parse_datetime(' '.join(line.split()[-2:]))


class BirdConfigurationOK(object):
    def __init__(self, data, code):
        self.name = "configuration_file_status"
        self.value = True


# Reconfiguration status
class BirdReconfiguration(object):
    def __init__(self, data, code):
        self.name = "reconfiguration_status"
        if code == 3:
            self.value = BirdReconfigurationStatus.RECONFIGURED
        if code == 4:
            self.value = BirdReconfigurationStatus.RECONFIGURATION_IN_PROGRESS
        if code == 5:
            self.value = BirdReconfigurationStatus.RECONFIGURATION_QUEUED
        if code == 6:
            self.value = BirdReconfigurationStatus.RECONFIGURATION_IGNORED
        if code == 17:
            self.value = BirdReconfigurationStatus.RECONFIGURATION_REMOVED_QUEUED
        if code == 18:
            self.value = BirdReconfigurationStatus.RECONFIGURATION_CONFIRMED


def parse_datetime(data):
    datetime_formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%H:%M:%S',
        '%H:%M:%S.%f'
    ]
    for datetime_format in datetime_formats:
        try:
            return datetime.strptime(data, datetime_format)
        except ValueError:
            continue
    return None


parsers_by_code = {
    3: BirdReconfiguration,
    4: BirdReconfiguration,
    5: BirdReconfiguration,
    6: BirdReconfiguration,

    13: BirdDaemonStatus,

    17: BirdReconfiguration,
    18: BirdReconfiguration,
    20: BirdConfigurationOK,
    1000: BirdVersionParser,
    1011: BirdDaemonInfo
}
