import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Token
import Error
import Interpreter


class BindOperationNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOperationNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"


# 数字节点
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


# 字符串节点
class StringNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


# 数组节点
class ArrayNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end


# 簇节点
class ClusterNode:
    def __init__(self, cluster_nodes, pos_start, pos_end):
        self.cluster_nodes = cluster_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end


# 结构节点
class StructureNode:
    def __init__(self, structure_nodes, pos_start, pos_end):
        self.structure_nodes = structure_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end


# 变量节点
class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


# 操作变量节点
class DeleteNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


# 条件判断节点
class IfNode:
    def __init__(self, cases, else_cases):
        self.cases = cases
        self.else_cases = else_cases

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_cases or self.cases[len(self.cases) - 1][0]).pos_end


# 循环节点
class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end


class RepeatNode:
    def __init__(self, condition_node, body_node, type_: str):
        self.condition_node = condition_node
        self.body_node = body_node
        self.type = type_

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end


# 函数节点
class FunctionDefinedNode:
    def __init__(self, var_name_tok, arg_name_tokens, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_tokens
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end


class CallFunctionNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
            

# 关键字节点
# 返回节点
class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return
        
        self.pos_start = pos_start
        self.pos_end = pos_end


class ParserResult:
    def __init__(self):
        self.error = None
        self.node = None

        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


class RTResult:
    def __init__(self):
        self.value = None
        self.error = None
        self.function_return_value = None
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.function_return_value = None

    def register(self, res):
        if res.error: self.error = res.error
        self.function_return_value = res.function_return_value
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.function_return_value = value
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return (
            self.error or
            self.function_return_value
        )


class Parser:
    def __init__(self, tokens: list, run_mode: str, context):
        self.current_tok = None

        self.run_mode = run_mode
        self.context = context
        self.tokens = tokens

        self.tok_idx = -1

        self.advanced()

    def advanced(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if len(self.tokens) > self.tok_idx >= 0:
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != Token.TTT_EOF:
            return res.failure(
                Error.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                    "expected '+', '-', '*', '/', '**', '==', '!=', '<', '>', '<=', '>='"))
        return res

    def factor(self):
        res = ParserResult()
        tok = self.current_tok

        if tok.type in (Token.TCP_PLUS, Token.TCP_PLUS):
            res.register_advancement()
            self.advanced()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOperationNode(tok, factor))

        return self.power()

    def builder(self):
        res = ParserResult()
        tok = self.current_tok

        # 对数字的判断
        if tok.type in (Token.TTT_INT, Token.TTT_FLOAT):
            res.register_advancement()
            self.advanced()
            return res.success(NumberNode(tok))

        # 对字符串的判断
        elif tok.type == Token.TTT_STR:
            res.register_advancement()
            self.advanced()
            return res.success(StringNode(tok))

        # 对标识符的判断
        elif tok.type == Token.TTT_IDENTIFIER:
            res.register_advancement()
            self.advanced()
            # 三元运算符
            if self.current_tok.type == Token.TLP_WHETHER:
                res.register_advancement()
                self.advanced()

                left_value = res.register(self.expr())
                if res.error: return res

                if self.current_tok.type != Token.TTP_COLON:
                    return res.failure(Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "expected ':'"))
                res.register_advancement()
                self.advanced()

                right_value = res.register(self.expr())
                if res.error: return res

                var_result = Interpreter.Interpreter().visit(VarAccessNode(tok), self.context)
                if int(str(var_result.value.boolean())):
                    ternary_result = left_value
                else:
                    ternary_result = right_value

                # 处理节点
                if "tok" not in dir(ternary_result):
                    ternary_result = Interpreter.Interpreter().visit(ternary_result, self.context).value
                    error, tokens = Token.Lexer("<shell>", str(ternary_result.value)).make_tokens()
                    if error is not None: return error.as_string()
                    parser = Parser(tokens, "<shell>", self.context)
                    ast = parser.parse()
                    if ast.error: return ast.error.as_string()
                    ternary_result = ast.node

                if ternary_result.tok.type in (Token.TTT_INT, Token.TTT_FLOAT):
                    return res.success(NumberNode(ternary_result.tok))
                elif ternary_result.tok.type == Token.TTT_STR:
                    return res.success(StringNode(ternary_result.tok))
                elif ternary_result.tok.type == Token.TTT_STRUCTURE:
                    return res.success(StructureNode(ternary_result.tok))
                elif ternary_result.tok.type == Token.TTT_ARRAY:
                    return res.success(ArrayNode(ternary_result.tok))
                elif ternary_result.tok.type == Token.TTT_CLUSTER:
                    return res.success(ClusterNode(ternary_result.tok))
                else:
                    return res.failure(Error.InvalidTypeError(
                        ternary_result.tok.pos_start, ternary_result.tok.pos_end,
                        f"Not supported type '{type(ternary_result.tok.value).__name__}' for 'ternary'"
                    ))
            elif self.current_tok.type == Token.TTP_AS:
                res.register_advancement()
                self.advanced()

                identifier = self.current_tok
                if res.error: return res

                res.register_advancement()
                self.advanced()
                return res.success(VarAssignNode(identifier, VarAccessNode(tok)))

            return res.success(VarAccessNode(tok))

        # 对结构的判断
        elif tok.type == Token.TTT_STRUCTURE:
            structure_expr = res.register(self._include_expr(StructureNode, Token.TTP_COMMA))
            if res.error: return res
            return res.success(structure_expr)

        # 数组
        elif tok.type == Token.TTT_ARRAY:
            array_expr = res.register(self._include_expr(ArrayNode, Token.TTP_COMMA))
            if res.error: return res
            return res.success(array_expr)

        # 代码簇
        elif tok.type == Token.TTT_CLUSTER:
            cluster_expr = res.register(self._include_expr(ClusterNode, Token.TTP_SEMI))
            if res.error: return res
            return res.success(cluster_expr)

        # 关键字
        # 对if的判断
        elif self.current_tok.matches(Token.TTT_KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        # 对循环的判断
        elif self.current_tok.matches(Token.TTT_KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif self.current_tok.matches(Token.TTT_KEYWORD, "repeat"):
            repeat_expr = res.register(self.repeat_expr())
            if res.error: return res
            return res.success(repeat_expr)

        # 对函数的判断
        elif self.current_tok.matches(Token.TTT_KEYWORD, "function"):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        elif self.current_tok.matches(Token.TTT_KEYWORD, "delete"):
            delete_expr = res.register(self.delete_expr())
            if res.error: return res
            return res.success(DeleteNode(delete_expr))

        return res.failure(
            Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected type 'int' or 'float'"
            )
        )

    def power(self):
        return self.bin_op(self.call, (Token.TCP_POW,), self.factor)

    def term(self):
        return self.bin_op(self.factor, (Token.TCP_MUL, Token.TCP_DIV, Token.TCP_INTEGER_DIV, Token.TCP_MOD))

    def arith_expr(self):
        return self.bin_op(self.term, (Token.TCP_PLUS, Token.TCP_MINUS))

    def comp_expr(self):
        res = ParserResult()
        if self.current_tok.matches(Token.TTT_KEYWORD, "not"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advanced()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOperationNode(op_tok, node))

        node = res.register(self.bin_op(
            self.arith_expr,
            (Token.TLP_DOUBLE_EQUAL, Token.TLP_NOT_EQUAL,
                Token.TLP_LESS, Token.TLP_LESS_EQUAL,
                Token.TLP_GREATER, Token.TLP_GREATER_EQUAL)))
        if res.error:
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "expected int, float, '+', '-', 'not'"))

        return res.success(node)

    def _include_expr(self, NodeType, split_tok: str):
        res = ParserResult()

        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        original_tokens, original_idx = self.tokens, self.tok_idx
        self.tokens, self.tok_idx = self.current_tok.value, -1

        res.register_advancement()
        self.advanced()

        if self.current_tok.type != Token.TTT_EOF:
            element_nodes.append(res.register(self.statements()))
        if res.error:
            return res.failure(
                    Error.InvalidSyntaxError(
                            pos_start, self.current_tok.pos_end.copy(),
                            f"expected any syntax in {type(self.current_tok).__name__}"))

        while self.current_tok.type in (split_tok, Token.TTT_NEWLINE):
            res.register_advancement()
            self.advanced()

            element_nodes.append(res.register(self.statements()))
            if res.error: return res

        self.tokens, self.tok_idx = original_tokens, original_idx

        res.register_advancement()
        self.advanced()
        if NodeType == StructureNode:
            if len(element_nodes) == 1:
                interpreter = Interpreter.Interpreter()
                result = interpreter.visit(element_nodes[0], self.context)
                start = self.current_tok.pos_start
                end = self.current_tok.pos_end
                if isinstance(result.value, Interpreter.Number):
                    return res.success(NumberNode(result.value))
                if isinstance(result.value, Interpreter.String):
                    return res.success(StringNode(result.value))
                if isinstance(result.value, Interpreter.Structure):
                    return res.success(StructureNode(element_nodes, start, end))
                if isinstance(result.value, Interpreter.Array):
                    return res.success(ArrayNode(element_nodes, start, end))
                if isinstance(result.value, Interpreter.Cluster):
                    return res.success(ClusterNode(element_nodes, start, end))
        return res.success(NodeType(element_nodes, pos_start, self.current_tok.pos_end.copy()))

    def if_expr(self):
        res = ParserResult()
        cases = []
        else_cases = []

        if not self.current_tok.matches(Token.TTT_KEYWORD, "if"):
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected 'if'"
            ))

        res.register_advancement()
        self.advanced()

        condition = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != Token.TTT_CLUSTER:
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected '{' (after expression)"
            ))
        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_tok.matches(Token.TTT_KEYWORD, "elseif"):
            res.register_advancement()
            self.advanced()

            condition = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type != Token.TTT_CLUSTER:
                return res.failure(Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "expected '{' (after expression)"
                ))

            expr = res.register(self.expr())

            if res.error: return res
            cases.append((condition, expr))

        if self.current_tok.matches(Token.TTT_KEYWORD, "else"):
            res.register_advancement()
            self.advanced()

            if self.current_tok.type != Token.TTT_CLUSTER:
                return res.failure(Error.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                    "expected '{' (after expression)"
                ))
            expr = res.register(self.statement())
            if res.error: return res
            else_cases = expr

        return res.success(IfNode(cases, else_cases))

    def for_expr(self):
        res = ParserResult()

        if not self.current_tok.matches(Token.TTT_KEYWORD, "for"):
            return res.failure(
                Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "expected 'for'"))

        res.register_advancement()
        self.advanced()

        if self.current_tok.type != Token.TTT_IDENTIFIER:
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "lost variable"))

        var_name = self.current_tok
        res.register_advancement()
        self.advanced()
        if not self.current_tok.matches(Token.TTT_KEYWORD, "from"):
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected 'from'"))

        res.register_advancement()
        self.advanced()
        start_value = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(Token.TTT_KEYWORD, "to"):
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected 'to'"))

        res.register_advancement()
        self.advanced()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.matches(Token.TTT_KEYWORD, "step"):
            res.register_advancement()
            self.advanced()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if self.current_tok.type != Token.TTT_CLUSTER:
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected '{' (after expression)"
            ))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def repeat_expr(self):
        res = ParserResult()

        if not self.current_tok.matches(Token.TTT_KEYWORD, "repeat"):
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected 'repeat'"
            ))

        res.register_advancement()
        self.advanced()

        type_ = self.current_tok.value
        if self.current_tok.matches(Token.TTT_KEYWORD, "until") or self.current_tok.matches(Token.TTT_KEYWORD, "meet"):
            res.register_advancement()
            self.advanced()

            condition_expr = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type != Token.TTT_CLUSTER:
                return res.failure(
                    Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "expected '{'"))

            body = res.register(self.statement())
            if res.error: return res

            return res.success(RepeatNode(condition_expr, body, str(type_)))
        else:
            return res.failure(
                Error.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                    "expected type 'Int' or keyword 'until' or 'meet'"))

    def statements(self):
        res = ParserResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == Token.TTT_NEWLINE:
            res.register_advancement()
            self.advanced()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == Token.TTT_NEWLINE:
                res.register_advancement()
                self.advanced()
                newline_count += 1
            if newline_count == 0:
                more_statements = False
            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ArrayNode(statements, pos_start, self.current_tok.pos_end.copy()))

    def statement(self):
        res = ParserResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(Token.TTT_KEYWORD, "return"):
            res.register_advancement()
            self.advanced()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_end.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(Error.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                    "expected 'return', '+', '-', '*', '/', '**', '==', '!=', '<', '>', '<=', '>='"))
        return res.success(expr)

    def expr(self):
        res = ParserResult()

        if self.current_tok.matches(Token.TTT_KEYWORD, "var"):
            res.register_advancement()
            self.advanced()

            if self.current_tok.type != Token.TTT_IDENTIFIER:
                return res.failure(
                    Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "lost variable name"
                    ),
                )
            var_name = self.current_tok
            res.register_advancement()
            self.advanced()

            if self.current_tok.type != Token.TLP_EQUAL:
                return res.failure(
                    Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "lost character '=', did you forget '='?"
                    )
                )

            res.register_advancement()
            self.advanced()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((Token.TTT_KEYWORD, "and"), (Token.TTT_KEYWORD, "or"))))
        if res.error:
            return res.failure(
                Error.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                    "expected int, float")
            )
        return res.success(node)

    def delete_expr(self):
        res = ParserResult()

        res.register_advancement()
        self.advanced()
        if self.current_tok.type != Token.TTT_IDENTIFIER:
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "lose variable name"
            ))

        var_name = self.current_tok

        res.register_advancement()
        self.advanced()

        return res.success(var_name)

    # 函数
    def func_def(self):
        res = ParserResult()

        if not self.current_tok.matches(Token.TTT_KEYWORD, "function"):
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected 'function'"))

        res.register_advancement()
        self.advanced()

        if self.current_tok.type == Token.TTT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advanced()
            if self.current_tok.type != Token.TTT_STRUCTURE:
                return res.failure(
                    Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "expected '(''")
                )
        else:
            return res.failure(Error.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                "expected function name"
            ))

        arg_name_toks = []
        if self.current_tok.type != Token.TTT_STRUCTURE:
            return res.failure(
                Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "expected '(''")
            )
        original_tokens, original_idx = self.tokens, self.tok_idx
        self.tokens, self.tok_idx = self.current_tok.value, -1

        res.register_advancement()
        self.advanced()

        if self.current_tok.type == Token.TTT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advanced()

            while self.current_tok.type == Token.TTP_COMMA:
                res.register_advancement()
                self.advanced()

                if self.current_tok.type != Token.TTT_IDENTIFIER:
                    return res.failure(Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advanced()

        self.tokens, self.tok_idx = original_tokens, original_idx

        res.register_advancement()
        self.advanced()

        if self.current_tok.type != Token.TTT_CLUSTER:
            return res.failure(
                Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "expected '{'")
            )

        node_to_return = res.register(self.expr())
        if res.error: return res

        return res.success(FunctionDefinedNode(
            var_name_tok,
            arg_name_toks,
            node_to_return,
            True
        ))

    def call(self):
        res = ParserResult()
        builder = res.register(self.builder())
        if res.error: return res

        if self.current_tok.type == Token.TTT_STRUCTURE:
            original_tokens, original_idx = self.tokens, self.tok_idx
            self.tokens, self.tok_idx = self.current_tok.value, -1

            res.register_advancement()
            self.advanced()
            arg_nodes = []
            if self.current_tok.type != Token.TTT_EOF:
                arg_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(
                    Error.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end.copy(),
                        "expected any syntax in function"))

            while self.current_tok.type == Token.TTP_COMMA:
                res.register_advancement()
                self.advanced()

                arg_nodes.append(res.register(self.expr()))
                if res.error: return res

            self.tokens, self.tok_idx = original_tokens, original_idx

            res.register_advancement()
            self.advanced()
            return res.success(CallFunctionNode(builder, arg_nodes))
        return res.success(builder)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParserResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or ((self.current_tok.type, self.current_tok.value) in ops):
            op_tok = self.current_tok
            res.register_advancement()
            self.advanced()
            right = res.register(func_b())
            if res.error: return res
            left = BindOperationNode(left, op_tok, right)

        return res.success(left)
