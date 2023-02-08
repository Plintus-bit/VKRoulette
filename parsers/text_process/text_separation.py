from re import search, Match
from emoji import is_emoji
import advertools as adv

from parsers.text_process.text_tags import TextTags


class TextSeparator:
    @staticmethod
    def GetLinkData(link: str) -> Match[str]:
        pattern = r'wall(-[0-9]*)_([0-9]*)'
        return search(pattern, link)

    @staticmethod
    def GetShortNameOrId(link: str):
        template = r'https://vk.com/([0-9a-zA-Z_-]*)'
        return search(template, link).group(1)

    @staticmethod
    def GetGroupNameOrId(link: str):
        group_name = TextSeparator.GetShortNameOrId(link)
        if group_name.isdecimal():
            group_name = group_name[1:]
        return group_name

    @staticmethod
    def IsContainText(text: str,
                      need_to_contain: str) -> bool:
        text = text.lower()
        template = r'' + need_to_contain.lower()
        return search(template, text) is not None

    @staticmethod
    def IsContainNumeric(text: str) -> bool:
        template = r'[0-9-]*'
        return search(template, text) is not None

    @staticmethod
    def GetNumericData(text: str):
        template = r'[0-9-]*'
        return int(search(template, text).group(0))

    @staticmethod
    def IsEmoji(text: str) -> bool:
        return adv.extract_emoji([text])[TextTags.EMOJI_COUNTS][0] > 0
