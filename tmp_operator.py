import datetime

import rule_engine
from numbers import Number
from rule_engine import Rule, Context, type_resolver_from_dict

context = Context(type_resolver=rule_engine.type_resolver_from_dict({
    "a": rule_engine.DataType.STRING,
    'b': rule_engine.DataType.FLOAT,
    'c': rule_engine.DataType.FLOAT
}))

rule = Rule(
    'a in ["1", "2", "3", "4"] and  b > 1 and b < 3',
    context=context
)

result = rule.matches({'a': "1", 'b': 1, "c": 20})
print(result)


# 定义求和函数
def custom_sum(items):
    return sum(item['b'] for item in items)


# 注册函数到上下文
context = type_resolver_from_dict({
    'sum_values': (custom_sum, ('iterable',), None)
})
rule1 = Rule('sum(b)')
result1 = rule1.matches([{'a': 1, 'b': 100}, {'a': 2, 'b': 100}])
print(result1)

