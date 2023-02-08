from enum import Enum


# то, на что смотрим при выборе участников
# Activity Condition
class AC(Enum):
    DEFAULT = 0
    # один коммент от человека, шансы равны
    ONE_COMMENT = 1
    # больше комментов - выше шанс
    MANY_COMMENTS = 2
    # особый текст = участие
    TEXT_DATA = 3
    # наличие эмодзи = участие
    EMOJI = 4
