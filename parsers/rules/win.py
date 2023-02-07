from random import randint

from parsers.cond_enums.win_type import WinType
from parsers.rules.win_data import WinData
from parsers.text_process.data_retrieval import DataRetrieval
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class Win:
    WHO_WIN = "------Победитель: "
    WINNER_PLACES = "------Победитель №"
    WINNER_NUMBER = "Победный номер: "
    WINNER_NUMBERS = "Победные номера: "

    def __init__(self,
                 win_data=None,
                 link: str = None,
                 vk_req: VKRequests = None):
        if win_data is None:
            win_data = WinData().GetData()
        self.__win_data = win_data
        self.__link = link
        self.__vk_req = vk_req

    def SetVKReq(self, vk_req: VKRequests):
        self.__vk_req = vk_req

    def WhoWin(self, players: list):
        print()
        winners = []
        if self.__win_data[WinData.WIN_TYPE] == WinType.NUMERIC_DATA:
            players_data = DataRetrieval.GetPlayersNameAndNumeric(self.__vk_req,
                                                                  players,
                                                                  self.__link)
            winners_num = []
            nums = []
            for player in players_data:
                nums.append(int(player[TextTags.NUMERIC]))
            for i in range(self.__win_data[WinData.WIN_COUNT]):
                winner_index = randint(0, len(nums) - 1)
                winners.append(players[winner_index])
                winners_num.append(players_data[winner_index][TextTags.NUMERIC])
                nums.pop(winner_index)
            self.SayWinnersNum(winners_num)
        else:
            for i in range(self.__win_data[WinData.WIN_COUNT]):
                winner_index = randint(0, len(players) - 1)
                winners.append(players[winner_index])
                players.pop(winner_index)

        self.SayWhoWin(winners)

    def SayWinnersNum(self,
                      winners_num: list):
        if self.__win_data[WinData.WIN_COUNT] <= 1:
            print(Win.WINNER_NUMBER)
        else:
            print(Win.WINNER_NUMBERS)
        for winner_num in winners_num:
            print(winner_num)

    def SayWhoWin(self,
                  winners: list):
        winners_name = DataRetrieval.GetPlayersName(self.__vk_req,
                                                    winners)
        if self.__win_data[WinData.WIN_COUNT] <= 1:
            print(Win.WHO_WIN + winners_name[0])
        else:
            for winner_place in range(self.__win_data[WinData.WIN_COUNT]):
                print(Win.WINNER_PLACES, winner_place + 1, ": ",
                      winners_name[winner_place])
