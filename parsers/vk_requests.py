import vk


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

    def GetReposts(self, owner_id: int, post_id: int):
        return self.api.wall.getReposts(owner_id=owner_id, post_id=post_id)

    def GetLikes(self, owner_id: int, post_id: int):
        return self.api.wall.getLikes(owner_id=owner_id, post_id=post_id)

    def GetComments(self, owner_id: int, post_id: int, comment_id: int = -1):
        if comment_id < 0:
            return self.api.wall.getComments(owner_id=owner_id, post_id=post_id)
        return self.api.wall.getComments(owner_id=owner_id, post_id=post_id, comment_id=comment_id)

    def GetUsers(self, user_ids):
        users = ""
        separator = ","
        for user_id in user_ids:
            users += str(user_id) + separator
        users = users[:len(users) - 1]
        return self.api.users.get(user_ids=users)
