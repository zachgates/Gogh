class StackUnderflow:

    temp = ": This operation requires at least {0} element{1} in the stack."

    def __init__(self, n):
        plural = "s" if n > 1 else ""
        self.msg = self.__class__.__name__
        self.msg += self.temp.format(n, plural)
