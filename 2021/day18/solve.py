def parse(exprString):
    return eval(exprString)

def depth(expr):
    if isinstance(expr, int):
        return 0

    return 1 + max(depth(expr[0]), depth(expr[1]))


def pathTo(expr, need):
    if isinstance(expr, int):
        return [] if need == 0 else None

    lpath = pathTo(expr[0], max(need - 1, 0))
    if lpath is not None:
        return [0] + lpath

    rpath = pathTo(expr[1], max(need - 1, 0))
    if rpath is not None:
        return [1] + rpath

    return None


def bignum(expr):
    if isinstance(expr, int):
        return (expr, [])

    left, leftPath = bignum(expr[0])
    right, rightPath = bignum(expr[1])

    if left >= right:
        return left, [0] + leftPath
    return right, [1] + rightPath


def reduce(expr):
    path = pathTo(expr, 5)
    if path is not None:
        return explode(expr, path)
    
    maxval, path = bignum(expr)
    if maxval >= 10:
        pass

    return expr


def add(expr1, expr2):
    return expr2 if not expr1 else reduce([expr1, expr2])


def magnitude(expr):
    if isinstance(expr, int):
        return expr
    
    return 3 * magnitude(expr[0]) + 2 * magnitude(expr[1])


def main():
    expr = None
    for _ in range(100):
        expr = add(expr, parse(input.strip()))

    print(magnitude(expr))


main()
