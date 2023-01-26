import sys
import tempfile
from pathlib import Path

import typeshed_client

import stubdefaulter

PY_FILE = """
import enum
import re

def f(x=0, y="y", z=True, a=None):
    pass
def more_ints(x=-1, y=0):
    pass
def ints_as_hexadecimals(x=0x7FFFFFFF, y=0b1101, z=0o744):
    pass
def wrong_default(wrong=0):
    pass
def floats(a=1.23456, b=0.0, c=-9.87654, d=-0.0):
    pass
def float_edge_cases(one=float("nan"), two=float("inf"), three=float("-inf")):
    pass
def complex_function_with_complex_defaults(
    a=3j,
    b=-3j,
    c=3.14j,
    d=-3.14j,
    e=1+3j,
    f=1+3.14j,
    g=1-3j,
    h=1-3.14j,
    i=-1+3j,
    k=-1-3j,
    l=-1+3.14j,
    m=-1-3.14j,
    n=3.14+3j,
    o=3.14-3j,
    p=3.14+3.14j,
    q=3.14-3.14j,
    r=-3.14+3j,
    s=-3.14-3j,
    t=-3.14+3.14j,
    u=-3.14-3.14j,
):
    pass

class Capybara:
    def __init__(self, x=0, y="y", z=True, a=None):
        pass
    def overloaded_method(x=False):
        return 1 if x else "1"

class Klass:
    class NestedKlass1:
        class NestedKlass2:
            def method(self, a=False):
                pass
            async def async_method(self, b=3.14):
                pass

def overloaded(x=False):
    return 1 if x else "1"

def intenum_default(x=re.ASCII):
    return int(x)

class FooEnum(str, enum.Enum):
    FOO = "foo"

def strenum_default(x=FooEnum.FOO):
    return str(x)
"""
INPUT_STUB = """
import enum
import re
from typing import overload, Literal

def f(x: int = ..., y: str = ..., z: bool = ..., a: Any = ...) -> None: ...
def more_ints(x: int = ..., y: bool = ...) -> None: ...
def ints_as_hexadecimals(x: int = 0x7FFFFFFF, y=0b1101, z=0o744) -> None: ...
def wrong_default(wrong: int = 1) -> None: ...
def floats(a: float = ..., b: float = ..., c: float = ..., d: float = ...) -> None: ...
def float_edge_cases(one: float = ..., two: float = ..., three: float = ...) -> None: ...
def complex_function_with_complex_defaults(
    a: complex = ...,
    b: complex = ...,
    c: complex = ...,
    d: complex = ...,
    e: complex = ...,
    f: complex = ...,
    g: complex = ...,
    h: complex = ...,
    i: complex = ...,
    k: complex = ...,
    l: complex = ...,
    m: complex = ...,
    n: complex = ...,
    o: complex = ...,
    p: complex = ...,
    q: complex = ...,
    r: complex = ...,
    s: complex = ...,
    t: complex = ...,
    u: complex = ...,
) -> None: ...

class Capybara:
    def __init__(self, x: int = ..., y: str = ..., z: bool = ..., a: Any = ...) -> None: ...
    @overload
    def overloaded_method(x: Literal[False] = ...) -> str: ...
    @overload
    def overloaded_method(x: Literal[True]) -> int: ...

class Klass:
    class NestedKlass1:
        class NestedKlass2:
            def method(self, a: bool = ...) -> None: ...
            async def async_method(self, b: float = ...) -> None: ...

@overload
def overloaded(x: Literal[False] = ...) -> str: ...
@overload
def overloaded(x: Literal[True]) -> int: ...

def intenum_default(x: int = ...) -> int: ...

class FooEnum(str, enum.Enum):
    FOO: str

def strenum_default(x: str = ...) -> str: ...
"""
EXPECTED_STUB = """
import enum
import re
from typing import overload, Literal

def f(x: int = 0, y: str = 'y', z: bool = True, a: Any = None) -> None: ...
def more_ints(x: int = -1, y: bool = ...) -> None: ...
def ints_as_hexadecimals(x: int = 0x7FFFFFFF, y=0b1101, z=0o744) -> None: ...
def wrong_default(wrong: int = 1) -> None: ...
def floats(a: float = 1.23456, b: float = 0.0, c: float = -9.87654, d: float = -0.0) -> None: ...
def float_edge_cases(one: float = ..., two: float = ..., three: float = ...) -> None: ...
def complex_function_with_complex_defaults(
    a: complex = 3j,
    b: complex = -3j,
    c: complex = 3.14j,
    d: complex = -3.14j,
    e: complex = 1 + 3j,
    f: complex = 1 + 3.14j,
    g: complex = 1 - 3j,
    h: complex = 1 - 3.14j,
    i: complex = -1 + 3j,
    k: complex = -1 - 3j,
    l: complex = -1 + 3.14j,
    m: complex = -1 - 3.14j,
    n: complex = 3.14 + 3j,
    o: complex = 3.14 - 3j,
    p: complex = 3.14 + 3.14j,
    q: complex = 3.14 - 3.14j,
    r: complex = -3.14 + 3j,
    s: complex = -3.14 - 3j,
    t: complex = -3.14 + 3.14j,
    u: complex = -3.14 - 3.14j,
) -> None: ...

class Capybara:
    def __init__(self, x: int = 0, y: str = 'y', z: bool = True, a: Any = None) -> None: ...
    @overload
    def overloaded_method(x: Literal[False] = False) -> str: ...
    @overload
    def overloaded_method(x: Literal[True]) -> int: ...

class Klass:
    class NestedKlass1:
        class NestedKlass2:
            def method(self, a: bool = False) -> None: ...
            async def async_method(self, b: float = 3.14) -> None: ...

@overload
def overloaded(x: Literal[False] = False) -> str: ...
@overload
def overloaded(x: Literal[True]) -> int: ...

def intenum_default(x: int = ...) -> int: ...

class FooEnum(str, enum.Enum):
    FOO: str

def strenum_default(x: str = ...) -> str: ...
"""
PKG_NAME = "pkg"


def test_stubdefaulter() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        sys.path.append(tmpdir)
        td = Path(tmpdir)
        pkg_path = td / PKG_NAME
        pkg_path.mkdir()
        stub_path = pkg_path / "__init__.pyi"
        stub_path.write_text(INPUT_STUB)
        (pkg_path / "__init__.py").write_text(PY_FILE)
        (pkg_path / "py.typed").write_text("typed\n")

        errors, _ = stubdefaulter.add_defaults_to_stub(
            PKG_NAME, typeshed_client.finder.get_search_context(search_path=[td])
        )
        assert stub_path.read_text() == EXPECTED_STUB
        assert len(errors) == 1

        stub_path.write_text(INPUT_STUB.replace(" = 1", " = ..."))
        errors, _ = stubdefaulter.add_defaults_to_stub(
            PKG_NAME, typeshed_client.finder.get_search_context(search_path=[td])
        )
        assert stub_path.read_text() == EXPECTED_STUB.replace(
            "wrong: int = 1", "wrong: int = 0"
        )
        assert len(errors) == 0
