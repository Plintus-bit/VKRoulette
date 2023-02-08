from threading import Thread

from parsers.cond_enums.activity_cond import AC
from parsers.cond_enums.consider_cond import CC
from parsers.cond_enums.rule_type import RuleType
from parsers.cond_enums.win_type import WinType
from parsers.rules.rule import Rule
from parsers.rules.rule_data import RuleData
from parsers.rules.win import Win
from parsers.rules.win_data import WinData
from parsers.text_process.data_retrieval import DataRetrieval
from parsers.text_process.text_separation import TextSeparator
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class VKRoulette:
    VK_REQ = VKRequests()

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
    def GetContactExceptions(links: list[str]):
        group_ids = []
        for link in links:
            group_ids.append(TextSeparator.GetGroupNameOrId(link))
        return VKRoulette.VK_REQ.GetGroupContacts(group_ids)
    # ----------------- САМ РОЗЫГРЫШ ПО УСЛОВИЯМ --------------------

    @staticmethod
    def ExcludeExceptions(players: list,
                          group_links: list[str] = None,
                          exceptions=None):
        if exceptions is None:
            exceptions = []
         # сбор исключений
        if exceptions:
            exceptions = VKRoulette.GetExceptionsPlayers(exceptions)
        if group_links is not None:
            contacts_exc = VKRoulette.GetContactExceptions(group_links)
            for contact_exc in contacts_exc:
                for contact in contact_exc[TextTags.CONTACTS]:
                    exceptions.append(contact[TextTags.USER_ID])
        # удаление исключений
        for player_exc in exceptions:
            while player_exc in players:
                players.remove(player_exc)
        return players

    @staticmethod
    def ClearingGroupsFromParticipation(players: list):
        # если номер < 0, значит,
        # коммент оставлен не от юзера (от группы)
        for player_id in players:
            if player_id < 0:
                players.remove(player_id)
        return players

    @staticmethod
    def GetParticipants(rules: list[Rule]):
        players = []
        for rule in rules:
            rule.SetVKReq(VKRoulette.VK_REQ)
            players = rule.GetPlayers(players)
            if len(players) == 0:
                return players
        return players

    @staticmethod
    def TryLuck(win: Win,
                players: list):
        win.SetVKReq(VKRoulette.VK_REQ)
        win.WhoWin(players)

    @staticmethod
    def Roulette(rules: list[Rule],
                 win: Win = Win(),
                 group_links: list[str] = None,
                 exceptions=None):
        players = VKRoulette.GetParticipants(rules)
        players = VKRoulette.ClearingGroupsFromParticipation(players)
        players = VKRoulette.ExcludeExceptions(players,
                                               group_links,
                                               exceptions)
        VKRoulette.TryLuck(win, players)
        # print(VKRoulette.VK_REQ.GetComments(-204044583, 1111, need_name=True))


VKRoulette.Roulette(
    rules=[
        Rule(
            rule_data=RuleData(
                rule_type=RuleType.COMMENT,
                activity_type=AC.EMOJI
            ).GetData(),
            links=[
                "https://vk.com/wall-204044583_1143"
            ]),
        Rule(
            rule_data=RuleData(
                rule_type=RuleType.SUBSCRIBE
            ).GetData(),
            links=[
                "https://vk.com/camshel"
            ])
    ],
    win=Win(
        win_data=WinData(
            win_type=WinType.EMOJI_DATA,
            win_count=2
        ).GetData(),
        link="https://vk.com/wall-204044583_1143"
    )
)
