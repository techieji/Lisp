# @dataclass
# class atom:
#     text: str
#     typ: Any = catchall
#     def tryToPython(self):
#         if self.typ == "char":
#             return self.text
#         elif self.typ == "int":
#             return int(self.text)
#     def detType(self):
#         if re.match(integer, self.text):
#             return integer
#         elif re.match(decimal, self.text):
#             return decimal
#         elif re.match(fraction, self.text):
#             return fraction

# def flatten(l):
#     # print(l)
#     out = []
#     flag = True
#     for x in l:
#         if type(x) == list:
#             out += x
#             flag = False
#         else:
#             out.append(x)
#     if flag:
#         return out
#     else:
#         return flatten(out)

# def rmap(f, l):
#     out = []
#     for x in l:
#         if type(l) == list:
#             out.append(rmap(f, x))
#         else:
#             out.append(f(x))
#     return out
