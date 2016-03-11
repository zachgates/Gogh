from control import Planner


class Stack(list, Planner):

    # Storage

    _dreq = "_noop"
    _req2func = {
        "NOP": "_noop",
        "EMP": "_empty",
        "POP": "_discard",
        "DUP": "_duplicate",
        "COP": "_copy",
        "SWP": "_swap",
        "ROT": "_rotate",
        "LTS": "_ltrans",
        "RTS": "_rtrans",
    }
    _req2arity = {
        "NOP": [0],
        "EMP": [0],
        "POP": [0],
        "DUP": [0],
        "COP": [0, 1],
        "SWP": [0],
        "ROT": [0],
        "LTS": [0, 1],
        "RTS": [0, 1],
    }

    # Controllers

    def __init__(self, *args):
        Planner.__init__(self)
        list.__init__(self)
        self._push(*args)

    def _push(self, *args):
        pass

    def _pull(self, n, top):
        mv = []
        for i in range(n):
            if not top:
                mv.append(list.pop(self, 0))
            else:
                mv.append(list.pop(self))
        return mv

    def _islength(self, n):
        return len(self) >= n

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
            self._pull(1, True)
        else:
            self.broadcast(3, 1)

    @Planner.toapprove
    def _duplicate(self):
        if self._islength(1):
            mv = self._pull(1, True)
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
                mv = self._pull(1, False)
                list.__iadd__(self, mv)
                n -= 1

    @Planner.toapprove
    def _rtrans(self, n=1):
        if self._islength(2):
            while n > 0:
                mv = self._pull(1, True)
                list.insert(self, 0, mv.pop())
                n -= 1
