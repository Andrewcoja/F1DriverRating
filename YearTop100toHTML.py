import RaceDatabase
import CalculateRating

startYear = 1960

raceDB = RaceDatabase.RaceDatabase()
calculation = CalculateRating.CalculateRating()

for year in range(1950, 2000, 10):
    print(year)
    calculation.calculate_up_to_year(year+1)
    drivers = raceDB.get_all_drivers_sorted_by_rating()

    pageTemplateFile = open('cojatronictemplate.html', 'r')
    pageTemplate = pageTemplateFile.read()
    tableFile = open('web\\' + str(year) + '.html', 'w', encoding='utf-8')
    title = 'Top 100 Drivers in ' + str(year)
    table = '<h1>' + title + '</h1>\n<p><table class="sortable">\n<thead>\n<tr>\n<th>First Name</th><th>Last Name</th><th>Rating</th>\n</tr>\n</thead>\n<tbody>'

    for index in range(0, 100):
        if drivers[index]['rating'] == 0:
            continue
        table += '\n<tr>\n<td>' + drivers[index]['first_name'] + '</td>\n<td>' +  drivers[index]['last_name'] + '</td>\n<td>' + str(drivers[index]['rating']) + '</td>\n</tr>'

    table += '\n</tbody>\n</table></p>'
    table += '\n<h6><a href="http://cojatronic.com">Main Page</a></h6>'
    pageTemplate = pageTemplate.replace('TITLETEXT', title)
    pageTemplate = pageTemplate.replace('BODYTEXT', table)
    tableFile.write(pageTemplate)

