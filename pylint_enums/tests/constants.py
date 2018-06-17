import astroid

from pylint_enums.checker import EXCLUDED_SIMPLE_TYPES

IMPORT_TEST_CASES = (
    (astroid.extract_node('import foo'), False),
    (astroid.extract_node('import enum'), True),
    (astroid.extract_node('import foo as enum'), False),
    (astroid.extract_node('import enum as foo'), True),
    (astroid.extract_node('import foo, enum'), True),
    (astroid.extract_node('import foo, bar'), False),
    (astroid.extract_node('import foo, bar, enum as baz'), True)
)


IMPORTFROM_TEST_CASES = (
    (astroid.extract_node('from enum import Enum'), True),
    (astroid.extract_node('from enum import *'), True),
    (astroid.extract_node('from enum import EnumMeta'), False),
    (astroid.extract_node('from foo import bar'), False),
    (astroid.extract_node('from foo import bar as enum'), False)
)


CLASSDEF_TEST_CASES = (
    (astroid.extract_node("""
        class Foo(Enum): #@
            A = 'a'
            B = 'b'
    """), ('pylint-enums-no-annotated-value',)),
    *[
        (astroid.extract_node(f"""
            class Foo(Enum): #@
                value: {excluded_type}
                A = 'a'
                B = 'b'
        """), ())
        for excluded_type in EXCLUDED_SIMPLE_TYPES
    ],
    (astroid.extract_node("""
        class Foo(Enum): #@
            value: SomeNamedTuple
            A = SomeNamedTuple(a=5)
            B = SomeNamedTuple(a=6)
    """), ('pylint-enums-no-str-method',)),
    (astroid.extract_node("""
        class Foo(Enum): #@
            value: str = 'why'
            A = 'a'
            B = 'b'
            def __str__(self):
                return 'whatever'
    """), ('pylint-enums-no-assignment-to-value',)),
    (astroid.extract_node("""
        class Foo(Enum): #@
            value: str
            A = 'a'
            B = 'b'
            def __str__(self):
                return 'whatever'
    """), ()),
    (astroid.extract_node("""
        class Foo: #@
            value: str
            A = 'a'
            B = 'b'
            def __str__(self):
                return 'whatever'
    """), ()),
    (astroid.extract_node("""
        class Foo(NotEnum): #@
            value: str
            A = 'a'
            B = 'b'
            def __str__(self):
                return 'whatever'
    """), ()),
    (astroid.extract_node("""
        class Foo(NotEnum, Enum): #@
            value: str
            A = 'a'
            B = 'b'
            def __str__(self):
                return 'whatever'
    """), ())
)

ANNOTATION_NAME_TEST_CASES = (
    (astroid.extract_node("""
        class Foo(Enum):
            value: str #@
            A = 'a'
    """), 'str'),
    (astroid.extract_node("""
        class Foo(Enum):
            value: int #@
            A = 'a'
    """), 'int'),
    (astroid.extract_node("""
        class Foo(Enum):
            value: float #@
            A = 'a'
    """), 'float'),
    (astroid.extract_node("""
        class Foo(Enum):
            value: Decimal #@
            A = 'a'
    """), 'decimal'),
    (astroid.extract_node("""
        class Foo(Enum):
            value: Dict[str, str] #@
            A = 'a'
    """), 'dict'),
    (astroid.extract_node("""
        class Foo(Enum):
            value: Dict[Set[str], str] #@
            A = 'a'
    """), 'dict'),
    (astroid.extract_node("""
        class Foo(Enum):
            value: Tuple[str, ...] #@
            A = 'a'
    """), 'tuple'),
    (astroid.extract_node("""
        class Foo(Enum):
            value: List[str, ...] #@
            A = 'a'
    """), 'list'),
)
