from re import search, Match


class TextSeparator:
    @staticmethod
    def GetLinkData(link: str) -> Match[str]:
        pattern = r'wall(-[0-9]*)_([0-9]*)'
        return search(pattern, link)

    @staticmethod
    def GetShortNameOrId(exc_pl: str):
        template = r'https://vk.com/([0-9a-zA-Z_-]*)'
        return search(template, exc_pl).group(1)

    @staticmethod
    def IsContainText(text: str,
                      need_to_contain: str):
        text = text.lower()
        template = r'' + need_to_contain.lower()
        return search(template, text) is not None

    @staticmethod
    def IsContainNumeric(text: str):
        template = r'[0-9-]*'
        return search(template, text) is not None

    @staticmethod
    def GetNumericData(text: str):
        template = r'[0-9-]*'
        return int(search(template, text).group(0))

