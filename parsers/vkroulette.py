from parsers.cond_enums.activity_cond import AC
from parsers.cond_enums.consider_cond import CC
from parsers.cond_enums.rule_type import RuleType
from parsers.cond_enums.win_type import WinType
from parsers.rules.rule import Rule
from parsers.rules.rule_data import RuleData
from parsers.rules.win import Win
from parsers.rules.win_data import WinData
from parsers.text_process.text_separation import TextSeparator
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class VKRoulette:
    WHO_PLAY = "------Участвуют: "
    PLAYER = "Участник: "
    CHANCE = "--Шансы на победу: "
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
    def WhoPlay(players: list):
        print(VKRoulette.WHO_PLAY)
        players_name = VKRoulette.GetPlayersNameAndChance(players)
        for player_name in players_name:
            print(VKRoulette.PLAYER + player_name[TextTags.NAME])
            print(VKRoulette.CHANCE + player_name[TextTags.CHANCE])
            print()

    @staticmethod
    def GetPlayersNameAndChance(players_id: list) -> list:
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

    @staticmethod
    def GetContactExceptions(links: list[str]):
        group_ids = []
        for link in links:
            group_name = (TextSeparator.GetShortNameOrId(link))
            if group_name.isdecimal():
                group_name = group_name[1:]
            group_ids.append(group_name)
        return VKRoulette.VK_REQ.GetGroupContacts(group_ids)
    # ----------------- САМ РОЗЫГРЫШ ПО УСЛОВИЯМ --------------------

    @staticmethod
    def Roulette(rules: list[Rule],
                 win: Win = Win(),
                 group_links: list[str] = None,
                 exceptions=None):
        players = []
        if exceptions is None:
            exceptions = []

        for rule in rules:
            rule.SetVKReq(VKRoulette.VK_REQ)
            players = rule.GetPlayers(players)
        # если номер < 0, значит, коммент оставлен не от юзера (от группы)
        for player_id in players:
            if player_id < 0:
                players.remove(player_id)
        if exceptions:
            exceptions = VKRoulette.GetExceptionsPlayers(exceptions)
        if group_links is not None:
            contacts_exc = VKRoulette.GetContactExceptions(group_links)
            for contact_exc in contacts_exc:
                for contact in contact_exc[TextTags.CONTACTS]:
                    exceptions.append(contact[TextTags.USER_ID])

        for player_exc in exceptions:
            while player_exc in players:
                players.remove(player_exc)
        VKRoulette.WhoPlay(players)

        win.SetVKReq(VKRoulette.VK_REQ)
        win.WhoWin(players)

        # print(VKRoulette.VK_REQ.GetComments(-204044583, 1111))
        # print(VKRoulette.VK_REQ.GetComments(-204044583, 1111, 1115))


# VKRoulette.Roulette(
#     rules=[
#         Rule(
#             rule_data=RuleData(
#                 rule_type=RuleType.COMMENT,
#                 activity_type=AC.MANY_COMMENTS,
#                 consider_type=CC.ALL_COMMENTS
#             ).GetRuleData(),
#             links=[
#                 "https://vk.com/wall-204044583_1054"
#             ]),
#     ],
#     exceptions=[
#         "https://vk.com/plintus_ick",
#         "https://vk.com/akira_l",
#         "https://vk.com/wrong_gayborhood",
#         "https://vk.com/camshel"
#     ])

VKRoulette.Roulette(
    rules=[
        Rule(
            rule_data=RuleData(
                rule_type=RuleType.COMMENT,
                activity_type=AC.ONE_COMMENT,
                consider_type=CC.ALL_COMMENTS
            ).GetData(),
            links=[
                "https://vk.com/wall-204044583_1111"
            ])
    ],
    group_links=[
        "https://vk.com/camshel"
    ]
)
