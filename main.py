from stack import Stack
from control import Director, Planner
from gtypes import GoghObject, GoghString, GoghInteger, GoghDecimal, GoghArray


code_page  = """¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶"""
code_page += """°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭụṿẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”"""


class Gogh(Director, Stack):

    _dreq = "_noop"
    _req2func = {
        0  : "_output",
        97 : "_toarray",
        110: "_tonumber",
        115: "_tostring",
    }
    _req2arities = {}
    _req2argtype = {}
    _req2default = {}
    _req2stack = {
        0  : 1,
        97 : 1,
        110: 1,
        115: 1,
    }

    _req2func.update(Stack._req2func)
    _req2arities.update(Stack._req2arities)
    _req2argtype.update(Stack._req2argtype)
    _req2default.update(Stack._req2default)

    def __init__(self, code, ip, out, err, endchar):
        Director.__init__(self, out, endchar)
        Stack.__init__(self, ip)
        if err != None:
            self.broadcast(*err)
        self.cchar = None
        self.frames = self._tokenize(code)

    def _tokenize(self, code):
        for char in code:
            reqcode = code_page.index(char)
            self.cchar = char
            self._request(reqcode)
        self._exit(0)

    def _request(self, action):
        areq = self._req2func.get(action, self._dreq)
        if not getattr(super(), areq, False):
            rlen = self._req2stack.get(action, 0)
            if not self._islength(rlen):
                self.broadcast(3, rlen)
        Planner.request(self, action)

    def _exit(self, code):
        if self._islength(1):
            Director._update(self, self._TOS)
        self.broadcast(code)

    # Manipulators

    @Planner.toapprove
    def _output(self):
        self._update(self._TOS, True)
        self.broadcast(0)

    @Planner.toapprove
    def _toarray(self):
        retval = self._TOS._toarray()
        self._push(retval)

    @Planner.toapprove
    def _tonumber(self):
        retval = self._TOS._tonumber()
        self._push(retval)

    @Planner.toapprove
    def _tostring(self):
        retval = self._TOS._tostring()
        self._push(retval)
