class GoghError(str):

    def __new__(cls, *args):
        msg = (cls.__name__, cls.__doc__.format(*args))
        return str.__new__(cls, "%s: %s" % msg)


class CLIError(GoghError):
    """Command line arguments were not supplied correctly.\n"""


class FileError(GoghError):
    """'{0}' does not exist."""


class StackUnderflow(GoghError):
    """The operation {0} requires at least {1} element{2} in the stack."""

    def __new__(cls, char, arity):
        return GoghError.__new__(cls, char, arity, "s" if arity > 1 else "")
