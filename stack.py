from control import Planner
from control import broadcast


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
        """
        Description:
            Initialize the super classes.
        Usage:
            (       ) : []
            (1, 2, 3) : [1  2  3]
        """
        Planner.__init__(self)
        list.__init__(self, list(args))

    def _pull(self, n, top):
        """
        Description:
            Take n elements from the top or bottom.
        Usage:
            (n=1 top=True ) : [a b c d e] => [e]
            (n=1 top=False) : [a b c d e] => [a]
            (n=3 top=True ) : [a b c d e] => [e d c]
            (n=3 top=False) : [a b c d e] => [a b c]
        """
        mv = []
        for i in range(n):
            if not top:
                mv.append(list.pop(self, 0))
            else:
                mv.append(list.pop(self))
        return mv

    def _islength(self, n):
        """
        Description:
            Check if the stack is at least n large.
        Usage:
            (n=1) : [a b c d e] => True
            (n=2) : [a b c d e] => True
            (n=7) : [a b c d e] => False
        """
        return len(self) >= n

    # Manipulators

    @Planner.toapprove
    def _noop(self):
        """
        Description:
            Do nothing.
        Usage:
            () : [a b c d e] => [a b c d e]
        """
        pass

    @Planner.toapprove
    def _empty(self):
        """
        Description:
            Remove all elements.
        Usage:
            () : [a b c d e] => []
        """
        list.clear(self)

    @Planner.toapprove
    def _discard(self):
        """
        Description:
            Discard the top element.
        Usage:
            () : [a b c d e] => [a b c d]
        """
        if self._islength(1):
            self._pull(1, True)
        else:
            broadcast(1, 1)

    @Planner.toapprove
    def _duplicate(self):
        """
        Description:
            Duplicate the top element.
        Usage:
            () : [a b c d e] => [a b c d e e]
        """
        if self._islength(1):
            mv = self._pull(1, True)
            list.__iadd__(self, mv + mv)
        else:
            broadcast(1, 1)

    @Planner.toapprove
    def _copy(self, n=0):
        """
        Description:
            Top element becomes the nth-from-top element.
        Usage:
            (   ) : [a b c d e] => [a b c d e]
            (n=1) : [a b c d e] => [a b c d d]
            (n=3) : [a b c d e] => [a b c d b]
        """
        if self._islength(n+1) and (n == abs(n)):
            elem = list.__getitem__(self, -n-1)
            list.append(self, elem)
        else:
            broadcast(1, n+1)

    @Planner.toapprove
    def _swap(self):
        """
        Description:
            Swap the top 2 elements.
        Usage:
            () : [a b c d e] => [a b c e d]
        """
        if self._islength(2):
            mv = self._pull(2, True)
            list.__iadd__(self, mv)
        else:
            broadcast(1, 2)

    @Planner.toapprove
    def _rotate(self):
        """
        Description:
            Rotate the top 3 elements to the left.
        Usage:
            () : [a b c d e] => [a b d e c]
        """
        if self._islength(3):
            mv = self._pull(3, True)[::-1]
            list.__iadd__(self, mv[1:] + mv[:1])
        else:
            broadcast(1, 3)

    @Planner.toapprove
    def _ltrans(self, n=1):
        """
        Description:
            Rotate the stack to the left.
        Arguments:
            n: Number of elements to rotate. Defaults to 1.
        Usage:
            (   ) : [a b c d e] => [b c d e a]
            (n=3) : [a b c d e] => [d e a b c]
        """
        if self._islength(2):
            while n > 0:
                mv = self._pull(1, False)
                list.__iadd__(self, mv)
                n -= 1

    @Planner.toapprove
    def _rtrans(self, n=1):
        """
        Description:
            Rotate the stack to the right.
        Arguments:
            n: Number of elements to rotate. Defaults to 1.
        Usage:
            (   ) : [a b c d e] => [e a b c d]
            (n=3) : [a b c d e] => [c d e a b]
        """
        if self._islength(2):
            while n > 0:
                mv = self._pull(1, True)
                list.insert(self, 0, mv.pop())
                n -= 1
