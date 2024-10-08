import Interpreter


if __name__ == "__main__":
    while True:
        syntax = str(input("Toy > "))
        if syntax.strip():
            res = Interpreter.execute("<shell>", syntax)
            if res is not None:
                if isinstance(res, str):
                    print(res)
                elif isinstance(res, list):
                    print('\n'.join(res))
