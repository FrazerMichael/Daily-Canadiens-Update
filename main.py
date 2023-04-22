import requests, json
from datetime import date, timedelta

currentDate = date.today()
oneMonthLater = currentDate + timedelta(days=20)
yesterday = currentDate - timedelta(days=1)

#These are the the Links and get requests
nextGameURL = "https://statsapi.web.nhl.com/api/v1/schedule?teamId=8&startDate=" + str(currentDate) + "&endDate=" + str(oneMonthLater)
yesterdayURL = "https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.linescore&teamId=8&startDate=" + str(yesterday) + "&endDate=" + str(yesterday)

nextGameResponse = requests.get(nextGameURL)
responseDate = nextGameResponse.json()['dates'][0]['date']
yesterdayResponse = requests.get(yesterdayURL)
link = yesterdayResponse.json()['dates'][0]['games'][0]['link']
gameURL = "https://statsapi.web.nhl.com" + link

gameResponse = requests.get(gameURL)

print(yesterdayResponse.json()['dates'][0]['games'][0]['teams']['away']['score'])
print(yesterdayResponse.json()['dates'][0]['games'][0]['teams']['home']['score'])

awayPlayers = gameResponse.json()['liveData']['boxscore']['teams']['away']['players']
homePlayers = gameResponse.json()['liveData']['boxscore']['teams']['home']['players']

def jsonToList(dic):
    temp = []
    for each in dic:
        temp.append(each)
    return temp

awayList = jsonToList(awayPlayers)
homeList = jsonToList(homePlayers)

def goalScorer(playerList, teamList):
    temp = []
    for i in range(len(playerList)):
        player = []
        if 'skaterStats' in playerList[teamList[i]]['stats']:
            if (playerList[teamList[i]]['stats']['skaterStats']['goals']) > 0:
                player.append(('#' + playerList[teamList[i]]['jerseyNumber']))
                player.append(playerList[teamList[i]]['person']['fullName'])
                player.append(playerList[teamList[i]]['stats']['skaterStats']['goals'])

        if len(player) > 0:
            temp.append(player)
    return temp

awayGoalScorers = goalScorer(awayPlayers, awayList)
homeGoalScorers = goalScorer(homePlayers, homeList)

print(awayGoalScorers)
print(homeGoalScorers)

#These dive into the json structure to pull out the basic data for returning the next game
homeTeam = nextGameResponse.json()['dates'][0]['games'][0]['teams']['home']['team']['name']
awayTeam = nextGameResponse.json()['dates'][0]['games'][0]['teams']['away']['team']['name']
arenaName = nextGameResponse.json()['dates'][0]['games'][0]['venue']['name']

#Checks to see if Montreal is the home or away team in the next game
notMontrealCanadiens = ''
if homeTeam == 'Montréal Canadiens':
    notMontrealCanadiens = awayTeam
else:
    notMontrealCanadiens = homeTeam

if responseDate == str(currentDate):
    print('The next Montreal Canadiens game is Tonight!')
    print('They are playing the ' + notMontrealCanadiens + ' at the ' + arenaName + '.')

else:
    print('The next Montreal Canadiens\' game is on ' + responseDate)
    print('They will be playing the ' + notMontrealCanadiens + ' at the ' + arenaName + '.')


input("Press enter to exit;")