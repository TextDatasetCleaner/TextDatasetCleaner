class TDCException(Exception):
    """Base TDS Exception."""


class TDCValueError(TDCException):
    """ValueError TDC Exception."""


class TDCRuntimeError(TDCException):
    """RuntimeError TDC Exception."""


class TDCFileExistsError(TDCException):
    """FileExistsError TDC Exception."""


class TDCTypeError(TDCException):
    """TypeError TDC Exception."""


class TDCOSError(TDCException):
    """OSError TDC Exception."""


class TDCNotImplemented(TDCException):
    """NotImplemented TDC Exception."""
