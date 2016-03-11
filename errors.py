class GoghError(str):

    def __new__(cls, *args):
        msg = (cls.__name__, cls.__doc__.format(*args))
        return str.__new__(cls, "%s: %s" % msg)


class CLIError(GoghError):
    """Command line arguments were not supplied correctly.\n"""


class FileError(GoghError):
    """'{0}' does not exist."""


class StackUnderflow(GoghError):
    """This operation requires at least {0} element{1} in the stack."""
