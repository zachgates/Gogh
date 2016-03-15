import sys
import errors


class Planner(object):

    # Controllers

    def __init__(self):
        self._creq = None

    def toapprove(func):
        def filtered(*args):
            if func.__name__ == args[0]._creq:
                func(*args)
        return filtered

    def request(self, action):
        self._creq = self._req2func.get(action, self._dreq)
        func = eval("self." + self._creq)
        args = self._req2arities.get(action, 0)
        argtypes = self._req2argtype.get(action, [])
        defaults = self._req2default.get(action, [])
        if self._islength(args):
            args = self._pull(args, True)[::-1]
        else:
            pos = len(self)
            args = self._pull(pos, True)[::-1]
            args += defaults[pos:]
        for i, (k, v) in enumerate(zip(args, argtypes)):
            if not isinstance(k, v):
                if defaults:
                    args[i] = defaults[i]
                else:
                    return self
        func(*args)
        return self

    def chain(self, actions):
        for act in actions:
            self.request(act)
        return self


class Director(object):

    # Storage

    code2func = {
        0: "_cleanexit",
        1: "_clierror",
        2: "_fileerror",
        3: "_underflow",
    }
    code2err = {
        0: errors.CLIError,
        1: errors.FileError,
        2: errors.StackUnderflow,
    }

    # Controllers

    def __init__(self, out, endchar):
        self.out = out
        self.end = endchar

    def broadcast(self, code, *args):
        funcname = Director.code2func.get(code)
        if funcname:
            func = eval("self." + funcname)
            func(*args)

    def _update(self, out, override=False):
        if (self.out != False) or override:
            self.out = out

    def _error(self, code, *args, **kwargs):
        err = Director.code2err.get(code)
        sys.stderr.write(err(*args))
        self._cleanup(err=True, **kwargs)

    def _cleanup(self, err=False, override=False):
        if not override:
            stream = sys.stderr if err else sys.stdout
            if not isinstance(self.out, bool) or err or override:
                stream.write(self.end)
        sys.exit()

    # Manipulators

    def _cleanexit(self):
        if not isinstance(self.out, bool):
            sys.stdout.write(self.out._output())
        self._cleanup()

    def _clierror(self):
        self._error(0, override=True)

    def _fileerror(self, path):
        self._error(1, path)

    def _underflow(self, arity):
        self._error(2, self.cchar, arity)
