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

    def request(self, action, *args):
        self._creq = self._req2func.get(action, self._dreq)
        func = eval("self." + self._creq)
        func(*args)
        return self

    def chain(self, actions, arglist=[]):
        arity = map(self._req2arity.get, actions)
        needs = zip(actions, arity)
        for req, na in needs:
            args = arglist.pop(0) if (arglist and sum(na)) else []
            if not args and (0 not in na):
                break
            else:
                self.request(req, *args)
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

    def __init__(self, endchar):
        self.end = endchar

    def broadcast(self, code, *args):
        funcname = Director.code2func.get(code)
        if funcname:
            func = eval("self." + funcname)
            func(*args)

    def _error(self, code, *args, **kwargs):
        err = Director.code2err.get(code)
        sys.stderr.write(err(*args))
        self._cleanup(err=True, **kwargs)

    def _cleanup(self, err=False, override=False):
        if not override:
            stream = sys.stderr if err else sys.stdout
            stream.write(self.end)
        sys.exit()

    # Manipulators

    def _cleanexit(self):
        self._cleanup()

    def _clierror(self):
        self._error(0, override=True)

    def _fileerror(self, path):
        self._error(1, path)

    def _underflow(self, n):
        self._error(2, n)
