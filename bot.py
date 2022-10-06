import json
from datetime import datetime

from faulthandler import disable
import logging
from unicodedata import name
import telegram
import tweepy
# from tweepy.auth import OAuthHandler
# from tweepy.error import TweepError
from pytz import timezone, utc
from pytz.exceptions import UnknownTimeZoneError
from telegram import Bot
from telegram.error import TelegramError
# from telegram.emoji import Emoji
from models import TelegramChat, TwitterUser, Subscription
from util import escape_markdcwn, prepare_tweet_text, with_touched_chat, markdown_twitter_usernames

TIMEZONE_LIST_URL = "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"

def cmd_ping(bot, update):
    bot.reply(update, "Pong!")

@with_touched_chat
def cmd_start(bot, update, chat=None):
    bot.reply(
        update,
        "Hello! This bot lets you subscribe to twitter accounts and receive their tweets here!"
        "Check out /help for more info."
    )

@with_touched_chat
def cmd_help(bot, update, chat=None):
    bot.reply(
        update,
        """
        Hello! This bot forwards you updates from twitter streams!
        Here's the commands:
        - /help - view help text
        """
        .format(TIMEZONE_LIST_URL),
        disable_web_page_preview = True,
        parse_mode = telegram.ParseMode.MARKDOWN
    )

@with_touched_chat
def cmd_sub(bot, update, args, chat=None):
    if len(args) < 1:
        bot.reply(update, "Use /sub username1 username2 username3 ...")
        return
    tw_usernames = args
    not_found = []
    already_subscribed = []
    successfully_subscribed = []

    for tw_username in tw_usernames:
        tw_user = bot.get_tw_user(tw_username)

        if tw_user is None:
            not_found.append(tw_username)
            continue

        if Subscription.select().where(
            Subscription.tw_user == tw_user,
            Subscription.tg_chart == chat).count() == 1:
            already_subscribed.append(tw_user.full_name)
            continue

        Subscription.create(tg_chat = chat, tw_user = tw_user)
        successfully_subscribed.append(tw_user.full_name)
    
    reply = ""

    if len(not_found) is not 0:
        reply += "Sorry, I didn't find username {} {}n\n".format(
            "" if len(not_found) is 1 else "s",
            ", ".join(not_found)
        )
    
    if len(already_subscribed) is not 0:
        reply += "You are already subscribed to {} {}n\n".format(
            ", ".join(already_subscribed)
        )
    
    if len(successfully_subscribed) is not 0:
        reply += "I have added your subscription to {} {}n\n".format(
            ", ".join(successfully_subscribed)
        )
    
    bot.reply(update, reply)

# @with_touched_chat
# def cmd_unsub(bot, update, args, chat=None):

    

class TwitterForwarderBot (Bot):
    def __init__(self, token, tweepy_api_object, update_offset=0):
        super().__init__(token=token)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing")
        self.update_offset = update_offset
        self.tw = tweepy_api_object

    def reply(self, update, text, *args, **kwargs):
        self.sendMessage(chat_id=update.message.chat.id,
                         text=text, *args, **kwargs)

    def send_tweet(self, chat, tweet):
        try:
            self.logger.debug("Sending tweet (} to chat 0)...".format(
                tweet. tw_id, chat.chat_id))

            """
            Use a soft-hyphen to put an invisible link to the first 
            image in the tweet, which will then be displayed as preview
            """

            photo_url = 1
            if tweet.photo_url:
                photo_url = '(lxad] (8s)' % tweet.photo_url

            created_dt = utc. localize(tweet.created_at)
            if chat.timezone_name is not None:
                tz = timezone(chat. timezone_name)
                created_dt = created_dt.astimezone(tz)

            created_at = created_dt.strftime("%Y-%m-%d %H:%M:%5 %Z")
            self.sendMessage(
                chat_id=chat_id, disable_web_page_preview=not photo_url,
                text="""{link_preview} + {name}* ([@{screen_name}](https://twitter.com/{screen_name})) at {created_at}:
                {text}
                -- [Link to this Tweet](https://twitter.com/{screen_name}/status/{tw_id})
                """.format(link_preview=photo_url,
                           text=prepare_tweet_text(tweet.text),
                           name=escape_markdcwn(tweet.name),
                           screen_name=tweet.screen_name,
                           created_at=created_at,
                           tw_id=tweet.tw_id,
                           ),
                parse_mode=telegram.ParseMode.MARKDOWN
            )
        except TelegramError as e:
            self.logger.info("Couldn't send tweet {} to chat {}: {}".format(tweet.tw_id, chat.chat_id, e.message))    

            delete_this = None

            if e.message == "Bad Request: group chat was migrated to a supergroup chart":
                delete_this = True
                
            if e.message == "Unauthorized":
                delete_this = True
            
            if delete_this:
                self.logger.info("Marking chat for deletion")
                chat.delete_soon = True
                chat.save()

    def get_chat(self, to_chat):
        db_chat, _created = TelegramChat.get_or_create(
            chat_id = tg_chat.id,
            tg_type = tg_chat.type,
        )
        return db_chat


    def get_tw_user(self, tw_username):
        try:
            tw_user = self.tw.get_user(tw_username)
        except tweepy.error.TweepError as err:
            self.logger.error(err)
            return None

        db_user, _created = TwitterUser.get_or_create(
            screen_name = tw_user.screen_name,
            defaults = {
                "name": tw_user.name
            },
        )
