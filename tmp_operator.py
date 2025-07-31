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
    'a in ["1", "2", "3", "4"] and  b >= 1 and c < 10',
    context=context
)

result = rule.matches({'a': "1", 'b': 1, "c": 20})
print(result)


context = Context(type_resolver=rule_engine.type_resolver_from_dict({
    "rtm": rule_engine.DataType.STRING,
    "business_type": rule_engine.DataType.STRING,
    "lob": rule_engine.DataType.STRING,
    "sub_lob": rule_engine.DataType.STRING,
    "fph_level": rule_engine.DataType.FLOAT,
    "remarks": rule_engine.DataType.STRING,
    "instock_target": rule_engine.DataType.FLOAT
}))
a = "business_type != null and business_type != '' and rtm in ['Mono','Carrier','Multi','Online'] and sub_lob in ['Mono','Carrier','Multi','Online'] and instock_target > 50 and instock_target <= 70"

rule = Rule(a, context=context)
