from enum import Enum


# то, на что смотрим при выборе участников
# Activity Condition
class AC(Enum):
    DEFAULT = 0
    # один коммент от человека, шансы равны
    ONE_COMMENT = 1
    # больше комментов - выше шанс
    MANY_COMMENT = 2
    # число - победный номер
    NUMBER_DATA = 3
    # определённое сообщение = участие в розыгрыше
    TEXT_DATA = 4
    # НАЛИЧИЕ РЕПОСТА
