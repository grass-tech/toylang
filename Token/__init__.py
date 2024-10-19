import string

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Error

punctuation = "@#$%;:<>\\`([{" + string.whitespace

# 类型(Token Type)
# Basic
TTT_STR = "STR"
TTT_INT = "INT"
TTT_FLOAT = "FLOAT"

TTT_ARRAY = "ARRAY"
TTT_STRUCTURE = "STRUCTURE"
TTT_CLUSTER = "CLUSTER"

TTT_GETTER = "GETSPEC"

TTT_BIN = "BIN"
TTT_HEX = "HEX"
TTT_OCT = "OCT"

TTT_KEYWORD = "KEYWORD"
TTT_IDENTIFIER = "IDENTIFIER"

TTT_NEWLINE = "NEWLINE"
TTT_EOF = "EOF"
# 符号(Token Pos)
TTP_LEFT_PAR = "LPAR"  # (
TTP_RIGHT_PAR = "RPAR"  # )
TTP_LEFT_SQB = "LSQB"  # [
TTP_RIGHT_SQB = "RSQB"  # ]
TTP_LEFT_BRACE = "LBRACE"  # {
TTP_RIGHT_BRACE = "RBRACE"  # }
TTP_DOT = "DOT"  # .
TTP_COMMA = "COMMA"  # ,
TTP_COLON = "COLON"  # :
TTP_SEMI = TTT_NEWLINE  # ;
TTP_ESCAPE = "ESCAPE"  # \
TTP_AS = "AS"  # ->
TTP_MACRO = "MACRO"  # #
TTP_RIGHT_COMMENT = "RIGHT_COMMENT"  # /*
TTP_LEFT_COMMENT = "LEFT_COMMENT"  # */
## 运算(Computing Pos)
TCP_PLUS = "PLUS"  # +
TCP_MINUS = "MINUS"  # -
TCP_MUL = "MUL"  # *
TCP_POW = "POW"  # **
TCP_DIV = "DIV"   # /
TCP_INTEGER_DIV = "TRUNCATION"  # //
TCP_MOD = "MOD"  # %
## 逻辑(Logic Pos)
TLP_GETTER = "GETTER"  # $
TLP_WHETHER = "WHETHER"  # ?
TLP_NOT = "NOT"  # !
TLP_NOT_EQUAL = "NOTEQUAL"  # !=

TLP_XOR = "XOR"  # ^
TLP_AND = "AND"  # &
TLP_OR = "OR"  # |
TLP_AND_MOVEMENT = "AND_MOVEMENT"  # &&
TLP_OR_MOVEMENT = "OR_MOVEMENT"  # ||
TLP_LEFT_MOVEMENT = "LEFT_MOVEMENT"   # <<
TLP_RIGHT_MOVEMENT = "RIGHT_MOVEMENT"   # >>

TLP_GREATER = "GREATER"  # >
TLP_GREATER_EQUAL = "GREATEREQUAL"  # >=
TLP_LESS = "LESS"  # <
TLP_LESS_EQUAL = "LESSEQUAL"  # <=
TLP_EQUAL = "EQUAL"  # =
TLP_DOUBLE_EQUAL = "EQEQUAL"  # ==

