Contributing / Creating your own bot
===============================================================================

If you'd like to create your own bot, follow the steps below to get started.

1. `git clone` this repo to your local machine
2. Navigate to the directory of the download and run `python3 create_bot.py <bot name>` to auto-generate a new bot
3. Get started writing your bot in the `main.py` file! You shouldn't need to change any of the other files unless your bot requires a specific configuration for Google Cloud
4. Test your bot locally by running `python test_bot.py` in your bot directory
5. Deploy your bot by following these steps/guides:
    1. Create a Google Cloud account and create a new project in the App Engine Console
    2. Install the [Google App Engine SDK](https://cloud.google.com/appengine/)
    3. [Deploy your bot to the engine](https://github.com/gsuitedevs/hangouts-chat-samples/tree/master/python/basic-bot#deploy-the-sample)
    4. [Publish your bot](https://developers.google.com/hangouts/chat/how-tos/bots-publish) to use in Google Hangouts Chat

**Note: If you'd like to have your bot added to this repo, fork the repo and create a pull request**

Bot tracking
===============================================================================

Finished bots:
* NewsBot - get latest news about a topic

Bots being worked on:
* GamerStats - get a player's statistics for certain games

Bots to be worked on:
* LiveScores - get the current score of a live match or the last match played in a sport (soccer, basketball, cricket, etc.)

Ideas for bots:
* 