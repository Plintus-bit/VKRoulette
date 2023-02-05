import re
from random import randint

from parsers.cond_enums.activity_cond import AC
from parsers.cond_enums.rule_types import RuleType
from parsers.rules.rule import Rule
from parsers.rules.rule_data import RuleData
from parsers.text_process.text_separation import TextSeparator
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class VKRoulette:
    WHO_PLAY = "Участвуют: "
    WHO_WIN = "Победитель: "
    WINNER_PLACES = "Победитель №"
    VK_REQ = VKRequests()

    @staticmethod
    def WhoWin(players: list[str], win_places: int = 1):
        print()
        winners = []
        for i in range(win_places):
            winner_index = randint(0, len(players) - 1)
            winners.append(players[winner_index])
            players.pop(winner_index)
        winners_name = VKRoulette.GetPlayersName(winners)
        if win_places <= 1:
            print(VKRoulette.WHO_WIN + winners_name[0])
        else:
            winners_count = min([win_places, len(players)])
            for winner_place in range(winners_count):
                print(VKRoulette.WINNER_PLACES, winner_place + 1, ": ", winners_name[winner_place])

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
    def WhoPlay(players: list[str]):
        print(VKRoulette.WHO_PLAY)
        players_name = VKRoulette.GetPlayersName(players)
        for player_name in players_name:
            print(player_name)

    @staticmethod
    def GetPlayersName(players_id: list):
        names_separator = " "
        players_name = []
        players_data = VKRoulette.VK_REQ.GetUsers(players_id)
        for player_data in players_data:
            players_name.append(player_data[TextTags.FIRST_NAME]
                                + names_separator
                                + player_data[TextTags.LAST_NAME])
        return players_name
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
                if player_exc in players:
                    players.remove(player_exc)
        VKRoulette.WhoPlay(players)
        VKRoulette.WhoWin(players)


VKRoulette.Roulette(
    rules=[
        Rule(
            rule_data=RuleData(
                RuleType.COMMENT,
                AC.ONE_COMMENT,
            ).GetRuleData(),
            links=[
                "https://vk.com/wall-204044583_1024"
            ]),
    ],
    exceptions=[
        "https://vk.com/plintus_ick",
        "https://vk.com/akira_l",
        "https://vk.com/wrong_gayborhood",
        "https://vk.com/camshel"
    ])
