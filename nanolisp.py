import re
from forbiddenfruit import curse

curse(str, "regex", lambda x, y, z: re.sub(y, z, x))
parse = lambda t: eval("(" + t.regex(r'".*"', lambda x: f"(string {x.group(0)[1:-1]})").regex(r"\s", lambda x: " ").regex(r"[^\(\) ]+", lambda x: f"'{x.group(0)}',").regex(r"\)+", lambda x: x.group(0) + ",")[:-1] + ")")

class obj:
    __slots__ = ("args", "repr")
    def __init__(self, args): 
        self.args = args

    def __repr__(self):
        try: 
            return str(self.toPy())
        except NotImplementedError:
            return str(self.args)

    def __str__(self):
        return repr(self)
    
    def toPy(self): 
        raise NotImplementedError
    
    @staticmethod
    def sub(toPy):
        class T(obj):
            def __init__(self, val): 
                super().__init__(val)
            def toPy(self): 
                return toPy(self)
        return T

alist      = obj.sub(lambda i: dict(zip(i.args[0::2], i.args[1::2])))
boolean    = obj.sub(lambda i: i.args[0] == "#t")
byte       = obj.sub(lambda i: i.args[0])
bytevector = obj.sub(lambda i: i.args)
char       = obj.sub(lambda i: i.args[0])
li         = obj.sub()
pair       = obj.sub(lambda i: i.args)

print(boolean(["#t"]))