from random import randint

from parsers.cond_enums.additional_parameters import AP
from parsers.cond_enums.win_type import WinType
from parsers.rules.win_data import WinData
from parsers.text_process.data_retrieval import DataRetrieval
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class Win:
    WHO_WIN = "------Победитель: "
    NO_WINNERS = "Нет участников - нет победителей"
    WINNER_PLACES = "------Победитель №"
    WINNER_DATA = "Победный комментарий: "
    WINNER_DATAS = "Победные комментарии: "
    WHO_PLAY = "------Участвуют: "
    PLAYER = "Участник: "
    DATA = "--Участвует: "
    NUMBER = "--Номер:"
    CHANCE = "--Шансы на победу: "

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

    def GetWinType(self):
        return self.__win_data[WinData.WIN_TYPE]

    def WhoWin(self, players: list):
        print()
        winners = []
        if len(players) != 0:
            if self.__win_data[WinData.WIN_TYPE] == WinType.NUMERIC_DATA:
                winners = self.GetWinnersNum(players)
            elif self.__win_data[WinData.WIN_TYPE] == WinType.PLAYER:
                winners = self.GetWinnersPlayer(players)
            else:
                winners = self.GetWinnersText(players)
        self.SayWhoWin(winners)

    def WhoPlay(self,
                players_data: list,
                params=None):
        print(Win.WHO_PLAY)
        if params is None:
            if self.__win_data[WinData.WIN_TYPE] != WinType.PLAYER:
                self.__ShowWithoutNames(players_data)
            else:
                self.__ShowWithNames(players_data)
        else:
            self.__ShowWithNames(players_data)

    def __ShowWithNames(self,
                        players_data: list):
        win_type = self.__win_data[WinData.WIN_TYPE]
        if win_type == WinType.PLAYER:
            for player in players_data:
                print(Win.PLAYER + player[TextTags.NAME])
                print(Win.CHANCE + player[TextTags.CHANCE])
        elif win_type == WinType.NUMERIC_DATA:
            for player in players_data:
                print(Win.PLAYER + player[TextTags.NAME])
                print(Win.NUMBER + player[TextTags.DATA])
        else:
            for player in players_data:
                print(Win.PLAYER + player[TextTags.NAME])
                print(Win.DATA + player[TextTags.DATA])
        print()

    def __ShowWithoutNames(self,
                           players_data: list):
        win_type = self.__win_data[WinData.WIN_TYPE]
        if win_type == WinType.NUMERIC_DATA:
            for player in players_data:
                print(Win.NUMBER + player[TextTags.DATA])
        else:
            for player in players_data:
                print(Win.DATA + player[TextTags.DATA])
        print()

    def GetWinnersNum(self,
                      players: list):
        players_data = DataRetrieval.GetPlayersNameAndNumeric(self.__vk_req,
                                                              players,
                                                              self.__link)
        self.WhoPlay(players_data)
        winners = self.HolyRandom(players_data)
        winners_num = []
        for winner in winners:
            winners_num.append(winner[TextTags.DATA])
        self.SayWinnersData(winners_num)
        return winners

    def GetWinnersText(self,
                       players: list):
        players_data = DataRetrieval.GetPlayersNameAndText(self.__vk_req,
                                                           players,
                                                           self.__link,
                                                           self.__win_data[WinData.WIN_TYPE])
        self.WhoPlay(players_data)
        winners = self.HolyRandom(players_data)
        winners_text = []
        for winner in winners:
            winners_text.append(winner[TextTags.DATA])
        self.SayWinnersData(winners_text)
        return winners

    def GetWinnersPlayer(self, players: list):
        players_data = DataRetrieval.GetPlayersNameAndChance(self.__vk_req,
                                                             players)
        self.WhoPlay(players_data)
        return self.HolyRandom(players_data)

    def HolyRandom(self,
                   players_data):
        winners = []
        for i in range(self.__win_data[WinData.WIN_COUNT]):
            winner_index = randint(0, len(players_data) - 1)
            winners.append(players_data[winner_index])
            players_data.pop(winner_index)
        return winners

    def SayWinnersData(self,
                       winners_text: list):
        if self.__win_data[WinData.WIN_COUNT] <= 1:
            print(Win.WINNER_DATA)
        else:
            print(Win.WINNER_DATAS)
        for winner_text in winners_text:
            print(winner_text)

    def SayWhoWin(self,
                  winners: list):
        if len(winners) != 0:
            if self.__win_data[WinData.WIN_COUNT] <= 1:
                print(Win.WHO_WIN + winners[0][TextTags.NAME])
            else:
                for winner_place in range(self.__win_data[WinData.WIN_COUNT]):
                    print(Win.WINNER_PLACES, winner_place + 1, ": ",
                          winners[winner_place][TextTags.NAME])
        else:
            print(Win.WHO_WIN + Win.NO_WINNERS)
