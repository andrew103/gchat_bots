# =============================================================================
# Author(s):
# - Andrew Euredjian
# 
# Description:
# A bot that retrieves the statistics for a player in a specified game when
# given a username
# 
# =============================================================================
# [START gamer_stats]
import logging
from flask import Flask, request, json, make_response
import requests

app = Flask(__name__)

games = {
    "r6_siege": ["r6 siege", "rainbow 6 siege", "rainbow 6: siege", "r6: siege", "siege", "rainbow6: siege", "rainbow6 siege"]
}

r6_siege_rank_map = {
    0: "unranked", 1: "copper IV", 2: "copper III", 3: "copper II",
    4: "copper I", 5: "bronze IV", 6: "bronze III", 7: "bronze II",
    8: "bronze I", 9: "silver IV", 10: "silver III", 11: "silver II",
    12: "silver I", 13: "gold IV", 14: "gold III", 15: "gold II",
    16: "gold I", 17: "platinum III", 18: "platinum II", 19: "platinum I",
    20: "diamond"
}

commands_text = """Usage: @GamerStats <game title>/<player name>/<platform> <optional arg>

Available commands are:
help - Display this prompt
games - List currently supported games for retrieving player stats 

Available platforms to search under:
pc
psn
xbox

Available optional arguments are:
--detailed - Give a more detailed summary of a player's stats
--kd - Only retrieve the player's K/D ratio
--wl - Only retrieve the player's W/L ratio
--hours - Only retrieve the number of hours the player has played
--matches - Only retrieve the number of matches the player has played
--rank - Only retrieve the player's current rank and MMR
"""

@app.route('/', methods=['POST'])
def home_post():
    """Respond to POST requests to this endpoint.

    All requests sent to this endpoint from Hangouts Chat are POST
    requests.
    """

    data = request.get_json()

    resp = None

    if data['type'] == 'REMOVED_FROM_SPACE':
        logging.info('Bot removed from a space')

    else:
        resp_dict = format_response(data)
        resp = json.jsonify(resp_dict)

    return resp

def format_response(event):
    """Determine what response to provide based upon event data.

    Args:
      event: A dictionary with the event data.

    """

    text = ""

    # Case 1: The bot was added to a room
    if event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
        text = 'Thanks for adding me to "%s"!\n' % event['space']['displayName'] + commands_text

    # Case 2: The bot was added to a DM
    elif event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'DM':
        text = 'Thanks for adding me to a DM, %s!\n' % event['user']['displayName'] + commands_text

    elif event['type'] == 'MESSAGE':
        usr_input = event['message']['text'].split("@GamerStats")[1].strip()

        if len(usr_input) == 0 or usr_input.lower() == "help":
            text = commands_text
        elif usr_input.lower() == "games":
            text = "Available games to pull stats from:\n"+"\n".join(list(games.keys()))
        else:
            args = usr_input.split("/")
            if len(args) != 3:
                text = "Invalid input.\n"+commands_text
            else:
                text = get_stats(args[0].strip().lower(), args[1].strip(), args[2].strip().lower())

    return { 'text': text }

def get_stats(game_title, player_name, platform):
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
        resp = "Player data for "+player_name+" in Rainbow 6: Siege"

        if arg == "":
            pass
        elif arg == "--detailed":
            pass
        elif arg == "--kd":
            resp += "\nK/D ratio: "+str(float(data["kd"])/100.0)
        elif arg == "--wl":
            pass
        elif arg == "--hours":
            pass
        elif arg == "--matches":
            pass
        elif arg == "--rank":
            resp += "\nCurrent rank: "+r6_siege_rank_map[int(data["p_currentrank"])]
            resp += "\nCurrent MMR: "+str(data["p_currentmmr"])
        else:
            resp += "\nInvalid argument. Showing defaults"

        return resp
    else:
        return "Unexpected error"

# [END gamer_stats]

@app.route('/', methods=['GET'])
def home_get():
    """Respond to GET requests to this endpoint.

    This function responds to requests with a simple HTML landing page for this
    App Engine instance.
    """

    return "Empty page"
