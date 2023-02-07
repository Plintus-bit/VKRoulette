import re
from re import Match

from parsers.cond_enums.activity_cond import AC
from parsers.cond_enums.consider_cond import CC
from parsers.cond_enums.rule_type import RuleType
from parsers.rules.rule_data import RuleData
from parsers.text_process.text_separation import TextSeparator
from parsers.text_process.text_tags import TextTags
from parsers.vk_requests import VKRequests


class Rule:
    # DEFAULT_ADDRESS = "https://vk.com/"

    def __init__(self,
                 rule_data: dict,
                 links: list[str],
                 vk_req: VKRequests = None):
        self.__vk_req = vk_req
        self.__links = links
        self.__rule_data = rule_data

    def SetVKReq(self, vk_req: VKRequests):
        self.__vk_req = vk_req

    def ParsePlayersData(self, link_data: Match[str]):
        # должен вернуть игроков
        if self.__rule_data[RuleData.RULE_TYPE] == RuleType.LIKE:
            return self.ParseLikesData(link_data)

        if self.__rule_data[RuleData.RULE_TYPE] == RuleType.REPOST:
            return self.ParseRepostsData(link_data)

        if self.__rule_data[RuleData.RULE_TYPE] == RuleType.COMMENT:
            return self.ParseCommentsData(link_data)

    def ParseLikesData(self, link_data: Match[str]):
        players = []
        players_data = self.__vk_req.GetLikes(
            link_data.group(1),
            link_data.group(2))[TextTags.USERS]
        for player_data in players_data:
            players.append(player_data[TextTags.UID])
        return players

    def ParseRepostsData(self, link_data: Match[str]):
        players = []
        players_data = self.__vk_req.GetReposts(
            link_data.group(1),
            link_data.group(2))[TextTags.ITEMS]
        for player_data in players_data:
            players.append(player_data[TextTags.FROM_ID])
        return players

    def ParseCommentsData(self, link_data: Match[str]):
        players_data = self.__vk_req.GetComments(
            link_data.group(1),
            link_data.group(2))[TextTags.ITEMS]
        players = self.ParseComments(players_data, [])

        if self.__rule_data[RuleData.CONSIDER] == CC.ALL_COMMENTS:
            for player_data in players_data:
                if int(player_data[TextTags.THREAD][TextTags.COUNT]) > 0:
                    temp_data = self.__vk_req.GetComments(
                        link_data.group(1),
                        link_data.group(2),
                        player_data[TextTags.ID]
                    )[TextTags.ITEMS]
                    players = self.ParseComments(temp_data, players)
        return players

    def ParseComments(self, players_data,
                      players: list):
        if self.__rule_data[RuleData.ACTIVITY] == AC.ONE_COMMENT:
            for player_data in players_data:
                if player_data[TextTags.FROM_ID] not in players:
                    players.append(player_data[TextTags.FROM_ID])
        elif self.__rule_data[RuleData.ACTIVITY] == AC.MANY_COMMENTS:
            for player_data in players_data:
                players.append(player_data[TextTags.FROM_ID])
        elif self.__rule_data[RuleData.ACTIVITY] == AC.TEXT_DATA:
            for player_data in players_data:
                if TextSeparator.IsContainText(str(player_data[TextTags.TEXT]),
                                               str(self.__rule_data[RuleData.MSG])):
                    players.append(player_data[TextTags.FROM_ID])
        return players

    def GetLinks(self):
        return self.__links

    def SetLinks(self, links: list[str]):
        self.__links = links

    def GetPlayers(self, players: list):
        if players is None:
            players = []
        links = self.GetLinks()
        for link in links:
            part_players = self.ParsePlayersData(TextSeparator.GetLinkData(link))
            if len(players) == 0:
                players = part_players
            else:
                players = Rule.ComparePlayersAndGetFixedList(players, part_players)
        return players

    @staticmethod
    def ComparePlayersAndGetFixedList(now_play: list, part_play: list):
        # now_play - выполнившие предыдующие условия
        # part_play - участвующие в данной части условия
        result_players = []
        for player in now_play:
            if player in part_play:
                result_players.append(player)
        return result_players
