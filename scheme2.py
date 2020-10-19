from re import sub
from forbiddenfruit import curse
from types import CellType

code = '(display ((lambda (x) (+ x 1)) 1))\n(display "That was it!")'

env = CellType({})
def define(i): env.cell_contents[i[0]] = i[1]
fns = {'+': sum, '-': lambda i: i[0] - sum(i[1:]), "if": lambda i: i[1] if i[0] else i[2], "define": define, "string": lambda i: " ".join(i)}
curse(str, "regex", lambda x, y, z: sub(y, z, x))
curse(str, "run", lambda self: eval("(" + self + ",)"))
curse(tuple, "sc", lambda self, i: (env.cell_contents[i] if i in env.cell_contents else fns[i])(self))
parse = lambda t: t.regex(r'".*"', lambda x: f"(string {x.group(0)[1:-1]})").regex(r"\s", lambda x: " ").regex(r"[^\(\) ]+", lambda x: f"'{x.group(0)}',").regex(r"\)+", lambda x: x.group(0) + ",")[:-1].run()
def run(i):
    pass

print(parse(code))