from control import Planner
from gtypes import GoghString, GoghInteger, GoghDecimal, GoghArray
from gtypes import GoghBlock


class Stack(list, Planner):

    # Storage

    _dreq = "_noop"
    _req2func = {
        1  : "_copyn",
        3  : "_empty",
        5  : "_swap",
        6  : "_copy",
        8  : "_rotate",
        17 : "_discard",
        28 : "_duplicate",
        31 : "_collect",
        32 : "_noop",
        36 : "_revstack",
        250: "_ltrans",
        251: "_rtrans",
    }
    _req2arities = {
        1  : 1,
        6  : 1,
        250: 1,
        251: 1,
    }
    _req2argtype = {
        1  : [GoghInteger],
        6  : [GoghInteger],
        250: [GoghInteger],
        251: [GoghInteger],
    }
    _req2default = {
        1  : [1],
        6  : [0],
        250: [1],
        251: [1],
    }

    # Controllers

    def __init__(self, onstack=None):
        Planner.__init__(self)
        list.__init__(self)
        if onstack != None:
            self._push(onstack)

    def __repr__(self):
        elems = " ".join(repr(i) for i in self)
        return "[%s]" % elems

    def _push(self, *args):
        for elem in filter(lambda i: i != None, args):
            if isinstance(elem, GoghBlock):
                val = elem
            elif isinstance(elem, (str, GoghString)):
                val = GoghString(elem)
            elif isinstance(elem, (list, tuple, GoghArray)):
                val = GoghArray(elem)
            elif isinstance(elem, (int, GoghInteger)):
                val = GoghInteger(elem)
            elif isinstance(elem, (float, GoghDecimal)):
                val = GoghDecimal(elem)
            else:
                val = GoghString(elem)
            list.append(self, val)

    def _pull(self, n, top):
        return [list.pop(self, ~top+1) for i in range(n)]

    def _islength(self, n):
        return len(self) >= n

    @property
    def _TOS(self):
        return self._pull(1, True)[0]

    @property
    def _BOS(self):
        return self._pull(1, False)[0]

    # Manipulators

    @Planner.toapprove
    def _noop(self):
        pass

    @Planner.toapprove
    def _revstack(self):
        list.reverse(self)

    @Planner.toapprove
    def _empty(self):
        list.clear(self)

    @Planner.toapprove
    def _discard(self):
        if self._islength(1):
            self._TOS
        else:
            self.broadcast(3, 1)

    @Planner.toapprove
    def _duplicate(self):
        if self._islength(1):
            mv = self._TOS
            list.__iadd__(self, [mv, type(mv)(mv)])
        else:
            self.broadcast(3, 1)

    @Planner.toapprove
    def _copy(self, n):
        n = int(n)
        if self._islength(n+1):
            if n == abs(n):
                elem = list.__getitem__(self, -n-1)
                list.append(self, elem)
        else:
            self.broadcast(3, n+1)

    @Planner.toapprove
    def _copyn(self, n):
        n = int(n)
        if self._islength(n):
            if n == abs(n):
                elem = self._pull(n, True)
                list.__iadd__(self, elem)
                list.__iadd__(self, elem)
        else:
            self.broadcast(3, n)

    @Planner.toapprove
    def _swap(self):
        if self._islength(2):
            mv = self._pull(2, True)
            list.__iadd__(self, mv)
        else:
            self.broadcast(3, 2)

    @Planner.toapprove
    def _rotate(self):
        if self._islength(3):
            mv = self._pull(3, True)[::-1]
            list.__iadd__(self, mv[1:] + mv[:1])
        else:
            self.broadcast(3, 3)

    @Planner.toapprove
    def _ltrans(self, n):
        if self._islength(2):
            while n > 0:
                list.__iadd__(self, [self._BOS])
                n -= 1

    @Planner.toapprove
    def _rtrans(self, n):
        if self._islength(2):
            while n > 0:
                list.insert(self, 0, self._TOS)
                n -= 1

    @Planner.toapprove
    def _collect(self):
        retval = GoghArray(elem for elem in self)
        list.clear(self)
        list.append(self, retval)
