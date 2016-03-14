import re


# Base class


class GoghObject(object):

    # Manipulators

    _prec = lambda self, i: len(str(float(i)).split(".")[1])

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
            return GoghInteger(sum(ord(c) for c in value))

    def _GoghArray__tonumber(value):
        return GoghInteger(len(value))

    # Arithmetic Operations

    def __add__(self, value):
        if value._is(GoghString):
            value = str(value)
            prec = max(map(self._prec, [self, value]))
            if value.isnumeric():
                return type(self)(round(float(self) + int(value), prec))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(round(float(self) + float(value), prec))
            else:
                return GoghString(str(self) + value)
        else:
            return GoghArray([self] + list(value))

    def __sub__(self, value):
        if value._is(GoghString):
            value = str(value)
            prec = max(map(self._prec, [self, value]))
            if value.isnumeric():
                return type(self)(round(float(self) - int(value), prec))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(round(float(self) - float(value), prec))
            else:
                return GoghString(str(self).replace(value))
        else:
            return GoghArray([self-elem for elem in list(value)])

    def __mul__(self, value):
        if value._is(GoghString):
            value = str(value)
            prec = max(map(self._prec, [self, value]))
            if value.isnumeric():
                return type(self)(round(float(self) * int(value), prec))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(round(float(self) * float(value), prec))
            else:
                return GoghString(value * int(self))
        else:
            return GoghArray([self for _ in list(value)])

    def __truediv__(self, value):
        if value._is(GoghNumber):
            retval = float(self) / float(value)
            if retval % 1:
                return GoghDecimal(retval)
            else:
                return GoghInteger(retval)
        elif value._is(GoghString):
            value = str(value)
            if value.isnumeric():
                return type(self)(float(self) / int(value))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(float(self) / float(value))
            else:
                return None
        else:
            return None


class GoghInteger(GoghNumber, int):

    # Arithmetic Operations

    def __add__(self, value):
        if value._is(GoghInteger):
            return GoghInteger(int(self) + int(value))
        elif value._is(GoghDecimal):
            prec = max(map(self._prec, [self, value]))
            return GoghDecimal(round(float(self) + float(value), prec))
        else:
            return GoghNumber.__add__(self, value)

    def __sub__(self, value):
        if value._is(GoghInteger):
            return GoghInteger(int(self) - int(value))
        elif value._is(GoghDecimal):
            prec = max(map(self._prec, [self, value]))
            return GoghDecimal(round(float(self) - float(value), prec))
        else:
            return GoghNumber.__sub__(self, value)

    def __mul__(self, value):
        if value._is(GoghInteger):
            return GoghInteger(int(self) * int(value))
        elif value._is(GoghDecimal):
            prec = max(map(self._prec, [self, value]))
            return GoghDecimal(round(float(self) * float(value), prec))
        else:
            return GoghNumber.__mul__(self, value)


class GoghDecimal(GoghNumber, float):

    # Controllers

    def __new__(cls, value):
        if value == ".":
            return float.__new__(cls, 0)
        else:
            return float.__new__(cls, value)

    # Arithmetic Operations

    def __add__(self, value):
        if value._is(GoghNumber):
            prec = max(map(self._prec, [self, value]))
            return GoghDecimal(round(float(self) + float(value), prec))
        else:
            return GoghNumber.__add__(self, value)

    def __sub__(self, value):
        if value._is(GoghNumber):
            prec = max(map(self._prec, [self, value]))
            return GoghDecimal(round(float(self) - float(value), prec))
        else:
            return GoghNumber.__sub__(self, value)

    def __mul__(self, value):
        if value._is(GoghNumber):
            prec = max(map(self._prec, [self, value]))
            return GoghDecimal(round(float(self) * float(value), prec))
        else:
            return GoghNumber.__mul__(self, value)


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
        return "".join(str(i) for i in self)

    def __repr__(self):
        elems = " ".join(repr(i) for i in self)
        return "[%s]" % elems

    def _splice(self, start, stop):
        opn = self[:start]
        cls = self[stop:]
        mid = self[start:stop]
        list.clear(self)
        list.extend(self, opn + cls)
        return mid

    # Conversions

    _tonumber = GoghNumber.__tonumber

    def _tostring(self):
        return ",".join(str(i) for i in self)

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

    def __mul__(self, value):
        if value._is(GoghNumber):
            return GoghArray([GoghArray(self) for _ in range(int(value))])
        elif value._is(GoghString):
            return GoghArray([elem*value for elem in self])
        else:
            return GoghArray([GoghArray(elem) for elem in zip(self, value)])

    def __truediv__(self, value):
        if value._is(GoghInteger):
            sp = lambda: self._splice(0, value)
            chunks = [sp() for _ in range(len(self) // int(value) + 1)]
            return GoghArray(filter(None, chunks))
        elif value._is((GoghDecimal, GoghString)):
            return GoghInteger(list.count(self, value))
        else:
            return GoghArray([GoghInteger(list.count(self, v)) for v in value])


# Strings


class GoghString(GoghArray):

    # Controllers

    def __init__(self, value):
        GoghArray.__init__(self, str(value))

    def __str__(self):
        return "".join(str(i) for i in self)

    def __repr__(self):
        return "'%s'" % "".join(str(i) for i in self)

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

    def __mul__(self, value):
        if value._is(GoghNumber):
            return GoghString(str(self) * int(value))
        elif value._is(GoghString):
            return GoghInteger(sum(map(ord, self)) + sum(map(ord, value)))
        else:
            return GoghArray([GoghString(self) for _ in value])

    def __truediv__(self, value):
        if value._is(GoghInteger):
            sp = lambda: self._splice(0, value)
            chunks = [sp() for _ in range(len(self) // int(value) + 1)]
            return GoghArray([GoghString(e) for e in filter(None, chunks)])
        elif value._is(GoghString):
            return GoghInteger(str(self).count(str(value)))
        else:
            return None
