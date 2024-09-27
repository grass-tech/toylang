import re
import ast

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Token
import Parser
import Error


class Value:
    def __init__(self):
        self.pos_start = None
        self.pos_end = None
        self.context = None

        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def is_equals(self, other):
        return None, self.illegal_operation(other)

    def is_not_equals(self, other):
        return None, self.illegal_operation(other)

    def is_less(self, other):
        return None, self.illegal_operation(other)

    def is_less_equals(self, other):
        return None, self.illegal_operation(other)

    def is_greater(self, other):
        return None, self.illegal_operation(other)

    def is_greater_equals(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def execute(self, args):
        return Parser.RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    @staticmethod
    def is_true():
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return Error.RunningTimeError(
            self.pos_start, other.pos_end,
            f"Not supported operation for '{type(self).__name__}'",
        )


class Null(Value):
    def __init__(self, type_=None, value=None):
        super().__init__()
        self.type = type_
        self.value = value

    def get(self):
        return self.type(self.value)

    @staticmethod
    def boolean():
        return Number(0)

    @staticmethod
    def length():
        return -1

    def __repr__(self):
        return "NULL"


class Number(Value):
    def __init__(self, value):
        super().__init__()
        if '.' in str(value):
            self.value = float(str(value))
        else:
            self.value = int(str(value))

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    @staticmethod
    def get_num(left, right=None):
        if '.' not in str(left):
            lv = int(str(left))
        else:
            lv = float(str(left))
        if right is not None:
            if '.' not in str(right):
                rv = int(str(right))
            else:
                rv = float(str(right))
        else:
            return lv
        return lv, rv

    def added_to(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(left + right), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'+' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def subbed_by(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(left - right), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'-' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def multi_by(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(left * right), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'*' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def dived_by(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            if right == 0:
                return (None, Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    "division by zero, division not supported by zero"))
            return Number(left / right), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'/' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def intdived_by(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            if right == 0:
                return (None, Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    "integer division by zero, integer division not supported by zero"))
            return Number(left // right), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'//' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def powered_by(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(left ** right), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'**' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def modded_by(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            if right == 0:
                return (None, Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    "Modulo by zero, modulo not supported by zero"))
            return Number(left % right), None

    def is_equals(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
        else:
            return Number(0), None
        return Number(int(left == right)), None

    def is_greater(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(int(left > right)), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'>' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def is_greater_equals(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(int(left >= right)), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'>=' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def is_less(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(int(left < right)), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'<' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def is_less_equals(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(int(left <= right)), None
        return None, Error.InvalidSyntaxError(
            self.pos_start, other.pos_end,
            f"'<=' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def is_not_equals(self, other):
        if isinstance(other, Number):
            left, right = self.get_num(self.value, other.value)
            return Number(int(left != right)), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'!=' is not supported for type '{type(self).__name__}' and '{type(other).__name__}'")

    def notted(self):
        main = self.get_num(self.value)
        return Number(0 if bool(main) else 1), None

    def anded_by(self, other):
        if isinstance(other.value, Number):
            left, right = self.get_num(self.value, other.value)
        else:
            left, right = self.get_num(self.value), other.value
        if not right:
            return Number(0), None
        return Number(1 if int(left and right) else 0), None

    def ored_by(self, other):
        if isinstance(other.value, Number):
            left, right = self.get_num(self.value, other.value)
        else:
            left, right = self.get_num(self.value), other.value
        if not right:
            return Number(0), None
        return Number(1 if int(left or right) else 0), None

    def is_true(self):
        return self.value != 0

    def boolean(self):
        return Number(0 if self.value == 0 else 1)

    @staticmethod
    def length():
        return -1

    def __repr__(self):
        return str(self.value)


true = Number.true = Number(1)
false = Number.false = Number(0)
null = Number.null = Number(0)


# 字符串的运算
class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = str(value)

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_equals(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)), None
        else:
            return Number(0), None

    def added_to(self, other):
        if isinstance(other, String):
            return String(str(self.value) + str(other.value)), None
        else:
            return None, Error.InvalidValueError(
                self.pos_start, self.pos_end,
                f"The type '{type(self).__name__}' "
                f"not supported '{type(self).__name__}' + '{type(other).__name__}'")

    def subbed_by(self, other):
        if isinstance(other, String):
            return String(
                re.sub(re.escape(other.value), "", self.value)), None
        elif isinstance(other, Number):
            return None, Error.InvalidValueError(
                self.pos_start, self.pos_end,
                f"The type '{type(self).__name__}' "
                f"not supported '{type(self).__name__}' - '{type(other).__name__}'")

    def multi_by(self, other):
        if isinstance(other, Number):
            return String(str(self.value) * int(other.value)), None
        else:
            return None, Error.InvalidValueError(
                self.pos_start, self.pos_end,
                f"The type '{type(self).__name__}' "
                f"not supported '{type(self).__name__}' * '{type(other).__name__}'")

    def notted(self):
        return Number(0 if bool(str(self.value)) else 1), None

    def anded_by(self, other):
        if not (self.value and other.value):
            return Number(0), None
        return Number(1 if int(self.value and other.value) else 0), None

    def ored_by(self, other):
        if not (self.value and other.value):
            return Number(0), None
        return Number(1 if int(self.value or other.value) else 0), None

    def is_true(self):
        return self.value != 0

    def boolean(self):
        return Number(0 if self.value == "" else 1)

    def __repr__(self):
        return str(self.value)

    def length(self):
        return len(str(self.value))


# 结构
class Structure(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = str(elements).split(",") if not isinstance(elements, list) else elements

    def copy(self):
        copy = Structure(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_equals(self, other):
        if isinstance(other, Structure):
            return Number(int(self.elements == other.elements)), None
        else:
            return Number(0), None

    def added_to(self, other):
        if isinstance(self.elements[0], String) and isinstance(other, String):
            return String(str(self.elements[0]) + str(other.value)), None
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'+' is not supported for type 'structure'"
        )

    def notted(self):
        return None, Error.InvalidValueError(
            self.pos_start, self.pos_end,
            f"'not' or '!' is not supported for type 'structure'")

    def anded_by(self, other):
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'and' or '&' is not supported for type 'structure'")

    def ored_by(self, other):
        return None, Error.InvalidValueError(
            self.pos_start, other.pos_end,
            f"'or' or '|' is not supported for type 'structure'")

    def is_true(self):
        return self.elements != 0

    def boolean(self):
        return Number(1 if self.elements else 0)

    def length(self):
        return len(self.elements)

    def __repr__(self):
        if len(self.elements) > 1:
            return (f"("
                    f"{', '.join(
                        [f'{{(arg{i} = {self.elements[i]})'
                         f' -> {type(self.elements[i]).__name__}}}'
                         for i in range(len(self.elements))])}"
                    f")")
        else:
            return f"{''.join([str(x) for x in self.elements])}"


# 数组
class Array(Value):
    def __init__(self, elements):
        super().__init__()
        if isinstance(elements, list):
            self.elements = elements
        elif isinstance(elements, Array):
            self.elements = str(str(elements)[1:-1]).split(", ")
        else:
            self.elements = str(elements).split(",")

    def is_equals(self, other):
        if isinstance(other, Array):
            return Number(int(self.elements == other.elements)), None
        else:
            return Number(0), None

    def copy(self):
        copy = Array(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def added_to(self, other):
        if isinstance(other, Array):
            new_array = self.copy()
            new_array.elements.extend(other.elements)
            return new_array, None
        else:
            new_array = self.copy()
            new_array.elements.append(other.value)
            return new_array, None

    def multi_by(self, other):
        if isinstance(other, Number):
            new_array = self.copy()
            new_array.elements = new_array.elements * int(other.value)
            return new_array, None
        else:
            return None, Error.InvalidValueError(
                self.pos_start, self.pos_end,
                f"The type '{type(self).__name__}' "
                f"is not supported '{type(self).__name__}' * '{type(other).__name__}'")

    def dived_by(self, other):
        if isinstance(other, Number):
            new_array = self.copy()
            try:
                new_array.elements.pop(int(other.value))
                return new_array, None
            except IndexError:
                return None, Error.RunningTimeError(
                    self.pos_start, self.pos_end,
                    f"'{other.value}' is out of range of index")
        else:
            return None, Error.InvalidValueError(
                self.pos_start, self.pos_end,
                f"The type '{type(self).__name__}' "
                f"is not supported '{type(self).__name__}' / '{type(other).__name__}'")

    def notted(self):
        return Number(0 if bool(self.elements) else 1), None

    def anded_by(self, other):
        if not (self.elements and other.elements):
            return Number(0), None
        return Number(1 if int(self.elements and other.elements) else 0), None

    def ored_by(self, other):
        if not (self.elements and other.elements):
            return Number(0), None
        return Number(1 if int(self.elements or other.elements) else 0), None

    def is_true(self):
        return self.elements != 0

    def boolean(self):
        return Number(1 if self.elements else 0)

    def length(self):
        return len(self.elements)

    def __repr__(self):
        return f"[{', '.join([str(x) for x in self.elements])}]"


# 簇
class Cluster(Value):
    def __init__(self, elements, ):
        super().__init__()
        self.elements = str(elements).split(";") if not isinstance(elements, list) else elements

    def copy(self):
        copy = Cluster(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_equals(self, other):
        if isinstance(other, Cluster):
            return Number(int(self.elements == other.elements)), None
        else:
            return Number(0), None

    def is_true(self):
        return self.elements != 0

    def boolean(self):
        return Number(1 if self.elements else 0)

    def length(self):
        return len(self.elements)

    def __repr__(self):
        return f"{''.join([str(x) for x in self.elements])}"


class Library(Value):
    def __init__(self, lib_name):
        super().__init__()
        self.lib_name = lib_name

    def copy(self):
        copy = Library(self.lib_name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_equals(self, other):
        if isinstance(other, Library):
            return Number(int(self.lib_name == other.lib_name)), None
        else:
            return Number(0), None

    @staticmethod
    def is_true():
        return True

    @staticmethod
    def boolean():
        return Number(1)

    @staticmethod
    def length():
        return -1

    def __repr__(self):
        return f"<(Library | Module) @ '{self.lib_name}'>"


class BaseFunction(Value):
    def __init__(self, name, father):
        super().__init__()
        self.name = name or '<anonymous>'
        self.father = father

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        # 往局部变量添加特定变量
        new_context.symbol_table.set("null", null)
        new_context.symbol_table.set("true", true)
        new_context.symbol_table.set("false", false)
        for var_name, value in self.context.symbol_table.symbols.items():
            if isinstance(value, Function) or isinstance(value, BuiltinFunction):
                new_context.symbol_table.set(var_name, value)
            if self.father is not None:
                if isinstance(value, dict) and str(var_name) == self.father[0]:
                    for dict_key, dict_value in value.items():
                        new_context.symbol_table.set(dict_key, dict_value)

        return new_context

    def check_args(self, arg_names, args):
        res = Parser.RTResult()

        if len(args) > len(arg_names):
            return res.failure(
                Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    f"{len(args) - len(arg_names)} too many args passed to {self.name}"
                )
            )
        if len(args) < len(arg_names):
            return res.failure(
                Error.InvalidSyntaxError(
                    self.pos_start, self.pos_end,
                    f"{len(arg_names) - len(args)} a few args passed to {self.name}"
                )
            )

        return res.success(Null())

    @staticmethod
    def populate_args(arg_names, args, exec_ctf):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctf)
            exec_ctf.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctf):
        res = Parser.RTResult()

        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctf)
        return res.success(Null())


# 函数
class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_return_null, father):
        super().__init__(name, father)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_return_null = should_return_null

    def execute(self, args):
        res = Parser.RTResult()
        interpreter = Interpreter()

        exec_ctf = self.generate_new_context()
        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctf))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_ctf, None))
        if res.should_return() and res.function_return_value is None: return res

        return_value = (value if self.should_return_null else None) or res.function_return_value or Null()
        return res.success(return_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_return_null, self.father)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def is_equals(self, other):
        if isinstance(other, Function):
            return Number(1), None
        else:
            return Number(0), None

    def is_true(self):
        return self.name != 0

    @staticmethod
    def boolean():
        return Number(1)

    @staticmethod
    def length():
        return -1

    def __repr__(self):
        return (f"<external.function {self.name} @ "
                f"{id(f'{self.name}')}>")


class BuiltinFunction(BaseFunction):
    def __init__(self, name, father):
        super().__init__(name, father)
        self.name = name
        self.father = father

    def execute(self, args):
        res = Parser.RTResult()
        exec_cft = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_cft))
        if res.should_return(): return res

        return_value = res.register(method(exec_cft))
        if res.should_return(): return res

        return res.success(return_value)

    def no_visit_method(self, node, context, father):
        raise Exception(f"No execute_{self.name} method defined")

    def execute_println(self, exec_cft):
        print(str(exec_cft.symbol_table.get('value')))
        return Parser.RTResult().success(Null())

    execute_println.arg_names = ["value"]

    def execute_readline(self, exec_cft):
        return Parser.RTResult().success(String(str(input(str(exec_cft.symbol_table.get('value'))))))

    execute_readline.arg_names = ["value"]

    def execute_len(self, exec_cft):
        if exec_cft.symbol_table.get('value').length() == -1:
            return Parser.RTResult().failure(Error.RunningTimeError(
                self.pos_start, self.pos_end,
                f"Can't get length of type '{type(exec_cft.symbol_table.get('value')).__name__}'"
            ))
        return Parser.RTResult().success(Number(int(exec_cft.symbol_table.get('value').length())))
    execute_len.arg_names = ["value"]

    def execute_run(self, exec_cft):
        fn = exec_cft.symbol_table.get("filename")

        if not isinstance(fn, String):
            return Parser.RTResult().failure(
                Error.InvalidTypeError(
                    self.pos_start, self.pos_end,
                    f"Argument must be String, not {type(fn).__name__}"
                )
            )

        fn = fn.value

        try:
            with open(fn, "r", encoding="utf-8") as f:
                scripts = f.read()
        except FileNotFoundError:
            return Parser.RTResult().failure(
                Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    f"'{fn}' is not exists"
                )
            )
        error = execute(fn, scripts)

        if error and not isinstance(error, Array):
            return Parser.RTResult().failure(
                Error.RunningTimeError(
                    self.pos_start, self.pos_end,
                    f"Failed to executing scripts '{fn}'\n\n"
                    f"During this error, discover another error:\n\n"
                    f"{error}"
                )
            )

        return Parser.RTResult().success(Null())
    execute_run.arg_names = ["filename"]

    def execute_int(self, exec_cft):
        try:
            return Parser.RTResult().success(Number(int(str(exec_cft.symbol_table.get('value')))))
        except (ValueError, SyntaxError):
            return Parser.RTResult().failure(
                Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    f"Can't literal for int() with: '{str(exec_cft.symbol_table.get('value'))}'")
            )

    execute_int.arg_names = ["value"]

    def execute_str(self, exec_cft):
        return Parser.RTResult().success(String(str(exec_cft.symbol_table.get('value'))))

    execute_str.arg_names = ["value"]

    def execute_float(self, exec_cft):
        try:
            return Parser.RTResult().success(Number(float(str(exec_cft.symbol_table.get('value')))))
        except (ValueError, SyntaxError):
            return Parser.RTResult().failure(
                Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    f"Can't literal for float() with: '{str(exec_cft.symbol_table.get('value'))}'")
            )

    execute_float.arg_names = ["value"]

    def execute_bool(self, exec_cft):
        return Parser.RTResult().success(exec_cft.symbol_table.get("value").boolean())

    execute_bool.arg_names = ["value"]

    def execute_array(self, exec_cft):
        try:
            return Parser.RTResult().success(
                Array(ast.literal_eval(str(exec_cft.symbol_table.get('value')))))
        except (ValueError, SyntaxError):
            return Parser.RTResult().failure(
                Error.InvalidValueError(
                    self.pos_start, self.pos_end,
                    f"Can't literal for array() with: '{str(exec_cft.symbol_table.get('value'))}'")
            )

    execute_array.arg_names = ["value"]

    def copy(self):
        copy = BuiltinFunction(self.name, self.father)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def is_equals(self, other):
        if isinstance(other, BuiltinFunction):
            return Number(1), None
        else:
            return Number(0), None

    @staticmethod
    def boolean():
        return Number(1)

    @staticmethod
    def length():
        return -1

    def __repr__(self):
        return (f"<builtin.function '{self.name}' @ "
                f"{id(f'{self.name}')}>")


