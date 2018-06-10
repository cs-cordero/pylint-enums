import astroid
import pylint.testutils
import pytest

import checker

# tuples of (astroid_node, whether enum has been imported)
import_test_cases = (
    (astroid.extract_node('import foo'), False),
    (astroid.extract_node('import enum'), True),
    (astroid.extract_node('import foo as enum'), False),
    (astroid.extract_node('import enum as foo'), True),
    (astroid.extract_node('import foo, enum'), True),
    (astroid.extract_node('import foo, bar'), False),
    (astroid.extract_node('import foo, bar, enum as baz'), True)
)
importFrom_test_cases = (
    (astroid.extract_node('from enum import Enum'), True),
    (astroid.extract_node('from enum import *'), True),
    (astroid.extract_node('from enum import EnumMeta'), False),
    (astroid.extract_node('from foo import bar'), False),
    (astroid.extract_node('from foo import bar as enum'), False)
)

('pylint-enums-no-annotated-value', 'pylint-enums-no-assignment-to-value', 'pylint-enums-no-str-method')


classDef_test_cases = (
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

class TestEnumChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = checker.EnumChecker

    @pytest.mark.parametrize("node,expected", import_test_cases)
    def test_import_test_cases(self, node, expected):
        self.checker.visit_import(node)
        assert self.checker.enum_imported is expected
        self.checker.enum_imported = False

    @pytest.mark.parametrize("node,expected", importFrom_test_cases)
    def test_importFrom_test_cases(self, node, expected):
        self.checker.visit_importfrom(node)
        assert self.checker.enum_imported is expected
        self.checker.enum_imported = False

    @pytest.mark.parametrize("node,expected", classDef_test_cases)
    def test_classDef_test_cases_no_import(self, node, expected):
        self.checker.enum_imported = False
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    @pytest.mark.parametrize("node,expected_messages", classDef_test_cases)
    def test_classDef_test_cases_with_import(self, node, expected_messages):
        self.checker.enum_imported = True
        added_messages = [
            pylint.testutils.Message(msg_id=message, node=node)
            for message in expected_messages
        ]
        with self.assertAddsMessages(*added_messages):
            self.checker.visit_classdef(node)
