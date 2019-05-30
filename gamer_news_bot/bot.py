import logging
from flask import Flask, render_template, request, json, make_response
from GoogleNews import GoogleNews as gnews

app = Flask(__name__)
googlenews = gnews()

news_topics = ['rainbow 6: siege', 'rocket league', 'the division 2', 'minecraft', 'destiny 2', 'pubg']

commands_text = """
Usage: @GamerNews <command> <topic>\n
Available commands are:\n
help/commands - Display this prompt
add - Add a topic to be searchable
topics - List the topics that are searchable
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
        text = 'Thanks for adding me to "%s"!\n' + commands_text % event['space']['displayName']

    # Case 2: The bot was added to a DM
    elif event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'DM':
        text = 'Thanks for adding me to a DM, %s!' + commands_text % event['user']['displayName']

    elif event['type'] == 'MESSAGE':
        usr_input = event['message']['text'].split("@GamerNews ")[1].lower().split() # CHANGE THIS

        if len(usr_input) == 0 or usr_input[0] == "help" or usr_input[0] == "commands":
            text = commands_text
        elif usr_input[0] == "add":
            topic = " ".join(usr_input[1:])
            news_topics.append(topic)
            text = "Topic %s added to list of searchable topics" % topic
        elif usr_input[0] == "topics":
            text = news_topics.join(", ")
        else:
            topic = " ".join(usr_input)
            if topic in news_topics:
                googlenews.search(topic)
                if len(googlenews.gettext()) > 5:
                    titles = googlenews.gettext()[:5]
                    links = googlenews.getlinks()[:5]
                else:
                    titles = googlenews.gettext()
                    links = googlenews.getlinks()

                text = "\n".join([str(title[i])+" - "+str(link[i]) for i in range(len(titles))])
            else:
                text = "Requested topic has not been added\n" + commands_text

        # text = 'Your message: "%s"' % event['message']['text']

    return { 'text': text }

@app.route('/', methods=['GET'])
def home_get():
    """Respond to GET requests to this endpoint.

    This function responds to requests with a simple HTML landing page for this
    App Engine instance.
    """

    return "Empty page"

