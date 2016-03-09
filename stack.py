# Temporary function

def broadcast(msg):
    pass


class Stack(list):

    # Controllers

    reqs = {
        "NOP": "__noop",
        "EMP": "__empty",
        "POP": "__discard",
        "DUP": "__duplicate",
        "COP": "__copy",
        "SWP": "__swap",
        "ROT": "__rotate",
        "LTS": "__ltrans",
        "RTS": "__rtrans",
    }

    def __init__(self, *args):
        list.__init__(self, list(args))
        self.creq = None

    def request(self, action, *args, **kwargs):
        self.creq = Stack.reqs.get(action, "_noop")
        func = eval("self." + self.creq)
        func(*args, **kwargs)
        return self

    def toapprove(func):
        def filtered(*args, **kwargs):
            if func.__name__ == args[0].creq:
                func(*args, **kwargs)
        return filtered

    # Helpers

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

    @toapprove
    def __noop(self):
        """
        Description:
            Do nothing.
        Usage:
            () : [a b c d e] => [a b c d e]
        """
        pass

    @toapprove
    def __empty(self):
        """
        Description:
            Remove all elements.
        Usage:
            () : [a b c d e] => []
        """
        list.clear(self)

    @toapprove
    def __discard(self):
        """
        Description:
            Discard the top element.
        Usage:
            () : [a b c d e] => [a b c d]
        """
        if self._islength(1):
            self._pull(1, True)
        else:
            broadcast(0)

    @toapprove
    def __duplicate(self):
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
            broadcast(0)

    @toapprove
    def __copy(self, n=0):
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
            broadcast(0)

    @toapprove
    def __swap(self):
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
            broadcast(0)

    @toapprove
    def __rotate(self):
        """
        Description:
            Rotate the top 3 elements to the left.
        Usage:
            () : [a b c d e] => [a b d e c]
        """
        if self._islength(3):
            mv = self._pull(3, True)[::-1]
            list.__iadd__(self, Stack(mv).lshift())
        else:
            broadcast(0)

    @toapprove
    def __ltrans(self, n=1):
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

    @toapprove
    def __rtrans(self, n=1):
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
                mv = self._pull(n, True)
                self.reverse()
                list.__iadd__(self, mv)
                self.reverse()
                n -= 1

    # Cleanup

    del toapprove
