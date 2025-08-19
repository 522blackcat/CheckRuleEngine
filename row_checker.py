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
check_result = ROWChecker(header_rule=header_check, check_rule=check_rule, check_data=check_data)._check_result() -> result
result:
{'_res': False, '_error': "business_type in ['Mono', 'Carrier', 'Multi', 'Online'] check result is Error.", '_col': 'business_type', '_col_index': 1, '_type': 'Invalid Value'}
"""
import datetime

import rule_engine.errors
from rule_engine import Rule, Context, type_resolver_from_dict
from utils.rule_checker import (
    get_rule_col_type,
    get_rule_text_by_require,
    ROW_CHECK_CATEGORY,
    SPECIAL_DB_TYPE,
    get_rule_text_by_type
)
from utils.rule_checker.const import CheckerType


class ROWChecker(object):
    def __init__(self, header_rule: list, check_rule: list, check_data: list):
        self.header_rule = header_rule
        self.check_data = check_data
        self.check_rule = check_rule

    # 获取header类型
    def get_context_by_type(self):
        _type_resolver = {}
        for info in self.header_rule:
            field = info["name"]
            _type = info["type"]
            _type_resolver[field] = get_rule_col_type(_type)
        return _type_resolver

    # 获取header类型及非空必空的参数
    def get_context_by_required_and_type_rule(self):
        _type_resolver = {}
        for info in self.header_rule:
            field = info["name"]
            _type = info["type"]
            required = info["required"]

            _type_resolver[field] = {"data_type": {field: get_rule_col_type(_type)}, "supple_data_type": "", "required": "", "_type": _type}
            if _type in SPECIAL_DB_TYPE:
                _type_resolver[field]["supple_data_type"] = get_rule_text_by_type(field, _type)
            _type_resolver[field]["required"] = get_rule_text_by_require(field, required)
        return _type_resolver

    def _check_header(self, allowed_null=False):
        type_resolver = self.get_context_by_required_and_type_rule()
        for field, rule_dict in type_resolver.items():
            data_type = rule_dict["data_type"]
            supple_data = rule_dict["supple_data_type"]
            required = rule_dict["required"]
            _type = rule_dict["_type"]

            if not data_type:
                return False, field, "Data Type is Error.", CheckerType.DATA_TYPE.value, _type
            # 声明数据类型
            context = Context(type_resolver=type_resolver_from_dict(data_type))
            # 补充数据类型说明
            if supple_data:
                engine_rule = Rule(supple_data, context=context)
                for data in self.check_data:
                    # 列数据在校验数据类型的时候，允许传none 和 空数据的通过, 等待required参数的校验
                    if allowed_null and (data[field] is None or data[field] == ''):
                        continue
                    try:
                        _result = engine_rule.matches(data)
                        if not _result:
                            return False, field, "Data Type is Error.", CheckerType.DATA_TYPE.value, _type
                    except rule_engine.errors.SymbolTypeError:
                        return False, field, "Data Type is Error.", CheckerType.DATA_TYPE.value, _type
                    except Exception as e:
                        return False, field, f"Data Type is Error: {str(e)}.", CheckerType.DATA_TYPE.value, _type
            # 校验非空字段
            if required:
                rule_text = f"{supple_data} and {required}" if supple_data else f"{required}"
                engine_rule = Rule(rule_text, context=context)
                for data in self.check_data:
                    try:
                        _result = engine_rule.matches(data)
                        if not _result:
                            return False, field, "Data required is Error.", CheckerType.REQUIRED.value, ''
                    except rule_engine.errors.SymbolTypeError:
                        return False, field, "Data Type is Error.", CheckerType.DATA_TYPE.value, _type
                    except Exception as e:
                        return False, field, f"Data required is Error: {str(e)}.", CheckerType.REQUIRED.value, ''
            if not supple_data and not required:
                rule_text = "1==1"
                engine_rule = Rule(rule_text, context=context)
                for data in self.check_data:
                    # # 列数据在校验数据类型的时候，允许传none 和 空数据的通过, 等待required参数的校验
                    # if allowed_null and _type in SPECIAL_DATE_TYPE and (data[field] is None or data[field] == ''):
                    #     continue
                    try:
                        _result = engine_rule.matches(data)
                        if not _result:
                            return False, field, "Data Type is Error.", CheckerType.DATA_TYPE.value, _type
                    except Exception as e:
                        return False, field, f"Data Type is Error: {str(e)}.", CheckerType.DATA_TYPE.value, _type
        return True, "", "", "", ""

    def _check_check_rule(self):
        type_resolver = self.get_context_by_type()
        context = Context(type_resolver=type_resolver_from_dict(type_resolver))
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

            rule_dict = {}
            for field in fields:
                if rule_dict.get(field) is None:
                    rule_dict[field] = []
                rule_dict[field].append(f"{field} {role}" if field not in role else f"{role}")

            for index, data in enumerate(self.check_data):
                for field, rule_list in rule_dict.items():
                    for rule in rule_list:
                        engine_rule = Rule(rule, context=context)
                        try:
                            _result = engine_rule.matches(data)
                            if not _result:
                                return False, field, index, f"{rule} check result is Error.", rule.split(field)[1].strip()
                        except Exception as e:
                            return False, field, index, f"{rule} check result is Error: {str(e)}.", rule.split(field)[1].strip()
        return True, "", 0, "", ""

    def check_result(self, allowed_null=False):
        header_flag, header_field, header_error, type, extra_info = self._check_header(allowed_null=allowed_null)
        if not header_flag:
            return {
                "_res": header_flag,
                "_error": header_error,
                "_col": header_field,
                '_col_index': 0,  # header 头
                "_type": type,
                "_extra_info": extra_info,
            }
        # check header 方法通过后才可以执行下面逻辑
        check_flag, check_field, check_index, check_error, extra_info = self._check_check_rule()
        if not check_flag:
            return {
                '_res': check_flag,
                '_error': check_error,
                '_col': check_field,
                '_col_index': check_index + 1,  # 行号
                "_type": CheckerType.CONTENT_INVALID.value,
                "_extra_info": extra_info,
            }

        return {
            '_res': True,
            '_error': "",
            '_col': "",
            '_col_index': -1,
            "_type": '',
            "_extra_info": '',
        }
