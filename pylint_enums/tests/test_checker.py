import pylint.testutils
import pytest

import checker
from tests.constants import *


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