println = BuiltinFunction.println = BuiltinFunction("println", None)
readline = BuiltinFunction.readline = BuiltinFunction("readline", None)
len_ = BuiltinFunction.len = BuiltinFunction("len", None)
int_ = BuiltinFunction.int = BuiltinFunction("int", None)
str_ = BuiltinFunction.str = BuiltinFunction("str", None)
float_ = BuiltinFunction.float = BuiltinFunction("float", None)
bool_ = BuiltinFunction.bool = BuiltinFunction("bool", None)
array = BuiltinFunction.array = BuiltinFunction("array", None)
run_ = BuiltinFunction.run_ = BuiltinFunction("run", None)


class Context:
    def __init__(self, display_name, parent=None, entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = entry_pos
        self.symbol_table = None


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value, father=None):
        def father_dict(d, iter_list, name, value):
            current_dict = d

            for i, key in enumerate(iter_list):
                if key not in current_dict:
                    current_dict[key] = {}
                current_dict = current_dict[key]

            current_dict[name] = value

            return d
        if father is None:
            self.symbols[name] = value
        elif isinstance(father, list):
            self.symbols = father_dict(self.symbols, father, name, value)
        else:
            raise Exception("father should be list")

    def remove(self, name):
        del self.symbols[name]


ESCAPE = {
    "Number": Number,
    "String": String,
    "Structure": Structure,
    "Cluster": Cluster,
    "Array": Array,
    "Function": Function,
    "BuiltinFunction": BuiltinFunction,
    "Library": Library,
}


