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
import stats

app = Flask(__name__)

games = {
    "r6_siege": ["r6 siege", "rainbow 6 siege", "rainbow 6: siege", "r6: siege", "siege", "rainbow6: siege", "rainbow6 siege"]
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
--embarass - Only retrieve stats that could be embarassing
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
            elif " " in args[1].strip():
                text = "Invalid input. Username cannot contain spaces."
            else:
                text = stats.get_stats(args[0].strip().lower(), args[1].strip(), args[2].strip().lower(), games)

    return { 'text': text }

# [END gamer_stats]

@app.route('/', methods=['GET'])
def home_get():
    """Respond to GET requests to this endpoint.

    This function responds to requests with a simple HTML landing page for this
    App Engine instance.
    """

    return "Empty page"
