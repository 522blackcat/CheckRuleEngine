from enum import Enum

import rule_engine


RULE_TYPE_VARCHAR = rule_engine.DataType.STRING
RULE_TYPE_INT = rule_engine.DataType.FLOAT
RULE_TYPE_FLOAT = rule_engine.DataType.FLOAT
RULE_TYPE_BOOLEAN = rule_engine.DataType.BOOLEAN
RULE_TYPE_DATE = rule_engine.DataType.DATETIME
RULE_TYPE_DATETIME = rule_engine.DataType.DATETIME


DB_TYPE_TRANSFORM_RULE = {
    "varchar": RULE_TYPE_VARCHAR,
    "int": RULE_TYPE_INT,
    "float": RULE_TYPE_FLOAT,
    "boolean": RULE_TYPE_BOOLEAN,
    "date": RULE_TYPE_DATE,
    "datetime": RULE_TYPE_DATETIME,
    "text": RULE_TYPE_VARCHAR,
}

DB_TYPE_TRANSFORM_DISPLAY = {
    "varchar": "String",
    "text": "String",
    "datetime": "Time",
    "date": "Date",
    "int": "Int",
    "float": "Float",
}

SPECIAL_DB_TYPE = ('int', 'float', 'date', 'datetime', 'varchar', 'text')


ROW_CHECK_CATEGORY = "row"
COL_CHECK_CATEGORY = "col"


TRUE_REQUIRE = True
FALSE_REQUIRE = False


def get_rule_col_type(db_type: str) -> rule_engine.DataType:
    if db_type in DB_TYPE_TRANSFORM_RULE:
        return DB_TYPE_TRANSFORM_RULE[db_type]
    raise ValueError("Unknown database type")


def get_rule_text_by_require(field: str, required: str) -> str:
    if required == TRUE_REQUIRE:
        return f"{field} != null and {field} != ''"
    if required == FALSE_REQUIRE:
        return ""
    return ''


def get_rule_text_by_type(field: str, _type: str) -> str:
    if _type in ['varchar', 'text']:
        return f"{field}=~'.*'"
    if _type == "int":
        return f"{field}//1=={field}"
    if _type == "float":
        return f"({field}>=0 or {field}<0)"
    if _type == "date":
        return f"{field}>=d'1970-01-01 00:00:00'"
    if _type == "datetime":
        return f"{field}>=d'1970-01-01 00:00:00'"
    return ""


# 检验规则的类型
class CheckerType(Enum):
    CONTENT_INVALID = "Invalid Value"
    DATA_TYPE = "Data Type"
    REQUIRED = "Required"
    DUPLICATE = "Duplicate Data"
    UNKNOWN = "Unknown Error"


class FileCheckMessageError:
    MESSAGE = {
        CheckerType.CONTENT_INVALID.value: "Invalid content value:",
        CheckerType.DATA_TYPE.value: "Field type mismatch:",
        CheckerType.REQUIRED.value: "Missing required fields:",
        CheckerType.DUPLICATE.value: "Duplicate data found:",
        CheckerType.UNKNOWN.value: "Unknown Error:",
    }

    @classmethod
    def get_message_by_check_type(cls, check_type):
        return cls.MESSAGE.get(check_type, CheckerType.UNKNOWN.value)