class Interpreter:
    def visit(self, node, context, father):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context, father)

    def no_visit_method(self, node, context, father):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    @staticmethod
    def visit_StringNode(node, context, father):
        return Parser.RTResult().success(String(node.tok.value).set_pos(node.pos_start, node.pos_end))

    @staticmethod
    def visit_NumberNode(node, context, father):
        return Parser.RTResult().success(Number(node.tok.value).set_pos(node.pos_start, node.pos_end))

    def visit_ClusterNode(self, node, context, father):
        res = Parser.RTResult()
        cluster = []

        for cluster_node in node.cluster_nodes:
            cluster.append(res.register(self.visit(cluster_node, context, father)))
            if res.should_return(): return res

        return res.success(Null())

    def visit_ArrayNode(self, node, context, father):
        res = Parser.RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context, father)))
            if res.should_return(): return res

        return res.success(Array(elements).set_pos(node.pos_start, node.pos_end))

    def visit_StructureNode(self, node, context, father):
        res = Parser.RTResult()
        structure = []

        for structure_node in node.structure_nodes:
            structure.append(res.register(self.visit(structure_node, context, father)))
            if res.should_return(): return res

        if len(structure) == 1 and isinstance(structure[0], Number):
            return res.success(Number(Number(0).get_num(str(structure[0]))).set_pos(node.pos_start, node.pos_end))
        elif len(structure) == 1 and isinstance(structure[0], String):
            return res.success(String(str(structure[0])).set_pos(node.pos_start, node.pos_end))
        return res.success(Structure(structure).set_pos(node.pos_start, node.pos_end))

    @staticmethod
    def visit_IncludeNode(node, context, father):
        res = Parser.RTResult()

        lib_name = node.file_name_tok.value

        try:
            with open(f"{lib_name}.tl", "r", encoding="utf-8") as f:
                scripts = f.read()
        except FileNotFoundError:
            return Parser.RTResult().failure(
                Error.InvalidValueError(
                    node.pos_start, node.pos_end,
                    f"'{lib_name}' is not a module or library"
                )
            )
        error = execute(f"<shell>", scripts, [lib_name], False)

        if error:
            return Parser.RTResult().failure(
                Error.RunningTimeError(
                    node.pos_start, node.pos_end,
                    f"Failed to load '{lib_name}'\n\n"
                    f"During this error, discover another error:\n\n"
                    f"{error}"
                )
            )
        context.symbol_table.set(lib_name, Library(lib_name).set_pos(node.pos_start, node.pos_end), [lib_name])

        return res.success(Null())

    def visit_FatherCallChildNode(self, node, context, father):
        res = Parser.RTResult()

        father_tok_list = node.father_list
        father_list = []
        for ftl in father_tok_list:
            father_list.append(ftl.value)
        child = res.register(self.visit(node.child_tok, context, father_list))
        if res.should_return(): return res

        return res.success(child)

    @staticmethod
    def visit_VarAccessNode(node, context, father):
        res = Parser.RTResult()
        var_name = node.var_name_tok.value
        if father is None:
            value = context.symbol_table.get(var_name)
            if value is None:
                return res.failure(
                    Error.DefinedError(
                        node.pos_start, node.pos_end,
                        f"'{var_name}' is not defined")
                )
            value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        else:
            symbol = context.symbol_table.symbols
            for f in father:
                try:
                    symbol = symbol[f]
                except KeyError:
                    return res.failure(
                        Error.DefinedError(
                            node.pos_start, node.pos_end,
                            f"'{f}' is not defined")
                    )
            try:
                value = symbol[var_name]
            except KeyError:
                return res.failure(
                    Error.DefinedError(
                        node.pos_start, node.pos_end,
                        f"'{var_name}' is not defined")
                )
        return res.success(value)

    def visit_VarAssignNode(self, node, context, father):
        res = Parser.RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context, father))
        if isinstance(value, Null):
            ESCAPE.update({"Null": value.type})
        if res.should_return(): return res
        context.symbol_table.set(var_name, value.get() if isinstance(value, Null) else value, father)
        return res.success(
            Null(
                ESCAPE[str(type(value).__name__)],
                value.get() if isinstance(value, Null) else value))

    @staticmethod
    def visit_DeleteNode(node, context, father):
        res = Parser.RTResult()
        var_name = node.var_name_tok.value
        if node.var_name_tok.value not in context.symbol_table.symbols:
            return res.failure(
                Error.DefinedError(
                    node.pos_start, node.pos_end,
                    f"'{var_name}' is not defined")
            )
        context.symbol_table.remove(var_name)
        return res.success(Null())

    def visit_IfNode(self, node, context, father):
        res = Parser.RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context, father))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context, father))
                if res.should_return(): return res
                return res.success(Null() if should_return_null else expr_value)

        if node.else_cases:
            expr, should_return_null = node.else_cases
            expr_value = res.register(self.visit(expr, context, father))
            if res.should_return(): return res
            return res.success(Null() if should_return_null else expr_value)

        return res.success(Null())

    def visit_ForNode(self, node, context, father):
        res = Parser.RTResult()

        start_value = res.register(self.visit(node.start_value_node, context, father))
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context, father))
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context, father))
            if res.should_return(): return res
        else:
            step_value = Number(1)

        i = int(start_value.value)

        if int(step_value.value) >= 0:
            condition = lambda: i < int(end_value.value) + 1
        else:
            condition = lambda: i + 1 > int(end_value.value)

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i), father)
            i += int(step_value.value)

            res.register(self.visit(node.body_node, context, father))
            if res.should_return() and \
                res.loop_should_break is False and res.loop_should_continue is False: return res

            if res.loop_should_break:
                break
            if res.loop_should_continue:
                continue

        return res.success(Null())

    def visit_RepeatNode(self, node, context, father):
        res = Parser.RTResult()

        while True:
            condition = res.register(self.visit(node.condition_node, context, father))
            if res.should_return(): return res

            if node.type == "until" and condition.is_true():
                break
            elif node.type == "meet" and not condition.is_true():
                break

            res.register(self.visit(node.body_node, context, father))
            if res.should_return() and \
                res.loop_should_break is False and res.loop_should_continue is False: return res
            if res.loop_should_break:
                break
            if res.loop_should_continue:
                continue

        return res.success(Null())

    @staticmethod
    def visit_BreakNode(node, context, father):
        return Parser.RTResult().success_break()

    @staticmethod
    def visit_ContinueNode(node, context, father):
        return Parser.RTResult().success_continue()

    @staticmethod
    def visit_FunctionDefinedNode(node, context, father):
        res = Parser.RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(
            func_name, body_node, arg_names, node.should_auto_return, father
        ).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value, father)
        return res.success(Null())

    def visit_CallFunctionNode(self, node, context, father):
        res = Parser.RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context, father))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context, father)))
            if res.should_return(): return res
        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        if isinstance(return_value, Null):
            return res.success(Null())
        else:
            try:
                return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
            except Exception:
                return res.success(Null())
        return res.success(return_value)

    def visit_ReturnNode(self, node, context, father):
        res = Parser.RTResult()
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context, father))
            if res.should_return(): return res
        else:
            value = Null()
        return res.success_return(value)

    def visit_BindOperationNode(self, node, context, father):
        res = Parser.RTResult()
        left = res.register(self.visit(node.left_node, context, father))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context, father))
        if res.should_return(): return res
        if node.op_tok.type == Token.TCP_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == Token.TCP_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == Token.TCP_MUL:
            result, error = left.multi_by(right)
        elif node.op_tok.type == Token.TCP_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == Token.TCP_INTEGER_DIV:
            result, error = left.intdived_by(right)
        elif node.op_tok.type == Token.TCP_POW:
            result, error = left.powered_by(right)
        elif node.op_tok.type == Token.TCP_MOD:
            result, error = left.modded_by(right)

        elif node.op_tok.type == Token.TLP_DOUBLE_EQUAL:
            result, error = left.is_equals(right)
        elif node.op_tok.type == Token.TLP_GREATER:
            result, error = left.is_greater(right)
        elif node.op_tok.type == Token.TLP_GREATER_EQUAL:
            result, error = left.is_greater_equals(right)
        elif node.op_tok.type == Token.TLP_LESS:
            result, error = left.is_less(right)
        elif node.op_tok.type == Token.TLP_LESS_EQUAL:
            result, error = left.is_less_equals(right)
        elif node.op_tok.type == Token.TLP_NOT_EQUAL:
            result, error = left.is_not_equals(right)

        elif node.op_tok.matches(Token.TTT_KEYWORD, "and"):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(Token.TTT_KEYWORD, "or"):
            result, error = left.ored_by(right)

        else:
            result, error = (0,
                             Error.RunningTimeError(
                                 node.pos_start, node.pos_end,
                                 f"Not supported pos type '{node.op_tok.type}'"))
        if error is not None:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOperationNode(self, node, context, father):
        res = Parser.RTResult()
        number = res.register(self.visit(node.node, context, father))
        if res.should_return(): return res

        error = None
        if node.op_tok.type == Token.TCP_MINUS:
            number, error = number.multi_by(Number(-1))
        elif node.op_tok.matches(Token.TTT_KEYWORD, "not"):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))


global_symbol_table = SymbolTable()
global_symbol_table.set("null", null)
global_symbol_table.set("true", true)
global_symbol_table.set("false", false)

global_symbol_table.set("println", println)
global_symbol_table.set("readline", readline)

global_symbol_table.set("int", int_)
global_symbol_table.set("float", float_)
global_symbol_table.set("string", str_)
global_symbol_table.set("boolean", bool_)
global_symbol_table.set("array", array)

global_symbol_table.set("length", len_)
global_symbol_table.set("run", run_)


def execute(fn, syntax, father=None, return_result=True):
    # 获取Token
    error, tokens = Token.Lexer(fn, syntax).make_tokens()
    if error is not None: return error.as_string()
    if tokens[0].type == Token.TTT_EOF: return None

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table

    # 生成AST
    parser = Parser.Parser(tokens, fn, context)
    ast = parser.parse()
    if ast.error: return ast.error.as_string()

    # 解释器
    result = interpreter.visit(ast.node, context, father)
    if not result.error:
        if isinstance(result.value.elements[0], Null):
            return None
        else:
            if return_result:
                return result.value
            else:
                return None
    else:
        return result.error.as_string()
