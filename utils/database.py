from sqlite3 import connect
from shutil import copyfile
from datetime import datetime


class DataBase:

    def __init__(self):
        self.connection = connect("data.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS reports(date TEXT, reporter TEXT, message TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS guilds(id INTEGER PRIMARY KEY, lang TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS banwords(guild INTEGER, word TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS offenses(guild INTEGER, user INTEGER, date TEXT, duration INTEGER, type INTEGER, reason TEXT)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS items()")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS orders()")
        self.connection.commit()

    def save_backup(self):
        self.cursor.close()
        self.connection.close()
        copyfile("data.db", f"backups/{str(datetime.now())[:16].replace(' ', '-').replace(':', '-')}.db")
        self.__init__()
        return self

    def add_guild(self, guild_id: int):
        self.cursor.execute(f"INSERT INTO guilds (id) VALUES ({guild_id})")
        self.connection.commit()
        return self.cursor

    def remove_guild(self, guild_id: int):
        self.cursor.execute(f"DELETE FROM guilds WHERE id={guild_id}")
        self.connection.commit()
        return self.cursor

    def edit_guild(self, guild_id: int, lang: str = None):
        if lang is not None:
            self.cursor.execute(f"UPDATE guilds SET lang={lang} WHERE id={guild_id}")
        self.connection.commit()
        return self.cursor

    def get_guild(self, guild_id):
        self.cursor.execute(f"SELECT * FROM guilds WHERE id={guild_id}")
        for value in self.cursor:
            return value
        return None

    def get_guilds(self):
        guilds = []
        self.cursor.execute(f"SELECT * FROM guilds")
        for value in self.cursor:
            guilds.append(value)
        return guilds

    def add_banword(self, guild_id, banword):
        self.cursor.execute(f"INSERT INTO banwords (guild, word) VALUES ({guild_id}, \"{banword}\")")
        self.connection.commit()
        return self.cursor

    def remove_banword(self, guild_id, banword):
        if self.banword_exists(guild_id, banword):
            self.cursor.execute(f"DELETE FROM banwords WHERE guild={guild_id} AND word=\"{banword}\"")
            self.connection.commit()
            return True
        else:
            return False

    def banword_exists(self, guild_id, banword):
        self.cursor.execute(f"SELECT * FROM banwords WHERE guild={guild_id} AND word=\"{banword}\"")
        for value in self.cursor:
            return True
        return False

    def get_banwords(self, guild_id):
        banwords = []
        self.cursor.execute(f"SELECT * FROM banwords WHERE guild={guild_id}")
        for value in self.cursor:
            banwords.append(value[1])
        return banwords

    def add_offense(self, guild_id, user_id, type, duration, reason):
        self.cursor.execute(f"INSERT INTO offenses (guild, user, date, duration, type, reason) VALUES ({guild_id}, {user_id}, \"{str(datetime.now())[:16]}\", {duration}, {type}, \"{reason}\")")
        self.connection.commit()
        return self.cursor

    def remove_offenses(self, guild_id, user_id):
        self.cursor.execute(f"DELETE FROM offenses WHERE guild={guild_id} AND user={user_id}")
        self.connection.commit()
        return self.cursor

    def get_offenses(self, guild_id, user_id):
        offenses = []
        self.cursor.execute(f"SELECT * FROM offenses WHERE guild={guild_id} AND user={user_id}")
        for value in self.cursor:
            offenses.append(value)
        return offenses

    def add_report(self, reporter, message):
        self.cursor.execute(f"INSERT INTO reports (date, reporter, message) VALUES (\"{str(datetime.now())[:16]}\", \"{reporter}\", \"{message}\")")
        self.connection.commit()
        return self.cursor

    def get_reports(self):
        reports = []
        self.cursor.execute("SELECT * FROM reports")
        for value in self.cursor:
            reports.append(value)
        return reports
