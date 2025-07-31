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
    "datetime": RULE_TYPE_DATETIME
}

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
