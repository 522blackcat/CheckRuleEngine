import decimal

import rule_engine
from rule_engine import Rule


def custom_sum(items):
    return sum(item['b'] for item in items)


rule1 = Rule('custom_sum(b) > 100')
result1 = rule1.matches({'custom_sum': custom_sum, 'b': [{'a': 1, 'b': 100}, {'a': 2, 'b': 100}]})
print(result1)


from rule_engine import Rule


def judge_type(items):
    if not items:  # 处理空列表
        return False
    try:
        return all((isinstance(x.get('b'), decimal.Decimal) for x in items))
    except (AttributeError, TypeError):
        return False


rule2 = Rule(f'judge_type(data)')
result2 = rule2.matches({'judge_type': judge_type, 'data': [{'a': '1', 'b': 100}, {'a': '3', 'b': 100}]})
print(result2)


data = [{'a': 1, 'b': 100}, {'a': 2, 'b': 100}]
print(judge_type(data))
