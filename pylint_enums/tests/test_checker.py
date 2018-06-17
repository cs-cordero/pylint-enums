import pylint.testutils
import pytest

from pylint_enums import checker
from pylint_enums.tests.constants import IMPORT_TEST_CASES
from pylint_enums.tests.constants import IMPORTFROM_TEST_CASES
from pylint_enums.tests.constants import CLASSDEF_TEST_CASES
from pylint_enums.tests.constants import ANNOTATION_NAME_TEST_CASES


class TestEnumChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = checker.EnumChecker

    @pytest.mark.parametrize("node,expected", IMPORT_TEST_CASES)
    def test_import_cases(self, node, expected):
        self.checker.visit_import(node)
        assert self.checker.enum_imported is expected
        self.checker.enum_imported = False

    @pytest.mark.parametrize("node,expected", IMPORTFROM_TEST_CASES)
    def test_importfrom_cases(self, node, expected):
        self.checker.visit_importfrom(node)
        assert self.checker.enum_imported is expected
        self.checker.enum_imported = False

    @pytest.mark.parametrize("node,expected", CLASSDEF_TEST_CASES)
    def test_classdef_cases_no_import(self, node, expected):
        self.checker.enum_imported = False
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    @pytest.mark.parametrize("node,expected_messages", CLASSDEF_TEST_CASES)
    def test_classdef_cases_with_import(self, node, expected_messages):
        self.checker.enum_imported = True
        added_messages = [
            pylint.testutils.Message(msg_id=message, node=node)
            for message in expected_messages
        ]
        with self.assertAddsMessages(*added_messages):
            self.checker.visit_classdef(node)

    @pytest.mark.parametrize("node,expected", ANNOTATION_NAME_TEST_CASES)
    def test_get_annotation_name(self, node, expected):
        assert checker.get_annotation_name(node) == expected
