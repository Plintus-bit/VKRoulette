from time import sleep

import vk
from parsers.text_process.text_tags import TextTags


class VKRequests:
    TOKEN = "vk1.a.zFqHBEyA0bJAZM97nPfeBqbZmY" \
            "fD_tiT3HhWDXon7hKZH3smZ_vrZmfhnz" \
            "V2MGflLeG-QtCDG_dQvpEbcyHH_vDVO9" \
            "eTH_iEpV_H3FaiiHWsOzD6sh2Z2XcPFR" \
            "DeGuIQLz7xvYd8zxDAjvLxPQ0KPyxJEs" \
            "Mu124DGcuyBVBh2x33-GSjUUGSCmc8UQ" \
            "V3FTDs0gj8pZg62jaOMfF0gb6--g"
    VERSION = "5.131"

    def __init__(self):
        self.api = vk.API(access_token=VKRequests.TOKEN,
                          v=VKRequests.VERSION)

    @staticmethod
    def __MergeData(data: list):
        res_data = ""
        separator = ","
        for r_data in data:
            res_data += str(r_data) + separator
        return res_data[:len(res_data) - 1]

    def GetReposts(self, owner_id: int, post_id: int):
        divider = 1000
        first = self.api.wall.getReposts(owner_id=owner_id, post_id=post_id)
        data = first[TextTags.ITEMS]
        count = first[TextTags.COUNT] // divider
        for i in range(1, count+1):
            data += self.api.wall.getReposts(owner_id=owner_id, post_id=post_id, offset=i*divider)[TextTags.ITEMS]
        return data

    def GetLikes(self, owner_id: int, post_id: int):
        divider = 1000
        first = self.api.wall.getLikes(owner_id=owner_id, post_id=post_id)
        data = first[TextTags.ITEMS]
        count = first[TextTags.COUNT] // divider
        for i in range(1, count + 1):
            data += self.api.wall.getLikes(owner_id=owner_id, post_id=post_id, offset=i * divider)[TextTags.ITEMS]
        return data

    def GetComments(self,
                    owner_id: int,
                    post_id: int,
                    need_name: bool = False,
                    comment_id: int = -1):
        divider = 100
        if need_name:
            if comment_id < 0:
                first = self.api.wall.getComments(owner_id=owner_id,
                                                  post_id=post_id,
                                                  extended=1,
                                                  fields="first_name,last_name")
                data = first[TextTags.ITEMS]
                data_2 = first[TextTags.PROFILES]
                count = first[TextTags.COUNT] // divider
                for i in range(1, count + 1):
                    temp = self.api.wall.getComments(owner_id=owner_id,
                                                     post_id=post_id,
                                                     extended=1,
                                                     fields="first_name,last_name",
                                                     offset=i * divider)
                    data += temp[TextTags.ITEMS]
                    data_2 += temp[TextTags.PROFILES]
                return data, data_2
            first = self.api.wall.getComments(owner_id=owner_id,
                                              post_id=post_id,
                                              extended=1,
                                              fields="first_name,last_name",
                                              comment_id=comment_id)
            data = first[TextTags.ITEMS]
            data_2 = first[TextTags.PROFILES]
            count = first[TextTags.COUNT] // divider
            for i in range(1, count + 1):
                temp = self.api.wall.getComments(owner_id=owner_id,
                                                 post_id=post_id,
                                                 extended=1,
                                                 fields="first_name,last_name",
                                                 comment_id=comment_id,
                                                 offset=i * divider)
                data += temp[TextTags.ITEMS]
                data_2 += temp[TextTags.PROFILES]
            return data, data_2
        if comment_id < 0:
            first = self.api.wall.getComments(owner_id=owner_id,
                                              post_id=post_id)
            data = first[TextTags.ITEMS]
            count = first[TextTags.COUNT] // divider
            for i in range(1, count + 1):
                data += self.api.wall.getComments(owner_id=owner_id,
                                                  post_id=post_id,
                                                  offset=i * divider)
            return data
        first = self.api.wall.getComments(owner_id=owner_id,
                                          post_id=post_id,
                                          comment_id=comment_id)
        data = first[TextTags.ITEMS]
        count = first[TextTags.COUNT] // divider
        for i in range(1, count + 1):
            data += self.api.wall.getComments(owner_id=owner_id,
                                              post_id=post_id,
                                              comment_id=comment_id,
                                              offset=i * divider)[TextTags.ITEMS]

    def GetUsers(self, user_ids: list):
        return self.api.users.get(user_ids=self.__MergeData(user_ids))

    def GetGroupContacts(self, group_ids: list):
        return self.api.groups.getById(group_id=self.__MergeData(group_ids),
                                       fields="contacts")[TextTags.CONTACTS]

    def GetSubscribers(self, group_id):
        divider = 500
        first = self.api.groups.getMembers(group_id=group_id)
        data = first[TextTags.ITEMS]
        count = first[TextTags.COUNT] // divider
        for i in range(1, count + 1):
            data += self.api.groups.getMembers(group_id=group_id,
                                               offset=i * divider)[TextTags.ITEMS]
        return data

    @staticmethod
    def __GoToSleep():
        sleep(0.5)

    def GetMembersOrNot(self,
                        group_id: str,
                        user_ids: list):
        return self.api.groups.isMember(group_id=group_id,
                                        user_ids=self.__MergeData(user_ids))
