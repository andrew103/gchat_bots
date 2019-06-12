import ast
import requests

r6_siege_rank_map = {
    0: "unranked", 1: "copper IV", 2: "copper III", 3: "copper II",
    4: "copper I", 5: "bronze IV", 6: "bronze III", 7: "bronze II",
    8: "bronze I", 9: "silver IV", 10: "silver III", 11: "silver II",
    12: "silver I", 13: "gold IV", 14: "gold III", 15: "gold II",
    16: "gold I", 17: "platinum III", 18: "platinum II", 19: "platinum I",
    20: "diamond"
}

def get_stats(game_title, player_name, platform, games):
    game = ""
    arg = ""
    for key in list(games.keys()):
        if game_title in games[key]:
            game = key
            break
    
    if len(platform.split()) != 1:
        arg = platform.split()[1].lower()
        platform = platform.split()[0].lower()

    if game == "":
        return "Requested game not found. Use the 'games' command to list available games"
    elif game == "r6_siege":
        data = {}
        search_endpoint = "https://r6tab.com/api/search.php"
        player_endpoint = "https://r6tab.com/api/player.php"
        try:
            if platform == "pc":
                data = requests.get(search_endpoint+"?platform=uplay&search="+player_name).json()
            elif platform == "psn":
                data = requests.get(search_endpoint+"?platform=psn&search="+player_name).json()
            elif platform == "xbox":
                data = requests.get(search_endpoint+"?platform=xbl&search="+player_name).json()
            else:
                return "Invalid platform"
        except:
            return "API for Rainbow 6 Siege is not available currently"

        if "results" not in list(data.keys()):
            return "No results from search"
        else:
            data = data['results'][0]

        pid = data["p_id"]
        data = requests.get(player_endpoint+"?p_id="+pid).json()
        p_data = ast.literal_eval(data["p_data"])
        return r6_siege_response(data, p_data, arg)
    else:
        return "Unexpected error"

def r6_siege_response(data, p_data, arg):
    resp = "Player data for "+data["p_name"]+" in Rainbow 6: Siege"

    if arg == "":
        resp += "\nCurrent level: "+str(data["p_level"])
        resp += "\nCurrent rank: "+r6_siege_rank_map[int(data["p_currentrank"])]
        resp += "\nK/D ratio: "+str(float(data["kd"])/100.0)
        wl_ratio = round(float(p_data[8]+p_data[3])/float(p_data[9]+p_data[4]), 2)
        resp += "\nW/L ratio: "+str(wl_ratio)
        resp += "\nHours played: "+str(round(float(p_data[0]+p_data[5])/3600.0, 2))
    elif arg == "--detailed":
        resp += "\nCurrent level: "+str(data["p_level"])
        resp += "\nCurrent season rank: "+r6_siege_rank_map[int(data["p_currentrank"])]
        resp += " | Best season rank: "+r6_siege_rank_map[int(data["p_maxrank"])]
        resp += "\nCasual K/D: "+str(round(float(p_data[6])/float(p_data[7]), 2))
        resp += " | Ranked K/D: "+str(round(float(p_data[1])/float(p_data[2]), 2))
        resp += "\nCasual W/L: "+str(round(float(p_data[8])/float(p_data[9]), 2))
        resp += " | Ranked W/L: "+str(round(float(p_data[3])/float(p_data[4]), 2))
        resp += "\nBomb W/L: "+str(round(float(p_data[10])/float(p_data[11]), 2))
        resp += " | Secure W/L: "+str(round(float(p_data[12])/float(p_data[13]), 2))
        resp += " | Hostage W/L: "+str(round(float(p_data[14])/float(p_data[15]), 2))
        resp += "\nTotal headshots: "+str(p_data[17])
        resp += " | Total melees: "+str(p_data[18])
    elif arg == "--kd":
        resp += "\nCasual K/D ratio: "+str(round(float(p_data[6])/float(p_data[7]), 2))
        resp += "\nRanked K/D ratio: "+str(round(float(p_data[1])/float(p_data[2]), 2))
    elif arg == "--wl":
        resp += "\nCasual W/L ratio: "+str(round(float(p_data[8])/float(p_data[9]), 2))
        resp += "\nRanked W/L ratio: "+str(round(float(p_data[3])/float(p_data[4]), 2))
    elif arg == "--hours":
        resp += "\nCasual hours played: "+str(round(float(p_data[5])/3600.0, 2))
        resp += "\nRanked hours played: "+str(round(float(p_data[0])/3600.0, 2))
    elif arg == "--matches":
        resp += "\nCasual matches played: "+str(p_data[8]+p_data[9])
        resp += "\nRanked matches played: "+str(p_data[3]+p_data[4])
    elif arg == "--rank":
        resp += "\nCurrent rank: "+r6_siege_rank_map[int(data["p_currentrank"])]
        resp += "\nCurrent MMR: "+str(data["p_currentmmr"])
    elif arg == "--embarass":
        wl_ratio = round(float(p_data[8]+p_data[3])/float(p_data[9]+p_data[4]), 2)
        if 0 < int(data["p_currentrank"]) < 5:
            resp += "\nHey check it out, we got a copper over here"
        if float(data["kd"])/100.0 < 0.5:
            resp += "\nK/D ratio: "+str(float(data["kd"])/100.0)+" (could use a little work)"
        if wl_ratio < 0.5:
            resp += "\nW/L ratio: "+str(wl_ratio)+" (could use a little work)"
        
        resp += "\nYou've owned yourself (likely with a grenade) "+str(p_data[20])+" times! Congrats!"
    else:
        resp += "\nInvalid argument. Showing defaults"
        resp += "\nCurrent level: "+str(data["p_level"])
        resp += "\nCurrent rank: "+r6_siege_rank_map[int(data["p_currentrank"])]
        resp += "\nK/D ratio: "+str(float(data["kd"])/100.0)
        wl_ratio = round(float(p_data[8]+p_data[3])/float(p_data[9]+p_data[4]), 2)
        resp += "\nW/L ratio: "+str(wl_ratio)
        resp += "\nHours played: "+str(round(float(p_data[0]+p_data[5])/3600.0, 2))
    
    return resp
