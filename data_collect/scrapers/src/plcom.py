import requests
import pandas as pd
import os
import datetime
from dateutil.parser import parse

api_key_football = '4dcbce1133594082808db951ee4d2068'
api_key_weather = 'eeddcecfae4a9faeb7596367dec83f73'

base_url_football = 'https://api.football-data.org/v2/competitions/PL/matches?season=2022'
base_url_weather = 'https://api.openweathermap.org/data/2.5/weather'

headers_football = {
    'X-Auth-Token': api_key_football
}

response_football = requests.get(base_url_football, headers=headers_football)

if response_football.status_code == 200:
    matches = response_football.json()['matches']
    data = []

    for match in matches:
        date_match = match['utcDate']
        venue = match['venue'] if 'venue' in match else 'N/A'
        match_date = parse(date_match)
        
        # API météo
        weather = 'Météo non disponible'
        if venue != 'N/A':
            response_weather = requests.get(base_url_weather, params={
                'q': venue,
                'appid': api_key_weather,
                'units': 'metric'
            })
            
            if response_weather.status_code == 200:
                weather_data = response_weather.json()
                weather = f"{weather_data['weather'][0]['description']}, Temp: {weather_data['main']['temp']}°C"

        match_id = match['id']
        match_details_url = f'https://api.football-data.org/v2/matches/{match_id}'
        match_details_response = requests.get(match_details_url, headers=headers_football)
        
        if match_details_response.status_code == 200:
            match_stats = match_details_response.json()['match']
            home_team = match_stats['homeTeam']['name']
            away_team = match_stats['awayTeam']['name']
            referees = ', '.join([ref['name'] for ref in match_stats['referees']]) if match_stats['referees'] else 'N/A'
            
            home_stats = match_stats['homeTeam']
            away_stats = match_stats['awayTeam']
            
            match_data = {
                'Date': date_match,
                'Matchday': match['matchday'],
                'Status': match['status'],
                'Venue': venue,
                'Home Team': home_team,
                'Away Team': away_team,
                'Home Team Score': match['score']['fullTime']['homeTeam'],
                'Away Team Score': match['score']['fullTime']['awayTeam'],
                'Referees': referees,
                'Weather': weather,
                'Shots on Target (Home)': home_stats.get('statistics', {}).get('shotsOnTarget', 'N/A'),
                'Shots on Target (Away)': away_stats.get('statistics', {}).get('shotsOnTarget', 'N/A'),
                'Possession (Home)': home_stats.get('statistics', {}).get('possession', 'N/A'),
                'Possession (Away)': away_stats.get('statistics', {}).get('possession', 'N/A'),
                'Corners (Home)': home_stats.get('statistics', {}).get('corners', 'N/A'),
                'Corners (Away)': away_stats.get('statistics', {}).get('corners', 'N/A'),
                'Fouls (Home)': home_stats.get('statistics', {}).get('fouls', 'N/A'),
                'Fouls (Away)': away_stats.get('statistics', {}).get('fouls', 'N/A')
            }
            data.append(match_data)

    df = pd.DataFrame(data)

    output_dir = os.path.join('data_collect', 'scrapers', 'output')
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'premier_league_2022_2023_results.csv')
    df.to_csv(output_file, index=False)

    print(f"Données des matchs sauvegardées dans {output_file}")
else:
    print(f"Échec de la récupération des données: {response_football.status_code}")
    print(response_football.json())