# 总预览(Preview)
PREVIEW = {
    ")": TTP_RIGHT_PAR,
    "]": TTP_RIGHT_SQB,
    "}": TTP_RIGHT_BRACE,
    ".": TTP_DOT,
    ":": TTP_COLON,
    ";": TTP_SEMI,
    "\\": TTP_ESCAPE,
    ",": TTP_COMMA,
    "->": TTP_AS,
    "/*": TTP_LEFT_COMMENT,
    "*/": TTP_RIGHT_COMMENT,

    "+": TCP_PLUS,
    "-": TCP_MINUS,
    "*": TCP_MUL,
    "**": TCP_POW,
    "/": TCP_DIV,
    "//": TCP_INTEGER_DIV,
    "%": TCP_MOD,

    "$": TLP_GETTER,
    "?": TLP_WHETHER,
    "!": TLP_NOT,

    "^": TLP_XOR,
    "&": TLP_AND_MOVEMENT,
    "|": TLP_OR_MOVEMENT,
    "&&": TLP_AND,
    "||": TLP_OR,
    "<<": TLP_LEFT_MOVEMENT,
    ">>": TLP_RIGHT_MOVEMENT,

    "!=": TLP_NOT_EQUAL,
    ">": TLP_GREATER,
    ">=": TLP_GREATER_EQUAL,
    "<": TLP_LESS,
    "<=": TLP_LESS_EQUAL,
    "=": TLP_EQUAL,
    "==": TLP_DOUBLE_EQUAL,
}
PREVIEW_LOGIC = {
    "+": TCP_PLUS,
    "-": TCP_MINUS,
    "*": TCP_MUL,
    "**": TCP_POW,
    "/": TCP_DIV,
    "//": TCP_INTEGER_DIV,
    "%": TCP_MOD,
}
SYNTAX = [
    "private",

    "var",
    "delete",

    "if",
    "elseif",
    "else",

    "foriter",
    "by",

    "for",
    "from",
    "to",
    "step",

    "repeat",
    "until",
    "meet",

    "break",
    "continue",

    "function",
    "return",

    "include"
]
BOOLEAN = [
    "and",
    "or",
    "not"
]
KEYWORDS = SYNTAX + BOOLEAN


