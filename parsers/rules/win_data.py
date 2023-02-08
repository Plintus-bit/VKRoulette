from parsers.cond_enums.win_type import WinType
from parsers.rules.data import Data


class WinData(Data):
    WIN_TYPE = "win_type"
    WIN_COUNT = "count"

    def __init__(self,
                 win_type: WinType = WinType.PLAYER,
                 win_count: int = 1):
        self.win_count = win_count
        self.win_type = win_type

    def GetData(self) -> dict:
        win_data = dict()
        win_data[WinData.WIN_TYPE] = self.win_type
        win_data[WinData.WIN_COUNT] = self.win_count
        return win_data
