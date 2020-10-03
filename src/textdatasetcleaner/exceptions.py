class TDSException(Exception):
    pass


class TDSValueError(TDSException):
    pass


class TDSRuntimeError(TDSException):
    pass


class TDSFileExistsError(TDSException):
    pass


class TDSTypeError(TDSException):
    pass


class TDSOSError(TDSException):
    pass


class TDSNotImplemented(TDSException):
    pass
