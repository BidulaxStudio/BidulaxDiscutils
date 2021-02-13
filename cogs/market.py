from discord.ext import commands


class Market(commands.Cog):

    def __init__(self, data, lang, bot):
        self.data = data
        self.lang = lang
        self.bot = bot

    def addItem(self):
        pass

    def removeItem(self):
        pass

    def modifyItem(self):
        pass

    def getItems(self):
        pass
    
    def order(self):
        pass

    def removeOrder(self):
        pass

    def confirmOrder(self):
        pass

    def terminateOrder(self):
        pass

    def getOrders(self):
        pass
