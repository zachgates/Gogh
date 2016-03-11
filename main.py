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

    _req2func.update(Stack._req2func)
    _req2arities.update(Stack._req2arities)
    _req2argtype.update(Stack._req2argtype)
    _req2default.update(Stack._req2default)

    def __init__(self, code, ip, out, err, endchar):
        Director.__init__(self, out, endchar)
        Stack.__init__(self, ip)
        if err != None:
            self.broadcast(*err)
        self.frames = self._tokenize(code)

    def _tokenize(self, code):
        for char in code:
            reqcode = code_page.index(char)
            self.request(reqcode)
        self._update(self._TOS)
        self.broadcast(0)

    # Manipulators

    def _output(self):
        self._update(self._TOS, True)
        self.broadcast(0)

    def _toarray(self):
        self._push(self._TOS._toarray())

    def _tonumber(self):
        self._push(self._TOS._tonumber())

    def _tostring(self):
        self._push(self._TOS._tostring())
