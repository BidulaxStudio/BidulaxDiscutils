from json import load, dump


class Configuration:

    def __init__(self):
        try:
            with open(file="assets/config.json", mode="r", encoding="utf-8") as file:
                self.file = load(file)
        except IOError:
            base_config = {"name": "BidulaxDiscutils", "author": "BidulaxStudio", "token": ""}
            with open(file="assets/config.json", mode="w", encoding="utf-8") as file:
                dump(base_config, file)
            self.reload()

    def reload(self):
        self.__init__()
        return self

    def get_name(self):
        return self.file["name"]

    def get_token(self):
        return self.file["token"]