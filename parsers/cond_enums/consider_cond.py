from enum import Enum


# то, что нужно учитывать
# Consider Condition
class CC(Enum):
    DEFAULT = 0
    # учитывать только основные комменты
    BASIC_COMMENT_ONLY = 1
    # учитывать и основные комменты, и ответы на комменты
    ALL_COMMENTS = 2
