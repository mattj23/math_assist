import sympy
import inspect


def main():
    # for name, item in inspect.getmembers(sympy):
    #     if inspect.isclass(item):
    #         if issubclass(item, sympy.Expr):
    #             print(name, item)

    for item in sympy.Expr.__subclasses__():
        print(item)



if __name__ == '__main__':
    main()
