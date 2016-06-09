import RaceDatabase
import CalculateRating

raceDB = RaceDatabase.RaceDatabase()
drivers = raceDB.get_all_drivers_sorted_by_rating()

pageTemplateFile = open('cojatronictemplate.html', 'r')
pageTemplate = pageTemplateFile.read()
tableFile = open('web\\drivertable.html', 'w', encoding='utf-8')
title = 'Table of All Drivers'
table = '<h1>' + title + '</h1>\n<table class="sortable">\n<thead>\n<tr>\n<th>First Name</th><th>Last Name</th><th>Rating</th>\n</tr>\n</thead>\n<tbody>'

for index in range(0, len(drivers)):
    table += '\n<tr>\n<td>' + drivers[index]['first_name'] + '</td>\n<td>' +  drivers[index]['last_name'] + '</td>\n<td>' + str(drivers[index]['rating']) + '</td>\n</tr>'

table += '\n</tbody>\n</table>'
pageTemplate = pageTemplate.replace('TITLETEXT', title)
pageTemplate = pageTemplate.replace('BODYTEXT', table)
tableFile.write(pageTemplate)

