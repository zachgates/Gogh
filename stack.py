from control import Planner
from gtypes import GoghString, GoghInteger, GoghDecimal, GoghArray


class Stack(list, Planner):

    # Storage

    _dreq = "_noop"
    _req2func = {
        3  : "_empty",
        5  : "_swap",
        6  : "_copy",
        8  : "_rotate",
        11 : "_duplicate",
        17 : "_discard",
        32 : "_noop",
        250: "_ltrans",
        251: "_rtrans",
    }
    _req2arity = {
        3  : [0],
        5  : [0],
        6  : [0, 1],
        8  : [0],
        11 : [0],
        17 : [0],
        32 : [0],
        250: [0, 1],
        251: [0, 1],
    }

    # Controllers

    def __init__(self, *args):
        Planner.__init__(self)
        list.__init__(self)
        self._push(*args)

    def _push(self, *args):
        for elem in args:
            if isinstance(elem, (list, tuple)):
                val = GoghArray(elem)
            elif isinstance(elem, int):
                val = GoghInteger(elem)
            elif isinstance(elem, float):
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
        return self._pull(1, True)

    @property
    def _BOS(self):
        return self._pull(1, False)

    # Manipulators

    @Planner.toapprove
    def _noop(self):
        pass

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
            list.__iadd__(self, mv + mv)
        else:
            self.broadcast(3, 1)

    @Planner.toapprove
    def _copy(self, n=0):
        if self._islength(n+1) and (n == abs(n)):
            elem = list.__getitem__(self, -n-1)
            list.append(self, elem)
        else:
            self.broadcast(3, n+1)

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
    def _ltrans(self, n=1):
        if self._islength(2):
            while n > 0:
                mv = self._BOS
                list.__iadd__(self, mv)
                n -= 1

    @Planner.toapprove
    def _rtrans(self, n=1):
        if self._islength(2):
            while n > 0:
                mv = self._TOS
                list.insert(self, 0, mv.pop())
                n -= 1
