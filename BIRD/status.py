from enum import Enum, auto


class BirdStatus(Enum):
    SHUTDOWN_IN_PROGRESS = auto()
    RECONFIGURATION_IN_PROGRESS = auto()
    DAEMON_UP_AND_RUNNING = auto()
    UNKNOWN = auto()


class BirdReconfigurationStatus(Enum):
    RECONFIGURED = auto()
    RECONFIGURATION_IN_PROGRESS = auto()
    RECONFIGURATION_QUEUED = auto()
    RECONFIGURATION_IGNORED = auto()
    RECONFIGURATION_REMOVED_QUEUED = auto()
    RECONFIGURATION_CONFIRMED = auto()
