import re


# Base class


class GoghObject(object):

    # Manipulators

    def _is(self, cls):
        return isinstance(self, cls)

    # Output

    def _output(self):
        return repr(self)

    # Conversions

    def _toarray(self):
        return GoghArray(self)

    def _tonumber(self):
        """To be written in the superclass."""
        return NotImplemented

    def _tostring(self):
        return GoghString(self)

    # Arithmetic Operations

    def __add__(self, value):
        """To be written in the superclass."""
        return NotImplemented

    def __sub__(self, value):
        """To be written in the superclass."""
        return NotImplemented

    def __mul__(self, value):
        """To be written in the superclass."""
        return NotImplemented

    def __truediv__(self, value):
        """To be written in the superclass."""
        return NotImplemented

    def __floordiv__(self, value):
        return self.__truediv__(value) // 1


# Numbers (Integers & Decimals)


class GoghNumber(GoghObject):

    # Conversions

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

    # Arithmetic Operations

    def __add__(self, value):
        if self._is(GoghInteger):
            if value._is(GoghInteger):
                return GoghInteger(int(self) + int(value))
            elif value._is(GoghDecimal):
                return GoghDecimal(float(self) + float(value))
        else:
            if value._is(GoghNumber):
                return GoghDecimal(float(self) + float(value))
        if value._is(GoghString):
            value = str(value)
            if value.isnumeric():
                return type(self)(float(self) + int(value))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(float(self) + float(value))
            else:
                return GoghString(str(self) + value)
        else:
            return GoghArray([self] + list(value))

    def __sub__(self, value):
        if self._is(GoghInteger):
            if value._is(GoghInteger):
                return GoghInteger(int(self) - int(value))
            elif value._is(GoghDecimal):
                return GoghDecimal(float(self) - float(value))
        else:
            if value._is(GoghNumber):
                return GoghDecimal(float(self) - float(value))
        if value._is(GoghString):
            value = str(value)
            if value.isnumeric():
                return type(self)(float(self) - int(value))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(float(self) - float(value))
            else:
                return GoghString(str(self).replace(value))
        else:
            return GoghArray([self-elem for elem in list(value)])


class GoghInteger(GoghNumber, int):
    pass


class GoghDecimal(GoghNumber, float):

    # Controllers

    def __new__(cls, value):
        if value == ".":
            return float.__new__(cls, 0)
        else:
            return float.__new__(cls, value)


# Lists


class GoghArray(list, GoghObject):

    # Controllers

    def __init__(self, value):
        if isinstance(value, GoghInteger):
            rng = range(int(value))
            list.__init__(self, map(GoghInteger, rng))
        elif isinstance(value, GoghDecimal):
            list.__init__(self)
        elif isinstance(value, GoghString):
            list.__init__(self, [GoghString(elem) for elem in str(value)])
        else:
            list.__init__(self, value)

    def __str__(self):
        return ",".join(str(i) for i in self)

    def __repr__(self):
        elems = " ".join(repr(i) for i in self)
        return "[%s]" % elems

    # Conversions

    _tonumber = GoghNumber.__tonumber

    # Arithmetic Operations

    def __add__(self, value):
        if value._is((GoghNumber, GoghString)):
            list.append(self, value)
            return self
        else:
            return GoghArray(list(self) + list(value))

    def __sub__(self, value):
        if value._is((GoghNumber, GoghString)):
            return GoghArray([elem for elem in list(self) if elem != value])
        else:
            return GoghArray([elem for elem in list(self) if elem not in value])


# Strings


class GoghString(GoghArray):

    # Controllers

    def __init__(self, value):
        GoghArray.__init__(self, str(value))

    def __str__(self):
        return "".join(str(i) for i in self)

    def __repr__(self):
        return "".join(str(i) for i in self)

    # Conversions

    _tonumber = GoghNumber.__tonumber

    # Arithmetic Operations

    def __add__(self, value):
        if value._is((GoghNumber, GoghString)):
            retval = str(self) + str(value)
        else:
            retval = str(self) + "".join(str(i) for i in value)
        return GoghString(retval)

    def __sub__(self, value):
        if value._is((GoghNumber, GoghString)):
            return GoghString(str(self).replace(str(value), ""))
        else:
            return GoghArray([self-elem for elem in list(value)])
