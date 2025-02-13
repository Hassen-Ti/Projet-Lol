import requests
import json
import time

# Charger la clé API depuis config.json
def load_api_key():
    with open("config.json", "r") as file:
        return json.load(file)["api_key"]

API_KEY = load_api_key()
BASE_URL = "https://europe.api.riotgames.com"
TIMEOUT = 5  # ⏳ Timeout en secondes

def request_api(url, max_retries=3):
    """
    Envoie une requête HTTP avec gestion des erreurs et timeout.
    """
    headers = {"X-Riot-Token": API_KEY}
    
    for _ in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print("🚨 Clé API expirée. Mets à jour `config.json`.")
                return None
            elif response.status_code == 429:
                print("🛑 Trop de requêtes. Pause 10 sec...")
                time.sleep(10)
            else:
                print(f"⚠️ Erreur API {response.status_code}. Retente...")
                time.sleep(2)
        
        except requests.Timeout:
            print(f"⏳ Timeout ({TIMEOUT}s). Nouvelle tentative...")
        except requests.RequestException as e:
            print(f"❌ Erreur réseau : {e}")
            return None

    print("❌ Échec après plusieurs tentatives.")
    return None

def get_puuid(game_name, tag_line):
    """Récupère le PUUID d'un joueur."""
    url = f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    return request_api(url).get("puuid")

def get_match_ids(puuid, count=5):
    """Récupère les derniers matchs d’un joueur."""
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    return request_api(url)

def get_match_details(match_id):
    """Récupère les détails d’un match."""
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    return request_api(url)
