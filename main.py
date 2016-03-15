import re
from stack import Stack
from control import Director, Planner
from gtypes import GoghObject
from gtypes import GoghString, GoghInteger, GoghDecimal, GoghArray
from gtypes import GoghBlock


code_page  = """¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶"""
code_page += """°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”"""


class Gogh(Director, Stack):

    # Storage

    _dreq = "_noop"
    _req2func = {
        0  : "_output",
        42 : "_multiply",
        43 : "_add",
        45 : "_subtract",
        47 : "_divide",
        94 : "_negate",
        97 : "_toarray",
        110: "_tonumber",
        115: "_tostring",
    }
    _req2arities = {
        0  : 1,
        42 : 2,
        43 : 2,
        45 : 2,
        47 : 2,
        94 : 1,
        97 : 1,
        110: 1,
        115: 1,
    }
    _req2argtype = {
        0  : [GoghObject],
        42 : [GoghObject, GoghObject],
        43 : [GoghObject, GoghObject],
        45 : [GoghObject, GoghObject],
        47 : [GoghObject, GoghObject],
        94 : [GoghObject],
        97 : [GoghObject],
        110: [GoghObject],
        115: [GoghObject],
    }
    _req2default = {}

    _req2func.update(Stack._req2func)
    _req2arities.update(Stack._req2arities)
    _req2argtype.update(Stack._req2argtype)
    _req2default.update(Stack._req2default)

    # Controllers

    def __init__(self, code, ip, out, err, endchar):
        Director.__init__(self, out, endchar)
        Stack.__init__(self, ip)
        if err != None:
            self.broadcast(*err)
        self.cchar = None
        self.intreg = None
        self.strreg = None
        self.strlit = False
        self.frames = self._tokenize(code)

    def _tokenize(self, code):
        blocks = re.findall('"[^"]+"|[0-9.]+|{[^}]+}|.', code)
        for elem in blocks:
            if elem.startswith('"') or elem.isnumeric():
                self._push(eval(elem))
            elif re.match("(\d+)?\.([\d.]+)?", elem):
                elem = elem.split(".", 1)
                elem[1] = elem[1].replace(".", "0")
                self._push(GoghDecimal(".".join(elem)))
            elif elem.startswith("{"):
                self._push(GoghBlock(elem[1:-1]))
            else:
                reqcode = code_page.index(elem) if elem != "\n" else 32
                self.cchar = elem
                self._request(reqcode)
        self._exit(0)

    def _request(self, action):
        areq = self._req2func.get(action, self._dreq)
        if not getattr(super(), areq, False):
            rlen = self._req2arities.get(action, 0)
            if not self._islength(rlen):
                self.broadcast(3, rlen)
        Planner.request(self, action)

    def _exit(self, code):
        if self._islength(1):
            Director._update(self, self._TOS)
        self.broadcast(code)

    # Manipulators

    @Planner.toapprove
    def _output(self, tos):
        self._update(tos._output(), True)
        self.broadcast(0)

    @Planner.toapprove
    def _toarray(self, tos):
        self._push(tos._toarray())

    @Planner.toapprove
    def _tonumber(self, tos):
        self._push(tos._tonumber())

    @Planner.toapprove
    def _tostring(self, tos):
        self._push(tos._tostring())

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
    def _negate(self, tos):
        self._push(-tos)
