import sqlite3

class Base:

    def __init__(self, namebase):
        self.__base = sqlite3.connect(namebase)
        self.check_base_start()
        self.__cur = self.__base.cursor()
        self.__cur.execute("""select * from sqlite_master where type = 'table'""")


    def check_base_start(self):
        if self.__base:
            print('DateBase connected...OK')
        elif self.__base is None:
            print('DateBase connected...NOT OK')

    @property
    def fetchall(self):
        return self.__cur.fetchall()

    def execute_user(self, name, id, data):
        return self.__cur.execute("SELECT game, sum(time) FROM {} WHERE userid == ? AND datetime > ? GROUP BY game".format(name),(id, data)).fetchall()

    def execute_user2(self, name):
        return self.__cur.execute('SELECT userid, sum(time) FROM {} GROUP BY game'.format(name)).fetchall()

    def execute_users(self, name):
        return self.__cur.execute('SELECT userid, sum(time) FROM {} GROUP BY userid'.format(name)).fetchall()

    def execute_statistics(self, name):
        return self.__cur.execute('SELECT game, sum(time) FROM {} GROUP BY game'.format(name)).fetchall()

    def execute_top_3(self, plug, table, months_minus, data):
        if plug == 'game':
            print(self.__cur.execute('SELECT game, SUM(time) FROM {} WHERE datetime BETWEEN ? AND ? GROUP BY game '
                                      'ORDER BY time DESC LIMIT 3'.format(table), (months_minus, data)).fetchall())
            return self.__cur.execute('SELECT game, SUM(time) FROM {} WHERE datetime BETWEEN ? AND ? GROUP BY game '
                                      'ORDER BY time DESC LIMIT 3'.format(table), (months_minus, data)).fetchall()
        elif plug == 'userid':
            return self.__cur.execute('SELECT userid, SUM(time) FROM {} WHERE datetime BETWEEN ? AND ? GROUP BY game '
                                      'ORDER BY time DESC LIMIT 3'.format(table), (months_minus, data)).fetchall()

    @property
    def execute_check(self, name):
        self.__base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
        self.__base.commit()

    def check(self, name, id):
        return self.__cur.execute('SELECT * FROM {} WHERE userid == ?'.format(name), (id,)).fetchone()

    @property
    def base_update(self, name, id):
        warning = self.check(name, id)
        if warning is None:
            self.__base.execute('INSERT INTO {} VALUES(?, ?)'.format(name), (id, 1))
            self.__base.commit()
        else:
            self.__base.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (warning[1] + 1, id))
            self.__base.commit()

    @property
    def create_table(self, name):
        self.__base.execute(
            'CREATE TABLE IF NOT EXISTS {}(userid INT, game TEXT, datetime DATETIME, time INT)'.format(name))
        self.__base.commit()


    @property
    def base_insert(self, name, user_id, game, time_start, game_time):
        self.__base.execute('INSERT INTO {} VALUES(?, ?, ?, ?)'.format(name), (user_id, game, time_start, game_time))
        self.__base.commit()
