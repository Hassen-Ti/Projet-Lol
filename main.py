from riot_api import get_puuid, get_match_ids, get_match_details
from data_processing import extract_match_data

GAME_NAME = "Vhorg"
TAG_LINE = "EUW"

def main():
    """
    Teste les requêtes API et affiche les performances du joueur.
    """
    print(f"🔎 Recherche du PUUID pour {GAME_NAME}#{TAG_LINE}...")
    puuid = get_puuid(GAME_NAME, TAG_LINE)
    
    if not puuid:
        print("❌ Impossible de récupérer le PUUID.")
        return
    
    print("✅ PUUID récupéré :", puuid)

    print("📥 Récupération des derniers matchs...")
    match_ids = get_match_ids(puuid, count=5)
    
    if not match_ids:
        print("❌ Impossible de récupérer les matchs.")
        return
    
    print("✅ Matchs trouvés :", match_ids)

    for match_id in match_ids:
        print(f"📊 Analyse du match {match_id}...")
        match_details = get_match_details(match_id)
        
        if match_details:
            match_data = extract_match_data(match_details, puuid)
            print(f"✅ Stats du match {match_id} :", match_data)
        else:
            print(f"❌ Impossible de récupérer les détails pour le match {match_id}.")

if __name__ == "__main__":
    main()
