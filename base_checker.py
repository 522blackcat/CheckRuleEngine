"""
    Base checker, not allowed by now


"""



from typing import Any
from datetime import datetime

import rule_engine
from rule_engine import Rule, Context


class BaseChecker:

    @classmethod
    def except_error(cls, exception: object):
        return exception.__str__()


class IntCellChecker(BaseChecker):
    """
    int 类型
    {"a": "1"}
    """
    def _get_rule(self, name: str) -> Rule:
        context = Context(type_resolver=rule_engine.type_resolver_from_dict({
            name: rule_engine.DataType.FLOAT
        }))
        return Rule('', context=context)

    def _check_cell(self, name: str, value: int) -> bool:
        rule = self._get_rule(name)
        return rule.matches({name: value})


class StrCellChecker(BaseChecker):
    """
    string 类型
    """
    def _get_rule(self, name: str) -> Rule:
        context = Context(type_resolver=rule_engine.type_resolver_from_dict({
            name: rule_engine.DataType.STRING
        }))
        return Rule('', context=context)

    def _check_cell(self, name: str, value: str) -> bool:
        rule = self._get_rule(name)
        return rule.matches({name: value})


class FloatCellChecker(BaseChecker):
    """
    float 类型 和 int 类型是用的一种判断
    """
    def _get_rule(self, name: str) -> Rule:
        context = Context(type_resolver=rule_engine.type_resolver_from_dict({
            name: rule_engine.DataType.FLOAT
        }))
        return Rule('', context=context)

    def _check_cell(self, name: str, value: float) -> bool:
        rule = self._get_rule(name)
        return rule.matches({name: value})


class ChoiceCellChecker(BaseChecker):
    """
    choice 类型
    """
    def _get_rule(self, name: str, choices: tuple) -> Rule:
        return Rule(f'{name} in "{choices}"')

    def _check_cell(self, name: str, value: Any[str, int, float, None], choices: tuple) -> bool:
        rule = self._get_rule(name, choices)
        return rule.matches({name: value})


class DatetimeCellChecker(BaseChecker):
    """
    datetime 类型
    """
    def _get_rule(self, name: str) -> Rule:
        context = Context(type_resolver=rule_engine.type_resolver_from_dict({
            name: rule_engine.DataType.DATETIME
        }))
        return Rule('', context=context)

    def _check_cell(self, name: str, value: datetime) -> bool:
        rule = self._get_rule(name)
        return rule.matches({name: value})


class BoolCellChecker(BaseChecker):
    """
    bool 类型
    """
    def _get_rule(self, name: str) -> Rule:
        context = Context(type_resolver=rule_engine.type_resolver_from_dict({
            name: rule_engine.DataType.BOOLEAN
        }))
        return Rule('', context=context)

    def _check_cell(self, name: str, value: bool) -> bool:
        rule = self._get_rule(name)
        return rule.matches({name: value})


class NotAllowedCellChecker(BaseChecker):
    """
    A class to check the str of a cell.
    """
    def _get_rule(self, name: str, not_allowed: tuple) -> Rule:
        return Rule(f'{name} in {not_allowed}')

    def _check_cell(self, name: str, value: Any[str, int, float], not_allowed: tuple) -> bool:
        rule = self._get_rule(name, not_allowed)
        return not rule.matches({name: value})


class RangeCellChecker(BaseChecker):
    """
    range 类型
    """
    def _get_rule(self, name: str, left: Any[int, float], right: Any[int, float]) -> Rule:
        return Rule(f'{name} > {left} and {name} < {right}')

    def _check_cell(self, name: str, value: Any[int, float], left: Any[int, float], right: Any[int, float]) -> bool:
        rule = self._get_rule(name, left, right)
        return not rule.matches({name: value})
