import types

def rmap(fn, i, t=tuple): yield from [t(rmap(fn, x)) if type(x) == t else fn(x) for x in i]

def lambdafn(i):
    args = i[0]
    code = i[1:]
    def fn(reals):
        sabre = dict(zip(args, reals))
        sabrer = lambda i: sabre.get(i, i)
        return tuple(rmap(sabrer, code))
    return fn

lambdafn = lambda i: lambda reals: tuple(rmap(lambda a: dict(zip(i[0], reals)).get(a, a), i[1:]))

# def dec(tup):
#     name, f = tup
#     def fn(i):
#         if any(map(lambda x: hasattr(x, "exists"), (name,) + i)):
#             return (name,) + i
#         else:
#             return f(i)
#     return (name, fn)

dec = lambda tup: (tup[0], lambda i: (ans if any(map(lambda x: hasattr(x, "exists"), (ans := (tup[0],) + i))) else tup[1](i)))

# def dec(tup):
#     # def fn(i):
#     #     # if any(map(lambda x: hasattr(x, "exists"), (tup[0],) + i)):
#     #     #     return (tup[0],) + i
#     #     # else:
#     #     #     return tup[1](i)
#     #     return ((tup[0],) + i if any(map(lambda x: hasattr(x, "exists"), (tup[0],) + i)) else tup[1](i))
#     return (tup[0], lambda i: ((tup[0],) + i if any(map(lambda x: hasattr(x, "exists"), (tup[0],) + i)) else tup[1](i)))

def transform(d): return dict(map(dec, d.items()))

transform = lambda d: dict(map(dec, d.items()))

def getdict(env):
    def define(i): env.cell_contents[i[0]] = i[1]
    return transform({
        '+': sum, '-': lambda i: i[0] - sum(i[1:]), 
        "if": lambda i: i[1] if i[0] else i[2], 
        "define": define, 
        "string": lambda i: " ".join(i), 
        "display": lambda i: print(i[0], end=""),
        "lambda": lambdafn
    })

if __name__ == "__main__":
    def binit(self, bname): self.name, self.exists = bname, True
    def bcall(self, *args): return (self,) + tuple(args)
    bvar = type("bvar", (), {"__init__": binit, "__repr__": lambda self: f"<bound variable '{self.name}'>", "__call__": bcall})
    env = types.CellType({})
    d = getdict(env)
    x = bvar("x")
    print(d["lambda"](((x,), ("+", x, 5)))((5,)))