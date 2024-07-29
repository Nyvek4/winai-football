import requests

def get_match_statistics():
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'YOUR_API_KEY'
    
    # Replace 'YOUR_LEAGUE_ID' with the ID of the league you want to collect statistics for
    league_id = 'YOUR_LEAGUE_ID'
    
    # Replace 'YOUR_SEASON' with the season you want to collect statistics for
    season = 'YOUR_SEASON'
    
    # Replace 'YOUR_TEAM_ID' with the ID of the team you want to collect statistics for
    team_id = 'YOUR_TEAM_ID'
    
    # Make a request to the football API
    url = f'https://api.football-data.org/v2/competitions/{league_id}/matches?season={season}&team={team_id}'
    headers = {'X-Auth-Token': api_key}
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Extract the match statistics
        statistics = []
        for match in data['matches']:
            match_statistics = {
                'home_team': match['homeTeam']['name'],
                'away_team': match['awayTeam']['name'],
                'date': match['utcDate'],
                'status': match['status'],
                'score': match['score']['fullTime']
            }
            statistics.append(match_statistics)
        
        return statistics
    else:
        print('Failed to retrieve match statistics.')
        return None

# Call the function to get the match statistics
match_statistics = get_match_statistics()

# Print the match statistics
if match_statistics:
    for match in match_statistics:
        print(f"Home Team: {match['home_team']}")
        print(f"Away Team: {match['away_team']}")
        print(f"Date: {match['date']}")
        print(f"Status: {match['status']}")
        print(f"Score: {match['score']}")
        print()