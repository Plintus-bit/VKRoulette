------ Пакеты:
cond_enums - различные условия (Condition) в формате перечислений (Enum) для удобного использования
rules - условия игры (Rule) и победы (Win)
text_process - обработка текстовой информации

------ Классы:
CC (Consider Condition) - условие учёта данных. Что для нас важно при определении участников
AC (Activity Condition) - условие действия. Что является принятием участия и что это даёт
RuleType - тип действия для участия
WinType - способ определения победителя

Data - базовый класс для условий рулетки
Rule - определяет одно "правило" для нахождения участников
Win - определяет одно "правило победы" для выбора победителей
RuleData/WinData - наборы параметров правила/победы

DataRetrieval - получение нужных для выборки и/или оглашения победителей данных из всех имеющхся
TextSeparation - получение набора данных из строки текста (поиск по шаблонам)
TextTags - теги для обращения в информации

VKRequests - взаимодействие с VK Api
VKRoulette - проведение конкурса

------ Данные для проведения конкурса:
--- rules (правила) - список наборов правил для определения участников **
- rule_data - условия правила
rule_type - тип **
activity_type - тип участия
consider_type - тип выборки
msg_data - сообщение для выборки (не нужно, если тип участия НЕ TEXT_DATA)
- links - ссылки на посты с данными условиями

--- win - список правил для определения победителей
- win_data - условия победы
win_type - способ определения победителя
win_count - число победителей
- link - пост для определения победителя (не нужно, если тип победы НЕ NUMERIC)

--- group_links - список ссылок на группы, если нужно исключить их анминов, модераторов, редакторов и т.п., кто есть в контактах пабликов
--- exceptions - список ссылок на участников, которых нужно исключить из розыгрыша

** - обязательно