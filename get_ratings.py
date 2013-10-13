from BeautifulSoup import BeautifulSoup
import requests


LEAGUE_ID = '140220'
FLEAFLICKER_URL = 'http://www.fleaflicker.com'
BASE_URL = FLEAFLICKER_URL + '/nfl/league-schedule?leagueId={0}&week='
LEAGUE_URL = BASE_URL.format(LEAGUE_ID)


def get_team_and_rating(row):
    team_name = row.find('div', 'league-name').find('a').text
    rating = row.find('div', 'bar')
    if rating:
        return team_name, int(rating.text.replace('%', ''))


def get_ratings_for_matchup(href):
    response = requests.get(FLEAFLICKER_URL + href)
    soup = BeautifulSoup(response.content)
    home = soup.find('tr', id='row_0_0_0')
    away = soup.find('tr', id='row_0_0_1')
    return [get_team_and_rating(row) for row in [home, away]]


def get_ratings_for_week(week):
    ratings = []
    response = requests.get(LEAGUE_URL + str(week))
    soup = BeautifulSoup(response.content)
    for link in soup.findAll('a', href=True, text='Box'):
        ratings += get_ratings_for_matchup(link.parent['href'])
    return ratings


def find_team_ratings():
    all_ratings = {}
    for i in xrange(1, 7):
        print i
        ratings = get_ratings_for_week(i)
        for team_rating in ratings:
            team_name, rating = team_rating
            if team_name in all_ratings:
                all_ratings[team_name].append(rating)
            else:
                all_ratings[team_name] = [rating]
    return all_ratings


if __name__ == '__main__':
    ratings = find_team_ratings()
    sorted_ratings = sorted(
        ratings.iteritems(),
        key=lambda x: sum(x[1]),
        reverse=True,
    )
    for team, ratings in sorted_ratings:
        print team, sum(ratings) / float(len(ratings))
