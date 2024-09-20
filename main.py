import Token
import Parser
import Interpreter

global_symbol_table = Interpreter.SymbolTable()
global_symbol_table.set("null", Interpreter.null)
global_symbol_table.set("true", Interpreter.true)
global_symbol_table.set("false", Interpreter.false)

global_symbol_table.set("println", Interpreter.println)
global_symbol_table.set("input", Interpreter.input_)

global_symbol_table.set("int", Interpreter.int_)
global_symbol_table.set("float", Interpreter.float_)
global_symbol_table.set("string", Interpreter.str_)
global_symbol_table.set("boolean", Interpreter.bool_)
global_symbol_table.set("array", Interpreter.array)

global_symbol_table.set("length", Interpreter.len_)


def run(syntax):
    # 获取Token
    error, tokens = Token.Lexer("<shell>", syntax).make_tokens()
    if error is not None: return error.as_string()
    if tokens[0].type == Token.TTT_EOF: return None

    interpreter = Interpreter.Interpreter()
    context = Interpreter.Context("<program>")
    context.symbol_table = global_symbol_table

    # 生成AST
    parser = Parser.Parser(tokens, "<shell>", context)
    ast = parser.parse()
    if ast.error: return ast.error.as_string()

    # 解释器
    result = interpreter.visit(ast.node, context)
    if not result.error:
        return None if isinstance(result.value, Interpreter.Null) else result.value
    else:
        return result.error.as_string()


if __name__ == "__main__":
    while True:
        syntax = str(input("Toy > "))
        if syntax.strip():
            res = run(syntax)
            if res is not None:
                print(res)
