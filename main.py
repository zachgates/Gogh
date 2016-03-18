import re
import sys
import string
from stack import Stack
from control import Director, Planner
from gtypes import GoghObject, GoghNumber
from gtypes import GoghString, GoghInteger, GoghDecimal, GoghArray
from gtypes import GoghBlock, Frame


code_page  = """¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶"""
code_page += """°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”"""


class Gogh(Director, Stack):

    # Storage

    _dreq = "_noop"
    _req2func = {
        0  : "_output",
        11 : "_keepif_destruct",
        13 : "_any",
        22 : "_all",
        33 : "_lognot",
        37 : "_modulo",
        39 : "_out_top",
        42 : "_multiply",
        43 : "_add",
        45 : "_subtract",
        47 : "_divide",
        58 : "_if_execute",
        60 : "_lessthan",
        61 : "_equals",
        62 : "_greaterthan",
        63 : "_keepif_construct",
        64 : "_ifelse_execute",
        68 : "_dump",
        70 : "_fibonacci",
        74 : "_join",
        81 : "_nth_sequence",
        82 : "_reverse_top",
        83 : "_split",
        94 : "_negate",
        97 : "_toarray",
        109: "_map",
        110: "_tonumber",
        112: "_power",
        114: "_root",
        115: "_tostring",
        120: "_execute",
        128: "_twofalse",
        129: "_twotrue",
        130: "_square",
        131: "_cube",
        151: "_print_top",
        247: "_exec_off_stack",
    }
    _req2arities = {
        0  : 1,
        11 : 2,
        13 : 1,
        22 : 1,
        33 : 1,
        37 : 2,
        39 : 1,
        42 : 2,
        43 : 2,
        45 : 2,
        47 : 2,
        58 : 2,
        60 : 2,
        61 : 2,
        62 : 2,
        63 : 2,
        64 : 3,
        68 : 1,
        70 : 1,
        74 : 2,
        81 : 2,
        82 : 1,
        83 : 2,
        94 : 1,
        97 : 1,
        109: 2,
        110: 1,
        112: 2,
        114: 2,
        115: 1,
        120: 1,
        130: 1,
        131: 1,
        151: 1,
        247: 2,
    }
    _req2argtype = {
        0  : [GoghObject],
        11 : [GoghObject, GoghObject],
        13 : [GoghObject],
        22 : [GoghObject],
        33 : [GoghObject],
        37 : [GoghObject, GoghObject],
        39 : [GoghObject],
        42 : [GoghObject, GoghObject],
        43 : [GoghObject, GoghObject],
        45 : [GoghObject, GoghObject],
        47 : [GoghObject, GoghObject],
        58 : [GoghBlock, GoghObject],
        60 : [GoghObject, GoghObject],
        61 : [GoghObject, GoghObject],
        62 : [GoghObject, GoghObject],
        63 : [GoghObject, GoghObject],
        64 : [GoghBlock, GoghBlock, GoghObject],
        68 : [GoghObject],
        70 : [GoghObject],
        74 : [GoghObject, GoghObject],
        81 : [GoghInteger, GoghBlock],
        82 : [GoghObject],
        83 : [GoghObject, GoghObject],
        94 : [GoghObject],
        97 : [GoghObject],
        109: [GoghObject, GoghBlock],
        110: [GoghObject],
        112: [GoghObject, GoghNumber],
        114: [GoghObject, GoghNumber],
        115: [GoghObject],
        120: [GoghBlock],
        130: [GoghObject],
        131: [GoghObject],
        151: [GoghObject],
        247: [GoghObject, GoghBlock],
    }
    _req2default = {
        74 : [NotImplemented, GoghString("")],
        112: [NotImplemented, GoghInteger(2)],
        114: [NotImplemented, GoghInteger(2)],
    }

    _req2func.update(Stack._req2func)
    _req2arities.update(Stack._req2arities)
    _req2argtype.update(Stack._req2argtype)
    _req2default.update(Stack._req2default)

    # Controllers

    def __init__(self, code, ip, out, err, endchar, wantexit=True):
        Director.__init__(self, out, endchar)
        Stack.__init__(self, ip)
        if err != None:
            self.broadcast(*err)
        self.cchar = None
        self.intreg = None
        self.strreg = None
        self.strlit = False
        self._pre(code)
        if wantexit:
            self._exit(0)

    def _tokenize(self, code):
        blocks = re.findall('"[^"]+"|[0-9.]+|{[^}]+}|.', code)
        return blocks

    def _pre(self, code):
        code = re.sub("“[^”]+”", "", code)
        blocks = self._tokenize(code)
        if blocks.count("Ø"):
            code = "".join(blocks[:blocks.index("Ø")])
            try:
                while True:
                    self._run(code)
            except:
                self._exit(0)
        else:
            self._run(code)

    def _run(self, code):
        blocks = self._tokenize(code)
        for elem in blocks:
            isnum = all(e in string.digits for e in elem)
            if (code_page.find(elem[0]) == 34) or isnum:
                self._push(eval(elem))
            elif re.match("(\d+)?\.([\d.]+)?", elem):
                elem = elem.split(".", 1)
                elem[1] = elem[1].replace(".", "0")
                self._push(GoghDecimal(".".join(elem)))
            elif code_page.find(elem[0]) == 123:
                self._push(GoghBlock(elem[1:-1]))
            else:
                reqcode = code_page.index(elem) if elem != "\n" else 32
                self.cchar = elem
                self._request(reqcode)

    def _runoffstack(self, code, ip=None):
        code = "".join(repr(e) for e in code)
        throwaway = Gogh(code, ip, False, None, "", False)
        if len(throwaway) > 0:
            return throwaway._TOS
        else:
            return type(ip)(None)

    def _request(self, action):
        areq = self._req2func.get(action, self._dreq)
        if not getattr(super(), areq, False):
            rlen = self._req2arities.get(action, 0)
            defs = self._req2default.get(action)
            if (not self._islength(rlen)) and (not defs):
                self.broadcast(3, rlen)
        Planner.request(self, action)

    def _exit(self, code):
        if self._islength(1):
            Director._update(self, self._TOS)
        self.broadcast(code)

    # Manipulators

    class _fibo(object):

        def __init__(self, n):
            self.n = n
            self.idx = 0
            self.last = [1, 1]

        def __iter__(self):
            return self

        def __next__(self):
            if self.idx > self.n:
                raise StopIteration
            else:
                self.idx += 1
                if self.idx < 3:
                    return 1
                new = sum(self.last)
                self.last = [self.last[1], new]
                return new

    # I/O Operators

    @Planner.toapprove
    def _output(self, tos):
        self._update(tos, True)
        self.broadcast(0)

    @Planner.toapprove
    def _out_top(self, tos):
        sys.stdout.write(tos._output())
        self._push(tos)

    @Planner.toapprove
    def _print_top(self, tos):
        print(tos._output())
        self._push(tos)

    # Conversion Operators

    @Planner.toapprove
    def _toarray(self, tos):
        self._push(tos._toarray())

    @Planner.toapprove
    def _tonumber(self, tos):
        self._push(tos._tonumber())

    @Planner.toapprove
    def _tostring(self, tos):
        self._push(tos._tostring())

    # Arithmetic Operations

    @Planner.toapprove
    def _add(self, stos, tos):
        self._push(stos + tos)

    @Planner.toapprove
    def _subtract(self, stos, tos):
        self._push(stos - tos)

    @Planner.toapprove
    def _multiply(self, stos, tos):
        self._push(stos * tos)

    @Planner.toapprove
    def _divide(self, stos, tos):
        self._push(stos / tos)

    @Planner.toapprove
    def _modulo(self, stos, tos):
        self._push(stos % tos)

    @Planner.toapprove
    def _greaterthan(self, stos, tos):
        if stos > tos:
            self._push(GoghInteger(1))
        else:
            self._push(GoghInteger(0))

    @Planner.toapprove
    def _lessthan(self, stos, tos):
        if stos < tos:
            self._push(GoghInteger(1))
        else:
            self._push(GoghInteger(0))

    @Planner.toapprove
    def _equals(self, stos, tos):
        if stos._is((GoghNumber, GoghString)):
            stos = str(stos)
        if tos._is((GoghNumber, GoghString)):
            tos = str(tos)
        retval = 1 if stos == tos else 0
        self._push(GoghInteger(retval))

    @Planner.toapprove
    def _negate(self, tos):
        self._push(-tos)

    @Planner.toapprove
    def _power(self, stos, tos):
        self._push(stos ** tos)

    @Planner.toapprove
    def _root(self, stos, tos):
        retval = stos ** (1 / tos)
        if isinstance(retval, (int, float)) and (retval % 1):
            self._push(GoghInteger(retval // 1))
        else:
            self._push(retval)

    # Control Operations

    @Planner.toapprove
    def _keepif_construct(self, stos, tos):
        if bool(stos):
            self._push(stos, tos)
        else:
            self._push(stos)

    @Planner.toapprove
    def _keepif_destruct(self, stos, tos):
        if bool(stos):
            self._push(tos)

    @Planner.toapprove
    def _lognot(self, tos):
        self._push(not bool(tos))

    @Planner.toapprove
    def _execute(self, tos):
        code = "".join(repr(e) for e in tos)
        self._pre(code)

    @Planner.toapprove
    def _if_execute(self, stos, tos):
        if bool(tos):
            code = "".join(repr(e) for e in stos)
            self._pre(code)

    @Planner.toapprove
    def _ifelse_execute(self, ttos, stos, tos):
        if bool(tos):
            torun = ttos
        else:
            torun = stos
        code = "".join(repr(e) for e in torun)
        self._pre(code)

    @Planner.toapprove
    def _exec_off_stack(self, stos, tos):
        retval = self._runoffstack(tos, stos)
        self._push(retval)

    # Array Operations

    @Planner.toapprove
    def _reverse_top(self, tos):
        if tos._is(GoghNumber):
            tos = -tos
        elif tos._is(GoghArray):
            tos.reverse()
        self._push(tos)

    @Planner.toapprove
    def _split(self, stos, tos):
        self._push(stos.split(tos))

    @Planner.toapprove
    def _join(self, stos, tos):
        self._push(stos.join(tos))

    @Planner.toapprove
    def _dump(self, tos):
        if tos._is((GoghNumber, GoghBlock)):
            self._push(tos)
        else:
            for elem in tos:
                self._push(elem)

    # Looping Functions

    @Planner.toapprove
    def _nth_sequence(self, stos, tos):
        stos = int(stos)
        i, j = 0, []
        if stos < 0:
            stos = abs(stos)
        while len(j) < stos:
            if bool(self._runoffstack(tos, i)):
                j.append(i)
            i += 1
        self._push(j.pop() if len(j) == int(stos) and j else 0)

    @Planner.toapprove
    def _map(self, stos, tos):
        if stos._is(GoghString):
            mpd = [self._runoffstack(tos, GoghString(e)) for e in stos]
            mpd = [str(e) for e in mpd if not e._is(GoghBlock)]
            self._push(GoghString("".join(mpd)))
        else:
            mpd = GoghArray(self._runoffstack(tos, e) for e in stos)
            self._push(mpd)

    @Planner.toapprove
    def _all(self, tos):
        if tos._is((GoghNumber, GoghBlock)):
            self._push(GoghInteger(bool(tos)))
        else:
            self._push(GoghInteger(all(tos)))

    @Planner.toapprove
    def _any(self, tos):
        if tos._is((GoghNumber, GoghBlock)):
            self._push(GoghInteger(bool(tos)))
        else:
            self._push(GoghInteger(any(tos)))

    # Pre-initialized Variables

    @Planner.toapprove
    def _twofalse(self):
        self._push(GoghInteger(0), GoghInteger(0))

    @Planner.toapprove
    def _twotrue(self):
        self._push(GoghInteger(1), GoghInteger(1))

    @Planner.toapprove
    def _square(self, tos):
        self._push(tos ** 2)

    @Planner.toapprove
    def _cube(self, tos):
        self._push(tos ** 3)

    # Various Operations

    @Planner.toapprove
    def _fibonacci(self, tos):
        if tos._is(GoghBlock):
            self._push(tos)
            return
        elif tos._is(GoghArray):
            tos = len(tos)
        else:
            tos = int(tos)
        fib = Gogh._fibo(tos-1)
        self._push(GoghArray(fib))
