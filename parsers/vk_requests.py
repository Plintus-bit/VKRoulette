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
    def __MergeData(data: list) -> list[str]:
        result_data_array = []
        res_data = ""
        separator = ","
        count = 0
        full_count = 0
        for r_data in data:
            res_data += str(r_data) + separator
            count += 1
            full_count += 1
            if count == 1000 or full_count == len(data):
                result_data_array.append(res_data[:len(res_data) - 1])
                res_data = ""
                count = 0
        return result_data_array

    def GetReposts(self, owner_id: int, post_id: int):
        return self.api.wall.getReposts(owner_id=owner_id, post_id=post_id)

    def GetLikes(self, owner_id: int, post_id: int):
        VKRequests.__GoToSleep()
        divider = 1000
        first = self.api.wall.getLikes(owner_id=owner_id,
                                       post_id=post_id,
                                       count=divider,
                                       offset=0)
        data = first[TextTags.USERS]
        count = first[TextTags.COUNT] // divider
        for i in range(1, count + 1):
            VKRequests.__GoToSleep()
            data += self.api.wall.getLikes(owner_id=owner_id,
                                           post_id=post_id,
                                           count=divider,
                                           offset=i * divider)[TextTags.USERS]
        return data

    def GetComments(self,
                    owner_id: int,
                    post_id: int,
                    need_name: bool = False,
                    comment_id: int = -1):
        divider = 100
        VKRequests.__GoToSleep()
        if need_name:
            if comment_id < 0:
                first = self.api.wall.getComments(owner_id=owner_id,
                                                  post_id=post_id,
                                                  extended=1,
                                                  fields="first_name,last_name",
                                                  count=divider)
                data = first[TextTags.ITEMS]
                data_2 = first[TextTags.PROFILES]
                count = first[TextTags.COUNT] // divider
                for i in range(1, count + 1):
                    temp = self.api.wall.getComments(owner_id=owner_id,
                                                     post_id=post_id,
                                                     extended=1,
                                                     fields="first_name,last_name",
                                                     count=divider,
                                                     offset=i * divider)[TextTags.ITEMS]
                    data += temp[TextTags.ITEMS]
                    data_2 += temp[TextTags.PROFILES]
                return data, data_2
            first = self.api.wall.getComments(owner_id=owner_id,
                                              post_id=post_id,
                                              extended=1,
                                              fields="first_name,last_name",
                                              comment_id=comment_id,
                                              count=divider)
            data = first[TextTags.ITEMS]
            data_2 = first[TextTags.PROFILES]
            count = first[TextTags.COUNT] // divider
            for i in range(1, count + 1):
                temp = self.api.wall.getComments(owner_id=owner_id,
                                                 post_id=post_id,
                                                 extended=1,
                                                 fields="first_name,last_name",
                                                 comment_id=comment_id,
                                                 count=divider,
                                                 offset=i * divider)[TextTags.ITEMS]
                data += temp[TextTags.ITEMS]
                data_2 += temp[TextTags.PROFILES]
            return data, data_2
        if comment_id < 0:
            first = self.api.wall.getComments(owner_id=owner_id,
                                              post_id=post_id,
                                              count=divider)
            data = first[TextTags.ITEMS]
            count = first[TextTags.COUNT] // divider
            for i in range(1, count + 1):
                data += self.api.wall.getComments(owner_id=owner_id,
                                                  post_id=post_id,
                                                  offset=i * divider,
                                                  count=divider)[TextTags.ITEMS]
            return data
        first = self.api.wall.getComments(owner_id=owner_id,
                                          post_id=post_id,
                                          comment_id=comment_id,
                                          count=divider)
        data = first[TextTags.ITEMS]
        count = first[TextTags.COUNT] // divider
        for i in range(1, count + 1):
            data += self.api.wall.getComments(owner_id=owner_id,
                                              post_id=post_id,
                                              comment_id=comment_id,
                                              count=divider,
                                              offset=i * divider)[TextTags.ITEMS]
        return data

    def GetUsers(self, user_ids: list):
        data = self.__MergeData(user_ids)
        result_data: list = None
        for item in data:
            if result_data is None:
                result_data = self.api.users.get(user_ids=item)
            else:
                result_data.extend(self.api.users.get(user_ids=item))
            VKRequests.__GoToSleep()
        return result_data

    def GetGroupContacts(self, group_ids: list):
        data = self.__MergeData(group_ids)
        result_data: list = None
        for item in data:
            if result_data is None:
                result_data = self.api.groups.getById(group_id=item,
                                                      fields="contacts")[TextTags.CONTACTS]
            else:
                result_data.extend(self.api.groups.getById(group_id=item,
                                                           fields="contacts")[TextTags.CONTACTS])
            VKRequests.__GoToSleep()
        return result_data

    def GetSubscribers(self, group_id):
        VKRequests.__GoToSleep()
        divider = 500
        first = self.api.groups.getMembers(group_id=group_id,
                                           count=divider)
        data = first[TextTags.ITEMS]
        count = first[TextTags.COUNT] // divider
        for i in range(1, count + 1):
            VKRequests.__GoToSleep()
            data += self.api.groups.getMembers(group_id=group_id,
                                               count=divider,
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
