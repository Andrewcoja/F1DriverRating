import RaceDatabase
import CalculateRating

raceDB = RaceDatabase.RaceDatabase()
calculate = CalculateRating.CalculateRating()
calculate.calculate_all()
drivers = raceDB.get_all_drivers_sorted_by_rating()

pageTemplateFile = open('cojatronictemplate.html', 'r')
pageTemplate = pageTemplateFile.read()
tableFile = open('web\\AllDrivers.html', 'w', encoding='utf-8')
title = 'All Time Top Formula 1 Drivers'
yearly = '<center>Top Drivers in <a href="1950">1950</a> | <a href="1960">1960</a> | <a href="1970">1970</a> | <a href="1980">1980</a> | <a href="1990">1990</a> | <a href="2000">2000</a> | <a href="2010">2010</a></center>'
table = '<h1>' + title + '</h1>\n<p>' + yearly + '\n\n<table class="sortable">\n<tr>\n<th>Ranking</th>\n<th>First Name</th>\n<th>Last Name</th>\n<th>Rating</th>\n</tr>\n'

for index in range(0, len(drivers)):
    if drivers[index]['rating'] == 0:
        continue
    table += '\n<tr>\n<td class="ranking">' + str(index + 1).zfill(3) + '</td>\n<td class="first">' + drivers[index][
        'first_name'] + '</td>\n<td class="last">' + drivers[index]['last_name'] + '</td>\n<td class="rating">' + str(
        drivers[index]['rating']) + '</td>\n</tr>'

table += '\n</table>\n\n' + yearly + '</p>'
table += '\n<h6><a href="http://cojatronic.com">Main Page</a></h6>'
pageTemplate = pageTemplate.replace('TITLETEXT', title)
pageTemplate = pageTemplate.replace('BODYTEXT', table)
tableFile.write(pageTemplate)

