"""
Test Case:

Columns checker after the row checker, so need checker the check_rule by special functions.

Add other config rule by col:
check_rule = [
    {"field": ["rtm", "business_type", "sub_lob"], "role": "unique", "category": "col"},
    {"field": ["fph_level", "remarks", "instock"], "role": "unique", "category": "col"}
]

Check Data by col:
check_data = [
    {"rtm": "Mono", "business_type": "cc", "sub_lob": "a", "fph_level": 1, "remarks": "11", "instock": 55},
    {"rtm": "Mono", "business_type": "bb", "sub_lob": "sd", "fph_level": 1, "remarks": "11", "instock": 55},
    {"rtm": "Mono", "business_type": "bb", "sub_lob": "d", "fph_level": 1, "remarks": "11", "instock": 55},
]

Use the func:
res, check_errors = COLChecker(check_rule, check_data)._check_result()
print(res)
print(check_errors)

Result:
[
    {
        '_res': False,
        '_error': [{
            'first_index': 0, 'current_index': 1, 'combination': ('Mono', 'bb', 'ddd')
        }, {
            'first_index': 0, 'current_index': 2, 'combination': ('Mono', 'bb', 'ddd')
        }]
    },
    {
        '_res': False,
        '_error': [{
            'first_index': 0, 'current_index': 1, 'combination': ('Mono', 'ddd', 1)
        }, {
            'first_index': 0, 'current_index': 2, 'combination': ('Mono', 'ddd', 1)
        }]
    }
]
"""
from utils.rule_checker import COL_CHECK_CATEGORY


class COLChecker(object):
    def __init__(self, check_rule: list, check_data: dict):
        self.check_data = check_data
        self.check_rule = check_rule

    @classmethod
    def _unique(cls, cols: list, check_data: list):
        """
        检查字典列表中指定字段组合是否唯一
        :return: (bool, list) 是否唯一，重复项列表
        """
        seen = {}
        duplicates = []

        for idx, item in enumerate(check_data):
            # 生成组合键
            combination = tuple(item[col] for col in cols)

            if combination in seen:
                duplicates.append({
                    'first_index': seen[combination],
                    'current_index': idx,
                    'combination': combination
                })
            else:
                seen[combination] = idx
        return {
            "_res": len(duplicates) == 0,
            "_error": duplicates
        }

    @classmethod
    def _get_check_rule(cls, col_rule: dict):
        role = col_rule['role']

        if hasattr(cls, f"_{role}") and callable(getattr(cls, f"_{role}")):
            return getattr(cls, f"_{role}")
        raise AttributeError(f"Method {cls.__name__} has no attribute _{role}")

    def _check_result(self):
        check_res = []
        for col_rule in self.check_rule:
            fields = col_rule['field']
            category = col_rule['category']
            if category != COL_CHECK_CATEGORY:
                continue
            _check_res = self._get_check_rule(col_rule)(fields, self.check_data)
            check_res.append(_check_res)

        _checks = all([i["_res"] is True for i in check_res])
        if _checks:
            return True, []
        else:
            return False, check_res