class Position:
    def __init__(self, idx: int, ln: int, col: int, fn: str, ftxt: str):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advanced(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = -1

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


class Token:
    def __init__(self, type_: str, value=None, pos_start=None, pos_end=None):
        self.value = value
        self.type = type_

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advanced()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        if self.value is not None:
            return f'{self.type}:{self.value}'
        else:
            return f'{self.type}'


class Lexer:
    def __init__(self, run_mode: str, syntax: str) -> None:
        self._syntax = syntax
        self._pos = Position(-1, 1, -1, run_mode, syntax)
        self._current_char = None
        self._err = None

        self._run_mode = run_mode

        self._advanced()

    def _advanced(self) -> None:
        """获取当前的字符"""
        self._pos.advanced(self._current_char)
        self._current_char = self._syntax[self._pos.idx] if self._pos.idx < len(self._syntax) else None

    def make_tokens(self) -> list:
        tokens = []
        # pos = self._pos
        while self._current_char is not None and self._err is None:
            # 制作符号(make pos)
            if self._current_char in PREVIEW.keys():
                self._err, t = self._make_pos(PREVIEW)
                if "null" not in t:
                    tokens.extend(t)
            # 制作数字(make number)
            elif self._current_char in string.digits + ".":
                self._err, t = self._make_number()
                tokens.append(t)
            # 制作标识符
            elif self._current_char in string.ascii_letters + "_":
                t = self._make_identifier()
                tokens.append(t)
            else:
                # 制作其他符号
                match self._current_char:
                    case "\n":
                        tokens.append(Token(TTT_NEWLINE, pos_start=self._pos.copy(), pos_end=self._pos))
                        self._advanced()
                    case "\"":
                        self._err, t = self._make_string("\"")
                        tokens.append(t)
                    case "'":
                        self._err, t = self._make_string("'")
                        tokens.append(t)
                    case "{":
                        pos_start = self._pos.copy()
                        self._err, t = self._make_include("}")
                        tokens.append(Token(TTT_CLUSTER, t, pos_start=pos_start, pos_end=self._pos))
                    case "[":
                        pos_start = self._pos.copy()
                        self._err, t = self._make_include("]")
                        tokens.append(Token(TTT_ARRAY, t, pos_start=pos_start, pos_end=self._pos))
                    case "(":
                        pos_start = self._pos.copy()
                        self._err, t = self._make_include(")")
                        tokens.append(Token(TTT_STRUCTURE, t, pos_start=pos_start, pos_end=self._pos))
                    case _:
                        self._advanced()
        tokens.append(Token(TTT_EOF, pos_start=self._pos, pos_end=self._pos))
        if self._err is not None:
            return [self._err, None]
        else:
            return [None, tokens]

    def _make_string(self, match_marks) -> list:
        char = ""
        pos_start = self._pos.copy()
        isEscape = False
        escape_dict = {
            "n": "\n",
            "t": "\t",
            "\\": "\\",
            "\"": "\"",
            "'": "\'",
        }
        self._advanced()

        while self._current_char != match_marks or isEscape:
            if self._current_char is None:
                return [
                    Error.InvalidSyntaxError(
                        pos_start, self._pos.copy(),
                        f"The {"\"'\"" if match_marks == "'" else '\'"\''} was never closed"),
                    None
                ]
            if isEscape:
                char += escape_dict[self._current_char]
                isEscape = False
            else:
                if self._current_char == "\\":
                    isEscape = True
                else:
                    char += self._current_char
            self._advanced()

        self._advanced()
        return [None, Token(TTT_STR, char, pos_start, self._pos)]

    def _make_number(self) -> list:
        char = ""
        dot_count = 0
        pos_start = self._pos.copy()
        is_base = False
        base_string = string.digits + '.bxo'
        while self._current_char is not None and self._current_char in base_string:
            if self._current_char == ".":
                dot_count += 1
            elif self._current_char == "x" and char[-1] == "0" and len(char) == 1:
                char = char[1:]
                is_base = TTT_HEX
                base_string = string.hexdigits
                self._advanced()
                continue
            elif self._current_char == "b" and char[-1] == "0" and len(char) == 1:
                char = char[1:]
                is_base = TTT_BIN
                base_string = "10"
                self._advanced()
                continue
            elif self._current_char == "o" and char[-1] == "0" and len(char) == 1:
                char = char[1:]
                is_base = TTT_OCT
                base_string = string.octdigits
                self._advanced()
                continue
            if dot_count >= 2:
                return [
                    Error.InvalidSyntaxError(
                        pos_start,
                        self._pos.copy(),
                        char + '.'
                    ),
                    None
                ]
            char += self._current_char
            self._advanced()
        if dot_count == 1:
            return [None, Token(TTT_FLOAT, float(char), pos_start, self._pos)]
        elif is_base == TTT_BIN:
            return [None, Token(TTT_BIN, char, pos_start, self._pos)]
        elif is_base == TTT_OCT:
            return [None, Token(TTT_OCT, char, pos_start, self._pos)]
        elif is_base == TTT_HEX:
            return [None, Token(TTT_HEX, char, pos_start, self._pos)]
        else:
            try:
                return [None, Token(TTT_INT, int(char), pos_start, self._pos)]
            except ValueError:
                return [Error.InvalidValueError(
                    pos_start, self._pos.copy(),
                    "invalid base value"
                ), None]

    def _make_identifier(self):
        char = ""
        pos_start = self._pos.copy()

        while self._current_char is not None and self._current_char in string.ascii_letters + string.digits + "_":
            char += self._current_char
            self._advanced()

        if char in KEYWORDS:
            return Token(TTT_KEYWORD, char, pos_start, self._pos)
        else:
            return Token(TTT_IDENTIFIER, char, pos_start, self._pos)

    def _make_pos(self, preview) -> list:
        chars = ""
        pos_start = self._pos
        tokens = []

        while self._current_char is not None and self._current_char in preview.keys():
            chars += self._current_char
            self._advanced()

        if chars in preview.keys():
            chars = [chars]
        for char in chars:
            if preview[char] == TTP_LEFT_COMMENT:
                err = self._skip_comment()
                if err:
                    return [err, None]
                tokens.append('null')
                continue

            elif char in ("!", "&&", "||"):
                transfer = {
                    "!": "not",
                    "&&": "and",
                    "||": "or"
                }
                tokens.append(Token(TTT_KEYWORD, transfer[char], pos_start=pos_start, pos_end=self._pos))
                continue

            elif char == "$":
                get_char = ''
                while self._current_char is not None and self._current_char in string.ascii_letters + "_":
                    get_char += self._current_char
                    self._advanced()

                tokens.append(Token(TTT_GETTER, get_char, pos_start=pos_start, pos_end=self._pos))
                continue

            tokens.append(Token(preview[char], pos_start=pos_start, pos_end=self._pos))
        return [None, tokens]

    def _make_include(self, match_pos) -> list:
        pos_start = self._pos.copy()

        disappearString = False
        isString = False
        disappearComment = False
        isComment = False
        relay_char = ""
        tokens = []

        self._advanced()
        while True:
            if str(self._current_char) in ('(', '[', '{') and not disappearString and not disappearComment:
                op = self._current_char
                start_idx = self._pos.idx
                i = self._pos.idx
                mp = {"(": ")", "[": "]", "{": "}"}[self._current_char]
                include_otherpos = []
                otherpos_idx = 0
                self._advanced()
                while True:
                    i += 1
                    if self._current_char in ("'", '"') and not isString and not isComment:
                        isString = True
                    elif self._current_char in ("'", '"') and isString and not isComment:
                        isString = False
                    if self._current_char == "/" and self._syntax[self._pos.idx + 1] == "*" and \
                            not isComment and not isString:
                        isComment = True
                    elif self._current_char == "*" and self._syntax[self._pos.idx - 1] == "/" and \
                            isComment and not isString:
                        isComment = False
                    if self._current_char == op and not isString and not isComment:
                        include_otherpos.append(True)
                        otherpos_idx += 1
                    if self._current_char == mp and not isString and not isComment and True not in include_otherpos:
                        break
                    elif self._current_char == mp and not isString and not isComment:
                        otherpos_idx -= 1
                        include_otherpos.pop(otherpos_idx)
                    if self._current_char is None:
                        return [Error.InvalidSyntaxError(
                            pos_start, self._pos.copy(), f"The '{mp}' was never closed, wth"), None]
                    self._advanced()
                err, t = Lexer(self._run_mode, self._syntax[start_idx:i + 1]).make_tokens()
                if err: return [err, None]
                tokens.append(t[:-1][0])
                self._advanced()

            elif self._current_char == match_pos and not disappearString and not disappearComment:
                self._advanced()
                if relay_char:
                    err, t = Lexer(self._run_mode, relay_char).make_tokens()
                    if err: return [err, None]
                    tokens += t[:-1]
                break
            elif self._current_char is None:
                return [Error.InvalidSyntaxError(
                    pos_start, self._pos.copy(), f"The '{match_pos}' was never closed"), None]
            else:
                relay_char += self._current_char
                if not disappearString and self._current_char in ('"', "'"):
                    disappearString = True
                elif disappearString and self._current_char in ('"', "'"):
                    disappearString = False
                if not disappearComment and relay_char.strip().replace("\n", "") == "/*":
                    disappearComment = True
                elif disappearComment and not disappearString and '*/' in relay_char.strip().replace("\n", ""):
                    disappearComment = False
                self._advanced()
                if self._current_char is None:
                    return [Error.InvalidSyntaxError(
                        pos_start, self._pos.copy(), f"The '{match_pos}' was never closed"), None]
                if not disappearString and not disappearComment and self._current_char in punctuation:
                    err, t = Lexer(self._run_mode, relay_char).make_tokens()
                    if err: return [err, None]
                    tokens += t[:-1]
                    relay_char = ""

        tokens = tokens + [Token(TTT_EOF, pos_start=self._pos.copy(), pos_end=self._pos.copy())]
        return [None, tokens]

    def _skip_comment(self):
        pos_start = self._pos.copy()
        self._advanced()
        while self._current_char != "*" and self._syntax[self._pos.idx + 1] != "/":
            if self._current_char is None:
                return Error.InvalidSyntaxError(
                    pos_start, self._pos.copy(),
                    "expected '*/', did you forget '*/'?")
            self._advanced()
        self._advanced()
        self._advanced()
        return None
