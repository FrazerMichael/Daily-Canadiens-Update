import requests, json
from datetime import date, timedelta

currentDate = date.today()
oneMonthLater = currentDate + timedelta(days=20)
x = 0

url = "https://statsapi.web.nhl.com/api/v1/schedule?teamId=8&startDate=" + str(currentDate) + "&endDate=" + str(oneMonthLater)

response = requests.get(url)
responseDate = response.json()['dates'][x]['date']

try:
    homeTeam = response.json()['dates'][x]['games'][0]['teams']['home']['team']['name']
    awayTeam = response.json()['dates'][x]['games'][0]['teams']['away']['team']['name']
    arenaName = response.json()['dates'][x]['games'][0]['venue']['name']

except:
    print('There was an error!')


notMontrealCanadiens = ''
if homeTeam == 'Montréal Canadiens':
    notMontrealCanadiens = awayTeam
else:
    notMontrealCanadiens = homeTeam

if responseDate == str(currentDate):
    print('The next Montreal Canadiens game is Tonight!')
    print('They are playing the ' + notMontrealCanadiens + ' at their home, the' + arenaName + '.')

else:
    print('The next Montreal Canadiens\' game is on ' + responseDate)
    print('They will be playing the ' + notMontrealCanadiens + ' at the ' + arenaName + '.')


input("Press enter to exit;")