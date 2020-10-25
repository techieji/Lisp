import re
from forbiddenfruit import curse
from types import CellType
import operator as op

env = CellType({
    "+": op.add, "-": op.sub, "*": op.mul, "/": op.truediv
})

def augAndExec(augumented, execute=lambda: None, rev=True):
    before = env.cell_contents
    env.cell_contents = {**before, **augumented}
    execute()
    if rev: env.cell_contents = before

def _transform(element):
    try: return int(element)
    except:
        try: return float(element)
        except: return element

curse(str, "regex", lambda x, y, z: re.sub(y, z, x))
parse = lambda t: eval("(" + t.regex(r'".*"', lambda x: f"(string {x.group(0)[1:-1]})").regex(r"\s", lambda x: " ").regex(r"[^\(\) ]+", lambda x: f"'{x.group(0)}',").regex(r"\)+", lambda x: x.group(0) + ",")[:-1] + ")")
def rmap(f, l): yield from (tuple(rmap(f, x)) if type(x) is tuple else f(x) for x in l)
def transform(parseOut): return tuple(rmap(_transform, parseOut))

def run(inp):
    if type(inp) != tuple: return inp
    (op, *args) = inp
    if op == "define": return augAndExec(args[0], run(args[1]))  # Add special case later
    elif op == "if":
        if run(inp[0]): return inp


print(transform(parse("(hello (world of (mine 1 1.0)))")))