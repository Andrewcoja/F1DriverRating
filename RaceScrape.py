from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import RaceDatabase


class RaceScrape(object):
    def __init__(self, start_year=1950, initialize=False):
        self.raceDB = RaceDatabase.RaceDatabase()
        if initialize:
            self.raceDB.initial_setup()
            self.startYear = 1950
        else:
            self.startYear = start_year

        self.seasons = {}
        self.header = {'User-Agent': 'Mozilla/5.0'}

    def get_seasons_list(self, amount=65):
        print("Getting races by season:")
        for year in range(self.startYear, self.startYear+amount):
            url = "http://www.formula1.com/content/fom-website/en/results.html/" + str(year) + "/races/94/great-britain/race-result.html"
            req = Request(url, headers=self.header)
            page = urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            race_list = soup.find("select", {"name": "meetingKey"})
            if race_list is None:
                break;
            options_list = race_list.findAll("option")
            stored_race_list = []

            for option in options_list:
                race = option['value']
                stored_race_list.append(race)

            self.seasons[year] = stored_race_list
            print(year)

    def populate_all_seasons(self):
        print("Populating races:")
        for year in sorted(self.seasons):
            print(year)
            self.populate_season(year)

    def populate_season(self, year):
        if year in self.seasons.keys():
            self.raceDB.clear_races_from_year(year)
            raceNum = 1
            for race in self.seasons[year]:
                self.__populate_race(year, race, raceNum)
                raceNum += 1

    def __populate_race(self, year, race, race_num):
        # Grab the page for this race
        url = "http://www.formula1.com/content/fom-website/en/results.html/" + str(year) + "/races/" + race + "/race-result.html"
        req = Request(url, headers=self.header)
        page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")

        # Set up race database
        split = race.find("/")
        raceNumber = str(race_num).zfill(2)
        raceName = race[split + 1:].replace("-", "_")
        raceName = str(year) + "_" + raceNumber + "_" + raceName

        # Grab the info of the race
        race_table = soup.find("table", {"class": "resultsarchive-table"})

        # Put the race in the database if it exists
        if race_table is not None:
            table_rows = race_table.findAll("tr")
            self.raceDB.new_race(year, raceNumber, raceName)
        else:
            return

        for raw_row in table_rows:
            position = raw_row.find("td", {"class": "dark"})
            if position is None:
                continue

            row = raw_row.findAll("td")
            position = row[1].get_text()
            nameSpan = row[3].findAll("span")
            firstName = nameSpan[0].get_text()
            lastName = nameSpan[1].get_text()

            if position == "NC":
                continue
            if row[6].get_text() == "SHC":
                continue
            if row[6].get_text() == "DNF":
                continue

            # Add driver to database if needed and add to the current race
            entry = self.raceDB.get_driver_by_name(firstName, lastName)
            if entry is None:
                self.raceDB.new_driver(firstName, lastName)
                driverID = self.raceDB.get_driver_by_name(firstName, lastName)['driver_id']
            else:
                driverID = entry['driver_id']

            self.raceDB.populate_race_info(raceName, driverID)


