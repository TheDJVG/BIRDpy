class ParseError(Exception):
    pass


class CommandTooLong(Exception):
    pass


class InvalidSymbolType(Exception):
    pass


class ReplyTooLong(Exception):
    pass


class RouteNotFound(Exception):
    pass


class ConfigurationFileError(Exception):
    pass


class NoProtocolsMatch(Exception):
    pass


class StoppedDueToReconfiguration(Exception):
    pass


class ProtocolIsDown(Exception):
    pass


class ReloadFailed(Exception):
    pass


class AccessDenied(Exception):
    pass


class EvaluationRuntimeError(Exception):
    pass


exceptions_by_code = {
    # 8xxx Run-time error
    8000: ReplyTooLong,
    8001: RouteNotFound,
    8002: ConfigurationFileError,
    8003: NoProtocolsMatch,
    8004: StoppedDueToReconfiguration,
    8005: ProtocolIsDown,
    8006: ReloadFailed,
    8007: AccessDenied,
    8008: EvaluationRuntimeError,

    # 9xxx Parse-time error
    9000: CommandTooLong,
    9001: ParseError,
    9002: InvalidSymbolType,
}
