# =============================================================================
# Author(s):
# - Andrew Euredjian
# 
# Description:
# A bot that gets the latest news articles about a given topic
# 
# =============================================================================
# [START news_bot]
import logging
from flask import Flask, render_template, request, json, make_response
from GoogleNews import GoogleNews as gnews

app = Flask(__name__)
googlenews = gnews()

commands_text = """Usage: @NewsBot <topic>
Available commands are:
help - Display this prompt
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
        usr_input = event['message']['text'].split("@NewsBot")[1].lower().strip()
        logging.info(usr_input)

        if len(usr_input) == 0 or usr_input == "help":
            text = commands_text
        else:
            # Make the search input one word since the GoogleNews library doesn't work with multiple word inputs
            search_input = usr_input.replace(" ", "-")
            googlenews.clear()
            googlenews.search(search_input)
            if len(googlenews.gettext()) > 5:
                titles = googlenews.gettext()[:5]
                links = googlenews.getlinks()[:5]
            else:
                titles = googlenews.gettext()
                links = googlenews.getlinks()

            text = "News on %s:\n" % usr_input + "\n".join([str(titles[i])+" - "+str(links[i]) for i in range(len(titles))])

    return { 'text': text }

# [END news_bot]

@app.route('/', methods=['GET'])
def home_get():
    """Respond to GET requests to this endpoint.

    This function responds to requests with a simple HTML landing page for this
    App Engine instance.
    """

    return "Empty page"

