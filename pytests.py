import astroid
import pylint.testutils
import pytest

import checker

class TestEnumChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = checker.EnumChecker

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
