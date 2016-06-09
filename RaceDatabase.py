import sqlite3


class RaceDatabase(object):
    def __init__(self, database='f1siteraces.db'):
        self.__database = database
        self.__connection = sqlite3.connect(self.__database)
        self.__connection
        self.__connection.row_factory = sqlite3.Row
        self.cursor = self.__connection.cursor()

    def initial_setup(self):
        self.cursor.execute("DROP TABLE IF EXISTS drivers")
        self.cursor.execute(
            "CREATE TABLE drivers(driver_id INTEGER NOT NULL UNIQUE, first_name TEXT NOT NULL, " +
            "last_name TEXT NOT NULL, rating INTEGER NOT NULL DEFAULT 1350, first_race INTEGER NOT NULL DEFAULT 1, " +
            "last_race INTEGER NOT NULL DEFAULT 1 PRIMARY KEY(driver_id))")

        self.cursor.execute("DROP TABLE IF EXISTS races")
        self.cursor.execute(
            "CREATE TABLE races(race_id INTEGER NOT NULL UNIQUE, year INTEGER NOT NULL, race_num INTEGER NOT NULL, " +
            "race_name TEXT NOT NULL, strength_of_field INTEGER, rating_available INTEGER, total_gain INTEGER, " +
            "PRIMARY KEY(race_id))")

    # Drivers
    def new_driver(self, first_name, last_name):
        self.cursor.execute("INSERT INTO drivers VALUES(?,?,?,?,?,?)", (None, first_name, last_name, 1350, 0, 0))
        self.__connection.commit()

    def update_driver_rating(self, driver_id, rating):
        statement = "UPDATE drivers SET rating=? WHERE driver_id=?"
        self.cursor.execute(statement, [rating, driver_id])
        self.__connection.commit()

    def update_driver_first_race(self, driver_id, first_race):
        statement = "UPDATE drivers SET first_race=? WHERE driver_id=?"
        self.cursor.execute(statement, [first_race, driver_id])
        self.__connection.commit()

    def update_driver_last_race(self, driver_id, last_race):
        statement = "UPDATE drivers SET last_race=? WHERE driver_id=?"
        self.cursor.execute(statement, [last_race, driver_id])
        self.__connection.commit()

    def get_driver_by_name(self, first_name, last_name):
        self.cursor.execute("SELECT * FROM drivers WHERE first_name=? AND last_name=?", [first_name, last_name])
        driver = self.cursor.fetchone()
        return driver

    def get_driver_by_id(self, driver_id):
        self.cursor.execute("SELECT * FROM drivers WHERE driver_id=?", [driver_id])
        driver = self.cursor.fetchone()
        return driver

    def get_driver_rating(self, driver_id):
        driver = self.get_driver_by_id(driver_id)
        return driver['rating']

    def get_all_drivers(self):
        self.cursor.execute("SELECT * FROM drivers")
        drivers = self.cursor.fetchall()
        return drivers

    # Races
    def new_race(self, season, race_num, race_name):
        self.cursor.execute("INSERT INTO races VALUES(?, ?, ?, ?, ?, ?, ?)", (None, season, race_num, race_name, 0, 0, 0))

        statement = "DROP TABLE IF EXISTS `%s`" % race_name
        self.cursor.execute(statement)
        statement = "CREATE TABLE `%s`(finish_id INTEGER NOT NULL UNIQUE, name_id INTEGER NOT NULL, " + \
                    "adjustment INTEGER, prediction INTEGER, pos_gain INTEGER, share REAL, gain INTEGER, " + \
                    "old_rating INTEGER, new_rating INTEGER, PRIMARY KEY(finish_id), " + \
                    "FOREIGN KEY(name_id) REFERENCES drivers(driver_id))" % race_name
        self.cursor.execute(statement)
        self.__connection.commit()

    def populate_race_info(self, race_name, driver_id):
        statement = "INSERT INTO `%s` VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)" % (race_name)
        self.cursor.execute(statement, (None, driver_id, 0, 0, 0, 0, 0, 0, 0))
        self.__connection.commit()

    def update_overview(self, race_id, sof, available, total_gain):
        statement = "UPDATE races SET strength_of_field=?, rating_available=?, total_gain=? WHERE race_id=?"
        self.cursor.execute(statement, (sof, available, total_gain, race_id))
        self.__connection.commit()

    def update_driver_in_race(self, driver, race_name):
        driver_info = (driver['finish_id'], driver['name_id'], driver['adjustment'], driver['prediction'],
                       driver['pos_gain'], driver['share'], driver['gain'], driver['old_rating'], driver['new_rating'],
                       driver['name_id'])
        statement = "UPDATE `%s` SET finish_id=?, name_id=?, adjustment=?, prediction=?, pos_gain=?, share=?, " + \
                    "gain=?, old_rating=?, new_rating=? WHERE name_id=?" % race_name
        self.cursor.execute(statement, driver_info)
        self.__connection.commit()

    def get_race_name_by_id(self, race_id):
        self.cursor.execute("SELECT * FROM races WHERE race_id=?", [race_id])
        race = self.cursor.fetchone()
        return race['race_name']

    def get_race_name_by_year_and_number(self, year, race_number):
        self.cursor.execute("SELECT * FROM races WHERE year=? AND race_num=?", [year, race_number])
        race = self.cursor.fetchone()
        return race['race_name']

    def get_race_info_by_name(self, race_name):
        statement = "SELECT * FROM `%s`" % race_name
        self.cursor.execute(statement)
        race = self.cursor.fetchall()
        return race

    def get_race_id_by_year_and_number(self, year, race_num):
        statement = "SELECT * FROM races WHERE year=? AND race_num=?"
        args = (year, race_num)
        self.cursor.execute(statement, args)
        race = self.cursor.fetchone()
        return int(race[0])

    def get_race_info_sorted_by(self, race_name, criteria, direction='ascending'):
        if direction == 'ascending':
            statement = "SELECT * FROM `%s` ORDER BY old_rating ASC" % race_name
        else:
            statement = "SELECT * FROM `%s` ORDER BY old_rating DESC" % race_name
        self.cursor.execute(statement)
        race_info = self.cursor.fetchall()
        return race_info

    def get_overview(self, race_id):
        statement = "SELECT * FROM races WHERE race_id=?"
        self.cursor.execute(statement, [race_id])
        overview = self.cursor.fetchone()
        return dict(overview)

    def get_driver_from_race(self, race_name, driver_id):
        statement = "SELECT * FROM `%s` WHERE name_id=?" % race_name
        self.cursor.execute(statement, [driver_id])
        driver = self.cursor.fetchone()
        if driver is None:
            return driver
        else:
            return dict(driver)

    def get_all_races(self):
        statement = "SELECT * FROM races"
        self.cursor.execute(statement)
        races = self.cursor.fetchall()
        return races

    def number_of_races(self):
        statement = "SELECT COUNT(*) FROM races"
        self.cursor.execute(statement)
        return self.cursor.fetchone()

    def close(self):
        self.__connection.close()

    # Clean up
    def clear_races_from_year(self, clearYear):
        numRaces = self.number_of_races()[0]
        lastRace = self.get_overview(numRaces)
        lastYear = lastRace['year']

        for year in range(clearYear, lastYear+1):
            statement = "DELETE FROM races WHERE year=?"
            self.cursor.execute(statement, [year])

        self.__connection.commit()

