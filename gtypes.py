import re
import string
from functools import reduce


code_page  = """¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶"""
code_page += """°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”"""


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
        """To be written in the subclass."""
        return self

    def _tostring(self):
        return GoghString(self)

    # Arithmetic Operations

    def __add__(self, value):
        """To be written in the subclass."""
        return self

    def __sub__(self, value):
        """To be written in the subclass."""
        return self

    def __mul__(self, value):
        """To be written in the subclass."""
        return self

    def __truediv__(self, value):
        """To be written in the subclass."""
        return self

    def __mod__(self, value):
        """To be written in the subclass."""
        return self

    def __neg__(self):
        """To be written in the subclass."""
        return self

    def __pow__(self, value):
        """To be written in the subclass."""
        return self

    def __gt__(self, value):
        """To be written in the subclass."""
        return True

    def __lt__(self, value):
        """To be written in the subclass."""
        return True

    def split(self, value):
        """To be written in the subclass."""
        return self

    def join(self, value):
        """To be written in the subclass."""
        return self


# Numbers (Integers & Decimals)


class GoghNumber(GoghObject):

    # Controllers

    def __bool__(self):
        if self != 0:
            return True
        return False

    # Conversions

    def _tonumber(self):
        return self

    def _GoghString__tonumber(value):
        value = str(value)
        isnum = all(e in string.digits for e in value)
        if re.match("(\d+)?\.(\d+)?", value):
            return GoghDecimal(value)
        elif isnum:
            return GoghInteger(value)
        else:
            return GoghInteger(sum(ord(c) for c in value))

    def _GoghArray__tonumber(value):
        return GoghInteger(len(value))

    def _GoghBlock__tonumber(value):
        return GoghInteger(len(value))

    # Arithmetic Operations

    def __add__(self, value):
        if value._is(GoghString):
            value = str(value)
            isnum = all(e in string.digits for e in value)
            prec = max(map(self._prec, [self, value]))
            if isnum:
                return type(self)(round(float(self) + int(value), prec))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(round(float(self) + float(value), prec))
            else:
                return GoghString(str(self) + value)
        elif value._is(GoghArray):
            return GoghArray([self] + list(value))
        else:
            return self

    def __sub__(self, value):
        if value._is(GoghString):
            value = str(value)
            isnum = all(e in string.digits for e in value)
            prec = max(map(self._prec, [self, value]))
            if isnum:
                return type(self)(round(float(self) - int(value), prec))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(round(float(self) - float(value), prec))
            else:
                return GoghString(str(self).replace(value))
        elif value._is(GoghArray):
            return GoghArray([self-elem for elem in list(value)])
        else:
            return self

    def __mul__(self, value):
        if value._is(GoghString):
            value = str(value)
            isnum = all(e in string.digits for e in value)
            prec = max(map(self._prec, [self, value]))
            if isnum:
                return type(self)(round(float(self) * int(value), prec))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(round(float(self) * float(value), prec))
            else:
                return GoghString(value * int(self))
        elif value._is(GoghArray):
            return GoghArray([self for _ in list(value)])
        else:
            return self

    def __truediv__(self, value):
        if value._is(GoghNumber):
            retval = float(self) / float(value)
            prec = max(map(self._prec, [self, value]))
            if retval % 1:
                return GoghDecimal(round(retval, prec))
            else:
                return GoghInteger(retval)
        elif value._is(GoghString):
            value = str(value)
            isnum = all(e in string.digits for e in value)
            if isnum:
                return type(self)(float(self) / int(value))
            elif re.match("(\d+)?\.(\d+)?", value):
                value = 0 if value == "." else value
                return type(self)(float(self) / float(value))
            else:
                return self
        else:
            return self

    def __mod__(self, value):
        if value._is(GoghNumber):
            retval = float(self) % float(value)
            prec = max(map(self._prec, [self, value]))
            if retval % 1:
                return GoghDecimal(round(retval, prec))
            else:
                return GoghInteger(retval)
        else:
            return self

    def split(self, value):
        if value._is(GoghNumber):
            mid = (float(self) + float(value)) / 2
            if mid % 1:
                return GoghDecimal(mid)
            else:
                return GoghInteger(mid)
        else:
            return self


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

    def __neg__(self):
        return int.__neg__(self)

    def __pow__(self, value):
        return int.__pow__(self, value)

    def __gt__(self, value):
        if value._is(GoghNumber):
            return bool(int.__gt__(self, value))
        elif value._is(GoghArray):
            value = len(value)
            return bool(int.__gt__(self, value))
        else:
            return bool(self)

    def __lt__(self, value):
        if value._is(GoghNumber):
            return bool(int.__lt__(self, value))
        elif value._is(GoghArray):
            value = len(value)
            return bool(int.__lt__(self, value))
        else:
            return (not bool(self))


