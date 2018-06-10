import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

def is_subclass_of_enum(node):
    """ Returns whether a base class on the node has the name 'Enum' """
    for base_class in node.bases:
        if isinstance(base_class, astroid.node_classes.Attribute):
            base_class_name = base_class.attrname
        elif isinstance(base_class, astroid.node_classes.Name):
            base_class_name = base_class.name
        else:
            continue

        if base_class_name == 'Enum':
            return True
    return False


class EnumChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'enum-implementation'
    priority = -1
    msgs = {
        'W5501': (
            'Enums must have their value attribute annotated',
            'pylint-enums-no-annotated-value',
            'All enums should have their value attribute annotated.'
        ),
        'W5502': (
            'Enums must not assign a value to their \'value\' attribute',
            'pylint-enums-no-assignment-to-value',
            'All enums should not assign a value to their value attribute.'
        ),
        'W5503': (
            'Enums must implement their __str__ method',
            'pylint-enums-no-str-method',
            'All enums implement a __str__ method.'
        ),
    }

    def __init__(self, linter=None):
        super().__init__(linter)
        self.enum_imported = False

    def visit_module(self, node):
        self.enum_imported = False

    def visit_import(self, node):
        """
        Checks whether an enum module has been imported
            i.e.,  import enum
        """
        if self.enum_imported:
            return

        for module_name, _ in node.names:
            if module_name == 'enum':
                self.enum_imported = True
                return

    def visit_importfrom(self, node):
        """
        Checks whether an Enum class has been imported with the "from" convention
        from an enum module.
            i.e.,  from enum import Enum
        """
        if self.enum_imported or not node.modname == 'enum':
            return

        for module_name, _ in node.names:
            if module_name in ('Enum', '*'):
                self.enum_imported = True
                return

    def visit_classdef(self, node):
        """
        Checks whether an Enum subclass has a value annotation and a __str__ method
        """
        if not self.enum_imported or not is_subclass_of_enum(node):
            return

        value_annotated = False
        for child_node in node.get_children():
            if not isinstance(child_node, astroid.node_classes.AnnAssign):
                continue

            if child_node.target.name == 'value':
                value_annotated = True
                if child_node.value is not None:
                    self.add_message('pylint-enums-no-assignment-to-value', node=node)
                    break

        if not value_annotated:
            self.add_message('pylint-enums-no-annotated-value', node=node)

        if not any(method.name == '__str__' for method in node.mymethods()):
            self.add_message('pylint-enums-no-str-method', node=node)

def register(linter):
    linter.register_checker(EnumChecker(linter))
