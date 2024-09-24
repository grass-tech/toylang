import Interpreter


if __name__ == "__main__":
    while True:
        syntax = str(input("Toy > "))
        if syntax.strip():
            res = Interpreter.execute("<shell>", syntax)
            if res is not None:
                if isinstance(res, str):
                    print(res)
                    continue
                if len(res.elements) == 1:
                    print(res.elements[0])
                else:
                    print(repr(res))