class GoghDecimal(GoghNumber, float):

    # Controllers

    def __new__(cls, value):
        if value == ".":
            return float.__new__(cls, 0)
        else:
            return float.__new__(cls, value)

    def __repr__(self):
        fstr = ("%f" % float(self)).rstrip("0")
        if fstr.endswith("."):
            fstr += "0"
        return fstr

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

    def __neg__(self):
        return float.__neg__(self)

    def __pow__(self, value):
        return float.__pow__(self, value)

    def __gt__(self, value):
        if value._is(GoghNumber):
            return bool(float.__gt__(self, value))
        elif value._is(GoghArray):
            value = len(value)
            return bool(float.__gt__(self, value))
        else:
            return bool(self)

    def __lt__(self, value):
        if value._is(GoghNumber):
            return bool(float.__lt__(self, value))
        elif value._is(GoghArray):
            value = len(value)
            return bool(float.__lt__(self, value))
        else:
            return (not bool(self))


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
        elif isinstance(value, GoghBlock):
            list.__init__(self, GoghBlock)
        else:
            list.__init__(self, value)

    def __str__(self):
        return "".join(str(i) for i in self)

    def __repr__(self):
        elems = " ".join(repr(i) for i in self)
        return "[%s]" % elems

    def __bool__(self):
        if len(self):
            return True
        return False

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
        return GoghString(",".join(str(i) for i in self))

    # Arithmetic Operations

    def __add__(self, value):
        if value._is((GoghNumber, GoghString, GoghBlock)):
            list.append(self, value)
            return self
        else:
            return GoghArray(list(self) + list(value))

    def __sub__(self, value):
        list.reverse(self)
        if value._is((GoghNumber, GoghString, GoghBlock)):
            list.remove(self, value)
        else:
            for elem in value:
                list.remove(self, value)
        list.reverse(self)
        return self

    def __mul__(self, value):
        if value._is(GoghNumber) and value >= 1:
            return GoghArray([GoghArray(self) for _ in range(int(value))])
        elif value._is(GoghString):
            return GoghArray([elem*value for elem in self])
        elif value._is(GoghArray):
            return GoghArray([GoghArray(elem) for elem in zip(self, value)])
        else:
            return GoghArray([value for elem in self])

    def __truediv__(self, value):
        if value._is(GoghInteger) and value >= 1:
            sp = lambda: self._splice(0, value)
            chunks = [sp() for _ in range(len(self) // int(value) + 1)]
            return GoghArray(filter(None, chunks))
        elif value._is((GoghDecimal, GoghString, GoghBlock)):
            return GoghInteger(list.count(self, value))
        else:
            return GoghArray([GoghInteger(list.count(self, v)) for v in value])

    def __mod__(self, value):
        if value._is((GoghNumber, GoghString, GoghBlock)):
            return GoghArray([elem for elem in list(self) if elem != value])
        else:
            return GoghArray([elem for elem in list(self) if elem not in value])

    def __neg__(self):
        list.reverse(self)
        return self

    def __pow__(self, value):
        if value >= 2:
            return GoghArray(sum(zip(*[self]*value), ()))
        return self

    def __gt__(self, value):
        if value._is(GoghNumber):
            return bool(len(self) > value)
        elif value._is(GoghArray):
            return bool(len(self) > len(value))
        else:
            return False

    def __lt__(self, value):
        if value._is(GoghNumber):
            return bool(len(self) < value)
        elif value._is(GoghArray):
            return bool(len(self) < len(value))
        else:
            return True

    def split(self, value):
        retval = GoghArray([])
        temp = GoghArray([])
        for elem in self:
            if elem == value:
                retval.append(temp)
                temp = GoghArray([])
            else:
                temp.append(elem)
        return retval

    def join(self, value):
        if value._is(GoghBlock):
            value = "".join(repr(e) for e in value)
        retval = str(value).join(str(i) for i in self)
        return GoghString(retval)


# Strings


class GoghString(GoghArray):

    # Controllers

    def __init__(self, value):
        GoghArray.__init__(self, str(value))

    def __str__(self):
        return "".join(str(i) for i in self)

    def __repr__(self):
        return '"%s"' % "".join(str(i) if i != "\n" else "\\n" for i in self)

    def __bool__(self):
        if len(self):
            return True
        return False

    # Output

    def _output(self):
        return str(self)

    # Conversions

    _tonumber = GoghNumber.__tonumber

    def _tostring(self):
        return GoghString(str(self))

    # Arithmetic Operations

    def __add__(self, value):
        return GoghString(str(self) + str(value))

    def __sub__(self, value):
        if value._is((GoghNumber, GoghString)):
            return GoghString(str(self).replace(str(value), "", 1))
        elif value._is(GoghArray):
            return GoghArray([self-elem for elem in list(value)])
        else:
            return GoghString(self - value._tostring())

    def __mul__(self, value):
        if value._is(GoghNumber) and value >= 1:
                return GoghString(str(self) * int(value))
        elif value._is(GoghString):
            x, y = list(self), list(value)
            x, y = min(x, y), max(x, y)
            x += ["\x01"] * (len(y) - len(x))
            inter = zip(map(ord, x), map(ord, y))
            leave = map(lambda a: a[0] * a[1], inter)
            return GoghArray([GoghInteger(e) for e in leave])
        elif value._is(GoghArray):
            return GoghArray([GoghString(self) for _ in value])
        return self

    def __truediv__(self, value):
        if value._is(GoghInteger) and value >= 1:
            sp = lambda: self._splice(0, value)
            chunks = [sp() for _ in range(len(self) // int(value) + 1)]
            return GoghArray([GoghString(e) for e in filter(None, chunks)])
        elif value._is(GoghString):
            return GoghInteger(str(self).count(str(value)))
        else:
            return self

    def __mod__(self, value):
        if value._is((GoghNumber, GoghString)):
            s = str(self)[::-1]
            return GoghString(s.replace(str(value), "")[::-1])
        elif value._is(GoghArray):
            return GoghArray([self%elem for elem in list(value)])
        else:
            return self

    def __pow__(self, value):
        if value >= 1:
            return GoghArray(map(lambda i: ord(i) ** value, self))
        else:
            return self

    def split(self, value):
        if value._is((GoghNumber, GoghString)):
            retval = str(self).split(str(value))
            retval = [GoghString(elem) for elem in retval]
            return retval
        else:
            return self


# Code Blocks


class Frame(int):

    def __str__(self):
        return code_page[self]

    def __repr__(self):
        return code_page[self]


class GoghBlock(list, GoghObject):

    # Controllers

    def __init__(self, code):
        list.__init__(self, self._build(code))

    def __str__(self):
        return "".join(str(i) for i in self)

    def __repr__(self):
        return "{%s}" % "".join(repr(elem) for elem in self)

    def __bool__(self):
        if len(self):
            return True
        return False

    def _build(self, code):
        blocks = re.findall('"[^"]+"|[0-9.]+|{[^}]+}|.', code)
        for elem in blocks:
            isnum = all(e in string.digits for e in elem)
            if code_page.find(elem[0]) == 34:
                yield GoghString(eval(elem))
            elif isnum:
                yield GoghInteger(eval(elem))
            elif re.match("(\d+)?\.([\d.]+)?", elem):
                elem = elem.split(".", 1)
                elem[1] = elem[1].replace(".", "0")
                yield GoghDecimal(".".join(elem))
            elif code_page.find(elem[0]) == 123:
                yield GoghBlock(elem[1:-1])
            else:
                yield Frame(code_page.index(elem) if elem != "\n" else 32)

    # Conversions

    _tonumber = GoghNumber.__tonumber

    def _tostring(self):
        return GoghString(str(self))

    # Arithmetic Operations

    def __add__(self, value):
        if value._is((GoghNumber, GoghString, GoghArray)):
            list.append(self, value)
        else:
            list.__iadd__(self, value)
        return self

    def __mul__(self, value):
        if value._is(GoghInteger) and value >= 1:
            list.__imul__(self, value)
        return self

    def __neg__(self):
        list.append(self, Frame(94))
        return self

    def __gt__(self, value):
        if value._is(GoghNumber):
            return (not bool(value))
        return True

    def __lt__(self, value):
        if value._is(GoghNumber):
            return bool(self)
        return False
