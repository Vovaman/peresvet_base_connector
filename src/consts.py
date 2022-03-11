# файл с константами: коды ошибок и т.д.

class Error:
    def __init__(self, id, mes):
        self.id: int = id
        self.mes: str = mes

class Errors:
    CN_NO_CONF: Error = Error(1, "Не указан файл конфигурации")
    CN_WRONG_CONFIG: Error = Error(2, "Ошибка файла конфигурации")
    CN_WRONG_RESPONSE: Error = Error(3, "Неверный формат ответа платформы")

class StrVals:
    server: str = "server"
    id: str = "id"
    attrs: str = "attributes"
    tags: str = "tags"
    x: str = "x"
    y: str = "y"
    prev_value: str = "prev_value"
    cur_value: str = "cur_value"
    data: str = "data"
    tag_id: str = "tagId"
    prsValueTypeCode: str = "prsValueTypeCode"
    prsMaxDev: str = "prsMaxDev"
