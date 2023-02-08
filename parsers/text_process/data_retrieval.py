from parsers.cond_enums.win_type import WinType
from parsers.text_process.text_separation import TextSeparator
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class DataRetrieval:
    @staticmethod
    def GetPlayersName(vk_req: VKRequests,
                       players_id: list) -> list[str]:
        players = []
        players_data = vk_req.GetUsers(players_id)
        for player_data in players_data:
            players.append(DataRetrieval.GetName(player_data))
        return players

    @staticmethod
    def GetPlayersNameAndNumeric(vk_req: VKRequests,
                                 players_id: list,
                                 link: str) -> list[dict]:
        players = []
        link_data = TextSeparator.GetLinkData(link)
        players_data = vk_req.GetComments(link_data.group(1),
                                          link_data.group(2),
                                          need_name=True)
        players_data = DataRetrieval.__GetPlayersDataAndProfiles(players_data[0],
                                                                 players_data[1])
        for player_data in players_data:
            if player_data[TextTags.FROM_ID] in players_id\
                    and TextSeparator.IsContainNumeric(player_data[TextTags.TEXT]):
                player = dict()
                player[TextTags.NAME] = DataRetrieval.GetName(player_data)
                player[TextTags.DATA] = TextSeparator.GetNumericData(player_data[TextTags.TEXT])
                players.append(player)
        return players

    @staticmethod
    def __GetPlayersDataAndProfiles(players_data,
                                    profiles):
        for player_data in players_data:
            for profile in profiles:
                if player_data[TextTags.FROM_ID] == profile[TextTags.ID]:
                    player_data[TextTags.FIRST_NAME] = profile[TextTags.FIRST_NAME]
                    player_data[TextTags.LAST_NAME] = profile[TextTags.LAST_NAME]
                    break
        return players_data

    @staticmethod
    def GetPlayersNameAndChance(vk_req: VKRequests,
                                players_id: list) -> list[dict]:
        players = []
        players_data = vk_req.GetUsers(players_id)
        for player_data in players_data:
            player = dict()
            player[TextTags.NAME] = DataRetrieval.GetName(player_data)
            chance = players_id.count(player_data[TextTags.ID])
            player[TextTags.CHANCE] = str(chance)
            players.append(player)
        return players

    @staticmethod
    def GetName(player_data):
        names_separator = " "
        return player_data[TextTags.FIRST_NAME]\
               + names_separator\
               + player_data[TextTags.LAST_NAME]

    @staticmethod
    def GetPlayersNameAndText(vk_req: VKRequests,
                              players_id: list,
                              link: str,
                              win_type: WinType = WinType.DATA):
        players = []
        link_data = TextSeparator.GetLinkData(link)
        players_data = vk_req.GetComments(link_data.group(1),
                                          link_data.group(2),
                                          need_name=True)
        players_data = DataRetrieval.__GetPlayersDataAndProfiles(players_data[0],
                                                                 players_data[1])
        if win_type == WinType.EMOJI_DATA:
            for player_data in players_data:
                if player_data[TextTags.FROM_ID] in players_id\
                        and TextSeparator.IsEmoji(str(player_data[TextTags.TEXT])):
                    player = dict()
                    player[TextTags.NAME] = DataRetrieval.GetName(player_data)
                    player[TextTags.DATA] = player_data[TextTags.TEXT]
                    players.append(player)
        else:
            for player_data in players_data:
                if player_data[TextTags.FROM_ID] in players_id:
                    player = dict()
                    player[TextTags.NAME] = DataRetrieval.GetName(player_data)
                    player[TextTags.DATA] = player_data[TextTags.DATA]
                    players.append(player)
        return players
