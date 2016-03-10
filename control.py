import sys
import errors


global ctrl
global broadcast


class Director(object):

    # Storage

    code2func = {
        0: "_cleanexit",
        1: "_underflow",
    }

    # Controllers

    def broadcast(self, code, *args):
        func_name = Director.code2func.get(code)
        if func_name:
            func = eval("self." + func_name)
            func(*args)

    # Manipulators

    def _cleanexit(self):
        sys.exit()

    def _underflow(self, n):
        sys.stderr.write(errors.StackUnderflow(n).msg)
        sys.exit()


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


ctrl = Director()
broadcast = ctrl.broadcast
