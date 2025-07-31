"""
Test Case:

Header config rule:
header_check = [
    {"name": "rtm", "type": "varchar", "required": False},
    {"name": "business_type", "type": "varchar", "required": True},
    {"name": "sub_lob", "type": "varchar", "required": False},
    {"name": "fph_level", "type": "int", "required": False},
    {"name": "remarks", "type": "varchar", "required": False},
    {"name": "instock", "type": "float", "required": False},
]

Add other config rule by row:
check_rule = [
    {"field": ["rtm"], "role": "in ['Mono', 'Carrier', 'Multi', 'Online']", "category": "row"},
    {"field": ["instock"], "role": "instock > 50 and instock <= 70", "category": "row"}
]

Check Data by row:
check_data = [
    {"rtm": "Mono", "business_type": "22", "sub_lob": "ddd", "fph_level": 1, "remarks": "11", "instock": 55},
    {"rtm": "Mono", "business_type": "bb", "sub_lob": "ddd", "fph_level": 1, "remarks": "11", "instock": 56},
    {"rtm": "Carrier", "business_type": "bb", "sub_lob": "ddd", "fph_level": 1, "remarks": "11","instock": 58},
]

Use the func:
check_result = ROWChecker(header_rule=header_check, check_rule=check_rule, check_data=check_data)._check_result() -> True
"""

from rule_engine import Rule, Context, type_resolver_from_dict
from utils.rule_checker import get_rule_col_type, get_rule_text_by_require, ROW_CHECK_CATEGORY


class ROWChecker(object):
    def __init__(self, header_rule: list, check_rule: list, check_data: dict):
        self.header_rule = header_rule
        self.check_data = check_data
        self.check_rule = check_rule

    # 获取header类型及非空必空的参数
    def get_context_by_required_and_type_rule(self):
        _type_resolver, rule_text = {}, ''
        for info in self.header_rule:
            field = info["name"]
            _type = info["type"]
            required = info["required"]

            _type_resolver[field] = get_rule_col_type(_type)

            add_rule_text = get_rule_text_by_require(field, required)
            if add_rule_text:
                if rule_text:
                    rule_text += f" and {add_rule_text}"
                else:
                    rule_text = add_rule_text

        # 构建校验context
        context = Context(type_resolver=type_resolver_from_dict(_type_resolver))
        return context, rule_text

    # 获取扩展类role规则的字段
    def get_rule_by_check_rule(self):
        rule_text = ""
        for info in self.check_rule:
            fields = info["field"]
            role = info["role"]
            category = info["category"]

            # 如果类型不是行标识,跳过不处理
            if category != ROW_CHECK_CATEGORY:
                continue

            # 如果role规则没有进行配置则也跳过不处理
            if not role:
                continue

            for field in fields:
                _sub_rule_text = f"{field} {role}" if field not in role else f"{role}"
                if rule_text:
                    rule_text += f" and {_sub_rule_text}"
                else:
                    rule_text = _sub_rule_text
        return rule_text

    @classmethod
    def return_rule_and_context(cls, header_rule: str, check_rule: str, context: Context):
        rule_text = ""
        if header_rule:
            rule_text += header_rule
        if check_rule:
            if rule_text:
                rule_text += f" and {check_rule}"
            else:
                rule_text += check_rule
        if rule_text:
            rule = Rule(rule_text, context=context)
            return rule

        if not header_rule and not check_rule:
            rule_text = "1 == 1"
            rule = Rule(rule_text, context=context)
            return rule

    def _check_result(self):
        context_obj, header_rule = self.get_context_by_required_and_type_rule()
        check_rule = self.get_rule_by_check_rule()

        engine_rule = self.return_rule_and_context(header_rule, check_rule, context_obj)
        result = []
        for data in self.check_data:
            _result = engine_rule.matches(data)
            result.append(_result)
        return all(result)
