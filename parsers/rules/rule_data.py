from parsers.cond_enums.rule_types import RuleType
from parsers.cond_enums.consider_cond import CC
from parsers.cond_enums.activity_cond import AC


class RuleData:
    RULE_TYPE = "rule_type"
    ACTIVITY = "activity"
    CONSIDER = "consider"
    MSG = "msg"

    def __init__(self,
                 rule_type: RuleType,
                 activity_type: AC = AC.DEFAULT,
                 consider_type: CC = CC.BASIC_COMMENT_ONLY,
                 msg_data: str = ""):
        self.rule_type = rule_type
        self.activity_type = activity_type
        self.consider_type = consider_type
        self.msg_data = msg_data

    def GetRuleData(self) -> dict:
        rule_data = dict()
        rule_data[RuleData.RULE_TYPE] = self.rule_type
        rule_data[RuleData.ACTIVITY] = self.activity_type
        rule_data[RuleData.CONSIDER] = self.consider_type
        rule_data[RuleData.MSG] = self.msg_data
        return rule_data
