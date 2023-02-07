from enum import Enum


# то, на что смотрим при выборе участников
# Activity Condition
class AC(Enum):
    DEFAULT = 0
    # один коммент от человека, шансы равны
    ONE_COMMENT = 1
    # больше комментов - выше шанс
    MANY_COMMENTS = 2
    # число - победный номер
    TEXT_DATA = 3
    # НАЛИЧИЕ РЕПОСТА
