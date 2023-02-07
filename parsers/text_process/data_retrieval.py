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
        players_data = vk_req.GetUsers(players_id)
        link_data = TextSeparator.GetLinkData(link)
        max_players_data = vk_req.GetComments(link_data.group(1),
                                              link_data.group(2))[TextTags.ITEMS]

        for pl_data_index in range(len(max_players_data)):
            if int(max_players_data[pl_data_index][TextTags.FROM_ID]) in players_id:
                max_players_data[pl_data_index][TextTags.FIRST_NAME] = players_data[pl_data_index][TextTags.FIRST_NAME]
                max_players_data[pl_data_index][TextTags.LAST_NAME] = players_data[pl_data_index][TextTags.LAST_NAME]

        for player_data in max_players_data:
            if player_data[TextTags.FROM_ID] in players_id\
                    and TextSeparator.IsContainNumeric(player_data[TextTags.TEXT]):
                player = dict()
                player[TextTags.NAME] = DataRetrieval.GetName(player_data)
                player[TextTags.NUMERIC] = TextSeparator.GetNumericData(
                    player_data[TextTags.TEXT])
                players.append(player)
        return players

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