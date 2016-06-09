import RaceDatabase
import CalculateRating

startYear = 1950
currentYear = 2016

raceDB = RaceDatabase.RaceDatabase()
calculation = CalculateRating.CalculateRating()

for year in range(startYear, currentYear+1, 1):
    print(year)

    if year == currentYear:
        calculation.calculate_all()
    else:
        calculation.calculate_up_to_year(year + 1)
    drivers = raceDB.get_all_drivers_sorted_by_rating()

    navigation = '<center>'
    if year > 1960:
        navigation += '<a href="' + str(year - 10) + '">Previous Decade</a> | '
    if year > 1950:
        navigation += '<a href="' + str(year - 1) + '">Previous Year</a>'
    if 1950 < year < currentYear:
        navigation += ' | '
    if year < currentYear:
        navigation += '<a href="' + str(year + 1) + '">Next Year</a>'
    if year < currentYear - 10:
        navigation += ' | <a href="' + str(year + 10) + '">Next Decade</a>'
    navigation += '</center>'
    pageTemplateFile = open('cojatronictemplate.html', 'r')
    pageTemplate = pageTemplateFile.read()
    pageTemplateFile.close()
    tableFile = open('web\\' + str(year) + '.html', 'w', encoding='utf-8')
    title = 'All Time Top 100 Formula 1 Drivers in ' + str(year)
    table = '<h1>' + title + '</h1>\n<p>' + navigation + '<table class="sortable">\n\n<tr>\n<th>Ranking</th>\n<th>First Name</th><th>Last Name</th><th>Rating</th>\n</tr>\n\n'

    for index in range(0, 100):
        if drivers[index]['rating'] == 0:
            continue
        table += '\n<tr>\n<td class="ranking">' + str(index+1).zfill(3) + '</td>\n<td class="first">' + drivers[index]['first_name'] + '</td>\n<td class="last">' +  drivers[index]['last_name'] + '</td>\n<td class="rating">' + str(drivers[index]['rating']) + '</td>\n</tr>'

    table += '\n\n</table>' + navigation + '</p>'
    table += '\n<h6><a href="http://cojatronic.com">Main Page</a> | <a href="AllDrivers">All Time Top Drivers</a></h6>'
    pageTemplate = pageTemplate.replace('TITLETEXT', title)
    pageTemplate = pageTemplate.replace('BODYTEXT', table)
    tableFile.write(pageTemplate)
    tableFile.close()

