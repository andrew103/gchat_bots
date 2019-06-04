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

app = Flask(__name__)

commands_text = """Usage: @GamerStats <game title>/<player name>
Available commands are:
help - Display this prompt

Available optional arguments are:
--detailed - Give a more detailed summary of a player's stats
--kd - Only retrieve the player's K/D ratio to display
--wl - Only retrieve the player's W/L ratio to display
--hours - Only retrieve the number of hours the player has played
--matches - Only retrieve the number of matches the player has played
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
        text = "Hello from gamer_stats!"

    return { 'text': text }

# [END gamer_stats]

@app.route('/', methods=['GET'])
def home_get():
    """Respond to GET requests to this endpoint.

    This function responds to requests with a simple HTML landing page for this
    App Engine instance.
    """

    return "Empty page"
