from json import load


class Languages:

    def __init__(self):
        self.lang = "en_US"
        try:
            with open(file="assets/lang.json", mode="r", encoding="utf-8") as file:
                self.file = load(file)
        except IOError:
            with open(file="assets/lang.json", mode="w", encoding="utf-8") as file:
                file.write("{}")
            self.reload()

    def reload(self):
        self.__init__()
        return self

    def set_lang(self, lang: str):
        self.lang = lang
        return self

    def get_path(self, path: str, lang: str = None):
        try:
            return self.file[(lang, self.lang)[lang is None]][path]
        except KeyError:
            return None
