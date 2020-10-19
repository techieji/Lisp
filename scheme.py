from dataclasses import dataclass
from typing import Any, Callable
import re

integer = re.compile(r"[0-9]+")
decimal = re.compile(r"[0-9]*\.[0-9]+")
fraction = re.compile(r"[0-9]+/[0-9]+")
catchall = re.compile(r".+")
nothing = re.compile(r"")

@dataclass
class expr:
    text: str
    inc: Callable[[str], bool] = lambda char: char == "("
    dec: Callable[[str], bool] = lambda char: char == ")"
    @staticmethod
    def isExpr(s): return s[-1] == ")" and "(" in s
    def parse(self):
        if type(self) == str: self = expr(self)
        elif type(self) != expr: return self
        level = 0
        elements = [""]
        for char in self.text:
            delta = int(self.inc(char)) - int(self.dec(char))
            if delta != 0:
                if level > 0: elements[-1] += char
                level += delta
            elif char == " " and level < 2: elements.append("")
            else: elements[-1] += char
        return list(map(lambda x: x[:-1] if x[-1] == ")" else x, elements))

def toast(s):
    if expr.isExpr(s): return [toast(x) for x in expr.parse(s)]
    else: return s

code = '((lambda (x) (+ x 1)) 1)'
print(toast(code))

@dataclass
class ev:
    ast: list
    def evaluate(self):
        pass