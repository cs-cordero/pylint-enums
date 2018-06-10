import astroid

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
    """), ('pylint-enums-no-annotated-value', 'pylint-enums-no-str-method')),
    (astroid.extract_node("""
        class Foo(Enum): #@
            value: str
            A = 'a'
            B = 'b'
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
