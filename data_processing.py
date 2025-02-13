def extract_match_data(match_details, target_puuid):
    """
    Extrait les stats importantes d’un match pour un joueur spécifique.
    """
    if not match_details:
        return None

    info = match_details["info"]
    
    # Trouver le joueur concerné
    player_data = next((p for p in info["participants"] if p["puuid"] == target_puuid), None)
    
    if not player_data:
        return None

    # Calcul du CS/min
    game_duration_minutes = info["gameDuration"] / 60
    cs_per_min = round(player_data["totalMinionsKilled"] / game_duration_minutes, 2) if game_duration_minutes > 0 else 0

    # Vérifier si TP était pris (Summoner Spell 1 ou 2)
    has_tp = player_data["summoner1Id"] == 12 or player_data["summoner2Id"] == 12

    # Statistiques importantes
    match_data = {
        "gameMode": info["gameMode"],
        "championName": player_data["championName"],
        "KDA": round((player_data["kills"] + player_data["assists"]) / max(1, player_data["deaths"]), 2),
        "csPerMin": cs_per_min,
        "goldEarned": player_data["goldEarned"],
        "damageDealtToChampions": player_data["totalDamageDealtToChampions"],
        "visionScore": player_data["visionScore"],
        "firstTowerKill": player_data["firstTowerKill"],
        "firstBloodKill": player_data["firstBloodKill"],
        "hasTP": has_tp,
        "teleportCasts": player_data["summoner1Casts"] if has_tp else player_data["summoner2Casts"],
        "teamBaronKills": info.get("teams", [{}])[0].get("objectives", {}).get("baron", {}).get("kills", 0),
        "teamDragonKills": info.get("teams", [{}])[0].get("objectives", {}).get("dragon", {}).get("kills", 0),
        "win": player_data["win"]
    }

    return match_data
