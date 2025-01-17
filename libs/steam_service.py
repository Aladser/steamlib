import sys
import requests
from steam_web_api import Steam

from config.settings import STEAM_API_KEY


class SteamService:
    @staticmethod
    def get_steam_userid(login, api_key):
        """Возвращает ID пользователя стим"""
        url = f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
        params = {
            'key': api_key,
            'vanityurl': login
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {'response':True, 'data':data.get('response', {}).get('steamid')}
        else:
            print(response.__dict__)
            print(f'Ошибка: {response.status_code}: {response.reason}', file=sys.stderr)
            return {'response':False, 'data':response._content}

    @staticmethod
    def get_game_info(appid):
        """Возвращает информацию об игре"""
        url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data[str(appid)]['success']:
                return {'data': data[str(appid)]['data'], 'is_full': True}
            else:
                details = SteamService.get_partial_game_info(appid)
                return {'data': details, 'is_full': False} if details else None
        else:
            details = SteamService.get_partial_game_info(appid)
            return {'data': details, 'is_full': False} if details else None

    @staticmethod
    def get_partial_game_info(appid):
        details = Steam(STEAM_API_KEY).apps.get_app_details(appid)
        return details[str(appid)]['data'] if details else None

    @staticmethod
    def get_steam_games_list(userid, apikey):
        """Возвращает список игр пользователя"""
        url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
        params = {
            'key': apikey,
            'steamid': userid,
            'include_appinfo': True,
            'include_played_free_games': True,
            'format': 'json'
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            games_data = response.json()
            owned_games = games_data.get('response', {}).get('games', [])
            games_list = []

            if owned_games:
                for game in owned_games:
                    # время
                    time = round(game['playtime_forever'] / 60, 1)
                    if int(time) == time:
                        time = int(time)

                    games_list.append({
                        'title': game['name'],
                        'appid': game['appid'],
                        'time': time,
                    })
                sorted_games_list = sorted(games_list, key=lambda x: x.get('time', 0), reverse=True)
                return sorted_games_list
            else:
                return None
        else:
            print(f"Ошибка: {response.status_code}", file=sys.stderr)
            return None

