import RaceScrape
import CalculateRating

scrapething = RaceScrape.RaceScrape(1950, True)
scrapething.get_seasons_list()
scrapething.populate_all_seasons()
scrapething.scrape_finished()

f1races = CalculateRating.CalculateRating()
f1races.full_calculation_from_latest()
f1races.calculation_finished()
