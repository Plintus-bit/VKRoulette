import re
from random import randint

from parsers.cond_enums.activity_cond import AC
from parsers.cond_enums.consider_cond import CC
from parsers.cond_enums.rule_types import RuleType
from parsers.rules.rule import Rule
from parsers.rules.rule_data import RuleData
from parsers.text_process.text_separation import TextSeparator
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class VKRoulette:
    WHO_PLAY = "------Участвуют: "
    WHO_WIN = "------Победитель: "
    PLAYER = "Участник: "
    CHANCE = "--Шансы на победу: "
    WINNER_PLACES = "------Победитель №"
    VK_REQ = VKRequests()

    @staticmethod
    def WhoWin(players: dict, win_places: int = 1):
        print()
        winners = []
        for i in range(win_places):
            winner_index = randint(0, len(players) - 1)
            winners.append(players[winner_index])
            players.pop(winner_index)
        winners_name = VKRoulette.GetPlayersName(winners)
        if win_places <= 1:
            print(VKRoulette.WHO_WIN + winners_name[0][TextTags.NAME])
        else:
            winners_count = min([win_places, len(players)])
            for winner_place in range(winners_count):
                print(VKRoulette.WINNER_PLACES, winner_place + 1, ": ",
                      winners_name[winner_place][TextTags.NAME])

    @staticmethod
    def GetExceptionsPlayers(exception_players: list[str]):
        exc_short_names = []
        for exc_pl in exception_players:
            exc_short_names.append(TextSeparator.GetShortNameOrId(exc_pl))
        exc_names_data = VKRoulette.VK_REQ.GetUsers(exc_short_names)
        result_exc = []
        for data in exc_names_data:
            result_exc.append(data[TextTags.ID])
        return result_exc

    @staticmethod
    def WhoPlay(players: dict):
        print(VKRoulette.WHO_PLAY)
        players_name = VKRoulette.GetPlayersName(players)
        for player_name in players_name:
            print(VKRoulette.PLAYER + player_name[TextTags.NAME])
            print(VKRoulette.CHANCE + player_name[TextTags.CHANCE])
            print()

    @staticmethod
    def GetPlayersName(players_id: list) -> list:
        names_separator = " "
        players = []
        players_data = VKRoulette.VK_REQ.GetUsers(players_id)
        for player_data in players_data:
            player = dict()
            player[TextTags.NAME] = player_data[TextTags.FIRST_NAME]\
                                    + names_separator\
                                    + player_data[TextTags.LAST_NAME]
            chance = players_id.count(player_data[TextTags.ID])
            player[TextTags.CHANCE] = str(chance)
            players.append(player)
        return players
    # ----------------- САМ РОЗЫГРЫШ ПО УСЛОВИЯМ --------------------

    @staticmethod
    def Roulette(rules: list[Rule],
                 exceptions=None):
        players = []

        for rule in rules:
            rule.SetVKReq(VKRoulette.VK_REQ)
            players = rule.GetPlayers(players)
        if exceptions is not None:
            players_exceptions = VKRoulette.GetExceptionsPlayers(exceptions)
            for player_exc in players_exceptions:
                while player_exc in players:
                    players.remove(player_exc)
        VKRoulette.WhoPlay(players)
        VKRoulette.WhoWin(players)
        # print(VKRoulette.VK_REQ.GetComments(-204044583, 1111))
        # print(VKRoulette.VK_REQ.GetComments(-204044583, 1111, 1115))


VKRoulette.Roulette(
    rules=[
        Rule(
            rule_data=RuleData(
                rule_type=RuleType.COMMENT,
                activity_type=AC.MANY_COMMENTS,
                consider_type=CC.ALL_COMMENTS
            ).GetRuleData(),
            links=[
                "https://vk.com/wall-204044583_1054"
            ]),
    ],
    exceptions=[
        "https://vk.com/plintus_ick",
        "https://vk.com/akira_l",
        "https://vk.com/wrong_gayborhood",
        "https://vk.com/camshel"
    ])
