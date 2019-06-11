from main import app
from _thread import start_new_thread
import time
import requests
import signal, sys

def signal_handler(sig, frame):
    print("\nExiting...")
    sys.exit(0)

def run_bot_server():
    app.run(host="127.0.0.1", port="8080", debug=False) # debug needs to be False for multi-threading

def test_bot():
    signal.signal(signal.SIGINT, signal_handler)
    data = {}

    # Test response to adding to group or DM
    data['type'] = 'ADDED_TO_SPACE'
    data['space'] = {}
    data['space']['type'] = 'ROOM'
    data['space']['displayName'] = "TEST_ROOM"
    bot_resp = requests.post("http://127.0.0.1:8080/", json=data)
    print(bot_resp.json()['text'])

    data['space']['type'] = 'DM'
    data['user'] = {}
    data['user']['displayName'] = "TEST_USER"
    bot_resp = requests.post("http://127.0.0.1:8080/", json=data)
    print(bot_resp.json()['text'])

    # Test response to messages
    data = {}
    data['type'] = 'MESSAGE'
    data['message'] = {}
    while True:
        message = input("\nMessage to bot (must include the @BotName): ")
        data['message']['text'] = message
        bot_resp = requests.post("http://127.0.0.1:8080/", json=data)
        try:
            print(bot_resp.json()['text'])
        except:
            print("An internal error caused the bot server to shutdown. Closing test script")
            sys.exit(0)

if __name__ == "__main__":
    start_new_thread(run_bot_server, ())
    time.sleep(1)
    print("\n\n\n\n")
    test_bot()