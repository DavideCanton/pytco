__author__ = 'Kami'

import ast
import inspect
import astunparse
from copy import copy


def bind_params(names, call_node):
    values = {}

    if len(names) != len(call_node.args):
        raise ValueError("Incorrect number of params {} (expected {})".format(
            len(call_node.args), len(names)))

    for name, arg in zip(names, call_node.args):
        values[name] = arg

    return values


class TCO_Replace(ast.NodeTransformer):
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
                  body=old, orelse=[])]
    TCO_Replace(func, t).replace_nodes()
    ast.fix_missing_locations(t)
    src = astunparse.unparse(t)
    fmt = "{}\nret={}(*args, **kwargs)"
    code = compile(fmt.format(src, func.__name__), "<string>", "exec")

    def w(*args, **kwargs):
        exec(code, globals(), locals())
        return locals()["ret"]

    return w

