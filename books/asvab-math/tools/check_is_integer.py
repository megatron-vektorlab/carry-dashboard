"""Find `x.is_integer` (no call) applied to Python float/Fraction at runtime.

sympy numbers have an `is_integer` *property*; Python floats and Fractions
have an `is_integer()` *method*, so `x.is_integer` on them is always truthy.
This script rewrites every chapter module so that each attribute access
`X.is_integer` (not followed by a call) goes through a checker, then
generates many problems from every template and reports offending lines.

    .venv/bin/python tools/check_is_integer.py
"""
import ast
import collections
import importlib
import pkgutil
import random
import sys
import types
from fractions import Fraction

sys.path.insert(0, ".")
import asvab.chapters as pkg  # noqa: E402
from asvab.core import Reject  # noqa: E402

HITS = collections.Counter()


def _chk(obj, where):
    if isinstance(obj, (float, Fraction)) or (isinstance(obj, int) and not isinstance(obj, bool) and False):
        HITS[(where, type(obj).__name__)] += 1
        return obj.is_integer()
    return obj.is_integer


class T(ast.NodeTransformer):
    def __init__(self, fname):
        self.fname = fname

    def visit_Call(self, node):
        # keep x.is_integer() calls as they are
        if isinstance(node.func, ast.Attribute) and node.func.attr == "is_integer":
            node.func.value = self.visit(node.func.value)
            node.args = [self.visit(a) for a in node.args]
            return node
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        node = self.generic_visit(node)
        if node.attr == "is_integer" and isinstance(node.ctx, ast.Load):
            return ast.copy_location(ast.Call(
                func=ast.Name("__chk_is_int", ast.Load()),
                args=[node.value, ast.Constant(f"{self.fname}:{node.lineno}")], keywords=[]), node)
        return node


def main():
    for info in pkgutil.iter_modules(pkg.__path__):
        if not info.name.startswith("ch"):
            continue
        name = f"{pkg.__name__}.{info.name}"
        orig = importlib.import_module(name)
        src = open(orig.__file__).read()
        tree = ast.fix_missing_locations(T(info.name).visit(ast.parse(src)))
        mod = types.ModuleType(name)
        mod.__file__ = orig.__file__
        mod.__package__ = pkg.__name__
        mod.__dict__["__chk_is_int"] = _chk
        sys.modules[name] = mod
        exec(compile(tree, orig.__file__, "exec"), mod.__dict__)
        rng = random.Random(5)
        for tpl, lvl, _ in mod.PLAN:
            for _ in range(150):
                try:
                    tpl(rng, lvl)
                except Reject:
                    pass
                except Exception as e:  # noqa: BLE001
                    HITS[(f"{info.name}.{tpl.__name__}", f"EXC {type(e).__name__}: {e}"[:80])] += 1
    for (where, typ), c in sorted(HITS.items()):
        print(f"{where:<45} {typ:<12} x{c}")
    print(f"{len(HITS)} location(s)")


if __name__ == "__main__":
    main()
