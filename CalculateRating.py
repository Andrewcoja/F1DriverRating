import RaceDatabase


class CalculateRating(object):
    def __init__(self, initialize=False):
        self.raceDB = RaceDatabase.RaceDatabase()
        self.numRaces = self.raceDB.number_of_races()[0]

        if initialize:
            self.full_calculation()

    def reset_driver_ratings(self):
        driver_list = self.raceDB.get_all_drivers()
        for driver in driver_list:
            self.raceDB.update_driver_rating(driver['driver_id'], 1350)
    
    def full_calculation(self):
        self.full_calculation_from_race_id(1)

    def full_calculation_from_latest(self):
        latestRace = self.numRaces
        latestOverview = self.raceDB.get_overview(latestRace)
        latestCalculatedRace = latestRace
        if latestOverview['strength_of_field'] > 0:
            print("Already at latest race")
            return
        else:
            for raceID in range(latestRace, 1, -1):
                raceOverview = self.raceDB.get_overview(raceID)
                if raceOverview['strength_of_field'] > 0:
                    latestCalculatedRace = raceID + 1
                    break

        self.full_calculation_from_race_id(latestCalculatedRace)

    def full_calculation_from_race_id(self, race_id):
        if race_id > 1:
            self.calculate_up_to_race_id(race_id-1)
        else:
            self.reset_driver_ratings()
        for race in range(race_id, self.numRaces + 1):
            race_name = self.raceDB.get_race_name_by_id(race)
    
            # Add in the current ratings and adjustments
            # Each finishing position gets an adjustment. It starts at half the total number of race entries for first
            # place and then goes down by one for each position. This insures that drivers who finish higher still get
            # points even if they finish lower than their prediction
            race_info = self.raceDB.get_race_info_by_name(race_name)
            adjustment = int(len(race_info) / 2)
            for current_ratings_row in race_info:
                name_id = int(current_ratings_row['name_id'])
                rating = self.raceDB.get_driver_rating(name_id)
                if rating == 0:
                    rating = 1350
                driver_race_entry = self.raceDB.get_driver_from_race(race_name, name_id)
                driver_race_entry['old_rating'] = rating
                driver_race_entry['adjustment'] = adjustment
                self.raceDB.update_driver_in_race(driver_race_entry, race_name)
                adjustment -= 1
    
            # Update predictions
            # Drivers are sorted by their current rating and are given a predicted finishing position
            race_info = self.raceDB.get_race_info_by_name(race_name)
            if race == 1:  # The first race, so everyone is equal, no real way to calculate this
                prediction = 11
                for prediction_row in race_info:
                    name_id = int(prediction_row['name_id'])
                    driver_race_entry = self.raceDB.get_driver_from_race(race_name, name_id)
                    driver_race_entry['prediction'] = prediction
                    self.raceDB.update_driver_in_race(driver_race_entry, race_name)
            else:
                prediction = 1
                sorted_ratings = self.raceDB.get_race_info_sorted_by(race_name, 'old_rating', 'descending')
    
                for sorted_row in sorted_ratings:
                    name_id = sorted_row['name_id']
                    driver_race_entry = self.raceDB.get_driver_from_race(race_name, name_id)
                    driver_race_entry['prediction'] = prediction
                    self.raceDB.update_driver_in_race(driver_race_entry, race_name)
                    prediction += 1
    
            # Check positions gained
            # Positions gained is simply the prediction minus the finishing position plus any adjustment given for
            # finishing position. If a driver has less than 100 rating, he will not lose any more rating and won't be
            # counted in the final tally
            race_info = self.raceDB.get_race_info_by_name(race_name)
            total_gain = 0
            for gain_row in race_info:
                name_id = int(gain_row['name_id'])
                driver_race_entry = self.raceDB.get_driver_from_race(race_name, name_id)
                pos_gain = driver_race_entry['prediction'] - driver_race_entry['finish_id'] + driver_race_entry[
                    'adjustment']
                driver_race_entry['pos_gain'] = pos_gain
                if driver_race_entry['old_rating'] < 100 and driver_race_entry['adjustment'] < 1 and driver_race_entry[
                    'pos_gain'] < 1:
                    driver_race_entry['adjustment'] = 0
                    driver_race_entry['pos_gain'] = 0
                self.raceDB.update_driver_in_race(driver_race_entry, race_name)
    
                if pos_gain > 0:
                    total_gain += pos_gain
    
            # Calculate Strength of Field
            # This is just a made up calculation to create a pool of rating to give out or take away
            race_info = self.raceDB.get_race_info_by_name(race_name)
            rating_sum = 0
            for sof_row in race_info:
                if sof_row['pos_gain'] == 0 and sof_row['adjustment'] == 0:
                    continue
                old_rating = sof_row['old_rating']
                rating_sum += old_rating
            sof = int(rating_sum / len(race_info))
            rating_available = int(sof * .15)
    
            # Send SOF, Rating available and total gain to database
            self.raceDB.update_overview(race, sof, rating_available, total_gain)
    
            # Calculate share
            # There are two pools that share is calculated from. Drivers who are gaining rating share one pool and
            # drivers who are losing rating share from another pool. Each pool is equal as the rating is zero sum
            race_info = self.raceDB.get_race_info_by_name(race_name)
            for share_row in race_info:
                name_id = int(share_row['name_id'])
                driver_race_entry = self.raceDB.get_driver_from_race(race_name, name_id)
                driver_race_entry['share'] = driver_race_entry['pos_gain'] / total_gain
                driver_race_entry['gain'] = int(driver_race_entry['share'] * rating_available)
                driver_race_entry['new_rating'] = driver_race_entry['old_rating'] + driver_race_entry['gain']
                self.raceDB.update_driver_in_race(driver_race_entry, race_name)
                self.raceDB.update_driver_rating(name_id, driver_race_entry['new_rating'])
                driver = self.raceDB.get_driver_by_id(name_id)
                if driver['first_race'] == 0:
                    self.raceDB.update_driver_first_race(name_id, race)
                self.raceDB.update_driver_last_race(name_id, race)
    
            # Display calculation progress
            if race % 10 == 0:
                complete = int((race / self.numRaces) * 100)
                status = 'Progress: ' + str(race) + "/" + str(self.numRaces) + ' - ' + str(complete) + '%'
                print(status)

    def calculate_all(self):
        self.calculate_up_to_race_id(self.numRaces)

    def calculate_up_to_year(self, year):
        race_id = self.raceDB.get_race_id_by_year_and_number(year, 1) - 1
        self.calculate_up_to_race_id(race_id)

    def calculate_up_to_year_and_race(self, year, race_num):
        race_id = self.raceDB.get_race_id_by_year_and_number(year, race_num)
        self.calculate_up_to_race_id(race_id)

    def calculate_up_to_race_id(self, race_id):
        print("Doing fast calculation of early races")
        self.reset_driver_ratings()
        driver_list = self.raceDB.get_all_drivers()
        for driver in driver_list:
            driver_id = driver['driver_id']
            last_race = self.raceDB.get_driver_by_id(driver_id)['last_race']
            if last_race == 0:
                continue
            if last_race <= race_id:
                race_name = self.raceDB.get_race_name_by_id(last_race)
                final_rating = self.raceDB.get_driver_from_race(race_name, driver_id)['new_rating']
                self.raceDB.update_driver_rating(driver_id, final_rating)
            else:
                if driver['first_race'] > race_id:
                    self.raceDB.update_driver_rating(driver_id, 0)
                else:
                    recent_race = self.find_most_recent_race(driver_id, race_id)
                    if recent_race > 0:
                        race_name = self.raceDB.get_race_name_by_id(recent_race)
                        rating = self.raceDB.get_driver_from_race(race_name, driver_id)['new_rating']
                        self.raceDB.update_driver_rating(driver_id, rating)

    def find_most_recent_race(self, driver_id, race_id):
        for id in range(race_id, 1, -1):
            race_name = self.raceDB.get_race_name_by_id(id)
            if self.raceDB.get_driver_from_race(race_name, driver_id) is None:
                continue
            else:
                return id
        return 0

