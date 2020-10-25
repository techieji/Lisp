import re, copy, types, forbiddenfruit

env = types.CellType({})
def copyswitch(prenv): env.cell_contents = prenv
def dummy(*args, **kwargs): return args[kwargs["i"]]
def rmap(fn, i, t=tuple): yield from [t(rmap(fn, x)) if type(x) == t else fn(x) for x in i]
def define(i): env.cell_contents[i[0]] = i[1]
def safe(fn, *args, **kwargs):
    try: return fn(*args)
    except: return kwargs["default"]

def binit(self, bname): self.name, self.exists = bname, True
def bcall(self, *args): return (self,) + tuple(args)
bvar = type("bvar", (), {"__init__": binit, "__repr__": lambda self: f"<bound variable '{self.name}'>", "__call__": bcall})
fns = (lambda d: dict(map(lambda tup: (tup[0], lambda i: (ans if any(map(lambda x: hasattr(x, "exists"), (ans := (tup[0],) + i))) else tup[1](i))), d.items())))({'+': sum, '-': lambda i: i[0] - sum(i[1:]), "if": lambda i: i[1] if i[0] else i[2], "define": define, "string": lambda i: " ".join(i), "display": lambda i: print(i[0], end=""), "run": lambda c: [k for x in c if (k := (lambda i: tuple(map(lambda x: dummy((prenv := env.cell_contents), copyswitch(copy.copy(prenv)), runln(x), copyswitch(prenv), i=2), i[1:])).sc(runln(i[0])) if type(i) == tuple else (env.cell_contents[i] if i in env.cell_contents else safe(lambda: eval(i, {}, {}), default=i)))(x)) != None], "lambda": lambda i: lambda reals: fns["run"](tuple(rmap(lambda a: dict(zip(i[0], reals)).get(a, a), i[1:])))})
parse = lambda t: t.regex(r'".*"', lambda x: f"(string {x.group(0)[1:-1]})").regex(r"\s", lambda x: " ").regex(r"[^\(\) ]+", lambda x: f"'{x.group(0)}',").regex(r"\)+", lambda x: x.group(0) + ",")[:-1].run()
runln = lambda i: tuple(map(lambda x: dummy((prenv := env.cell_contents), copyswitch(copy.copy(prenv)), runln(x), copyswitch(prenv), i=2), i[1:])).sc(runln(i[0])) if type(i) == tuple else (env.cell_contents[i] if i in env.cell_contents else (fns[i] if i in fns else safe(lambda: eval(i, {}, {}), default=i)))
run = lambda c: [k for x in c if (k := runln(x)) != None]
def expose(): globals().update(env.cell_contents)
forbiddenfruit.curse(str, "regex", lambda x, y, z: re.sub(y, z, x))
forbiddenfruit.curse(str, "run", lambda self: eval("(" + self + ",)"))
forbiddenfruit.curse(tuple, "sc", lambda self, i: safe(lambda: (ans if (ans := env.cell_contents.get(i)) else (ans if (ans := fns.get(i)) else bvar(i))(self)), default=(i,) + self))


# code = '(display ((lambda (x) (+ x 1)) 1))\n(newline)\n(display "That was it!")'
code = '(define inc (lambda (x) (+ x 1)))'
print(run(parse(code)))
expose()
print(run(inc((5,))))