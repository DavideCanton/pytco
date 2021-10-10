import ast
import inspect
import astunparse
from copy import copy

__author__ = 'Kami'


def bind_params(names, call_node):
    values = {}

    if len(names) != len(call_node.args):
        raise ValueError(f"Incorrect number of params {len(call_node.args)} (expected {len(names)})")

    for name, arg in zip(names, call_node.args):
        values[name] = arg

    return values


class TcoReplace(ast.NodeTransformer):
    def __init__(self, func, node):
        self.name = node.body[0].name
        self.node = node
        self.func = func

    def replace_nodes(self):
        self.visit(self.node)

    def visit_Return(self, node):
        if isinstance(node.value, ast.Call):
            fun_name = node.value.func.id

            if fun_name == self.name:
                names = [n.arg for n in self.node.body[0].args.args]
                params = bind_params(names, node.value)

                tl, tr = [], []
                for k, v in params.items():
                    tl.append(ast.Name(id=k, ctx=ast.Store()))
                    tr.append(v)

                tl = ast.Tuple(elts=tl, ctx=ast.Store())
                tr = ast.Tuple(elts=tr, ctx=ast.Load())
                assign = ast.Assign(targets=[tl], value=tr)
                return [assign, ast.Continue()]

        return node


def tco(func):
    s = inspect.getsource(func)
    t = ast.parse(s)
    t.body[0].decorator_list = []
    old = t.body[0].body
    t.body[0].body = [
        ast.While(test=ast.Name(id='True', ctx=ast.Load()),
                  body=old,
                  orelse=[])
    ]
    TcoReplace(func, t).replace_nodes()
    ast.fix_missing_locations(t)
    src = astunparse.unparse(t)
    fmt = f"{src}\nret={func.__name__}(*args, **kwargs)"
    code = compile(fmt, "<string>", "exec")

    def w(*args, **kwargs):
        exec(code, globals(), locals())
        return locals()["ret"]

    return w
