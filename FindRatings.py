import RaceScrape
import CalculateRating

scrapething = RaceScrape.RaceScrape(2016)
scrapething.get_seasons_list(1)
scrapething.populate_all_seasons()

f1races = CalculateRating.CalculateRating()
f1races.full_calculation_from_latest()
