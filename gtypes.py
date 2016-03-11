import re


# Base class


class GoghObject(object):

    def _tonumber(self):
        """To be written in the superclass."""
        return NotImplemented

    def _toarray(self):
        return GoghArray(self)

    def _tostring(self):
        return GoghString(self)

    def _output(self):
        return repr(self)


# Numbers (Integers & Decimals)


class GoghNumber(GoghObject):

    def _tonumber(self):
        return self

    def _GoghString__tonumber(value):
        value = str(value)
        if re.match("(\d+)?\.(\d+)?", value):
            return GoghDecimal(value)
        elif value.isnumeric():
            return GoghInteger(value)
        else:
            return GoghInteger(len(value))

    def _GoghArray__tonumber(value):
        return GoghInteger(len(value))


class GoghInteger(int, GoghNumber):
    pass


class GoghDecimal(float, GoghNumber):

    def __new__(cls, value):
        if value == ".":
            return float.__new__(cls, 0)
        else:
            return float.__new__(cls, value)


# Lists


class GoghArray(list, GoghObject):

    _tonumber = GoghNumber.__tonumber

    def __init__(self, value):
        if isinstance(value, GoghInteger):
            list.__init__(self, range(value))
        elif isinstance(value, GoghDecimal):
            list.__init__(self)
        else:
            list.__init__(self, value)

    def __str__(self):
        return ",".join(str(i) for i in self)

    def __repr__(self):
        elems = " ".join(repr(i) for i in self)
        return "[%s]" % elems


# Strings


class GoghString(GoghArray):

    _tonumber = GoghNumber.__tonumber

    def __init__(self, value):
        GoghArray.__init__(self, str(value))

    def __str__(self):
        return "".join(str(i) for i in self)

    def __repr__(self):
        return "".join(str(i) for i in self)

    def _output(self):
        return str(self)
