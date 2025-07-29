


class BaseChecker:

    @classmethod
    def except_error(cls, exception: object):
        return exception.__str__()


class ColumnsBaseChecker(BaseChecker):
    """
    column base类
    """
    pass


class RowsBaseChecker(BaseChecker):
    """
    row base类
    """
    pass
