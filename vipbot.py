#!/usr/bin/env python

import sys
import logging
import argparse

import yaml
import netifaces

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
import telegram.error


DEFAULT_CONFIG_PATH = "/etc/vipbot.yaml"


class VIPBot:

    ACCESS_DENIED_MESSAGE = "Sorry, you are not allowed to use this bot."
    HELLO_MESSAGE = "Hey, glad to see you! To request server IP, please press the button below."
    IP_MESSAGE = "Current server IP: {ip}"

    def __init__(self, token, interface, user_ids):
        self.token = token
        self.interface = interface
        self.user_ids = set(user_ids)

        self._updater = Updater(token)
        self._updater.dispatcher.add_handler(CommandHandler("start", self._onStart))
        self._updater.dispatcher.add_handler(CallbackQueryHandler(self._onGetIp))
        self._updater.dispatcher.add_error_handler(self._onError)

        button = InlineKeyboardButton("Get IP", callback_data="0")
        self._keyboard = InlineKeyboardMarkup([[button]])

    def _onStart(self, bot, update):
        if update.message.from_user.id not in self.user_ids:
            return update.message.reply_text(self.ACCESS_DENIED_MESSAGE)
        update.message.reply_text(self.HELLO_MESSAGE, reply_markup=self._keyboard)


    def _onGetIp(self, bot, update):
        if update.callback_query.from_user.id not in self.user_ids:
            return update.message.reply_text(self.ACCESS_DENIED_MESSAGE)
        bot.editMessageText(text=update.callback_query.message.text,
                            chat_id=update.callback_query.message.chat_id,
                            message_id=update.callback_query.message.message_id)
        update.callback_query.message.reply_text(self._makeIpReply(), reply_markup=self._keyboard)

    def _onError(self, bot, update, error):
        logging.warning("Update '{}' caused error '{}'".format(update, error))

    def _makeIpReply(self):
        try:
            addresses = netifaces.ifaddresses(self.interface)
        except ValueError:
            return "Interface not found: {}".format(self.interface)
        if netifaces.AF_INET not in addresses or not addresses[netifaces.AF_INET]\
        or "addr" not in addresses[netifaces.AF_INET][0]:
            return "Interface does not have associated IPv4 address: {}".format(self.interface)
        return self.IP_MESSAGE.format(ip=addresses[netifaces.AF_INET][0]["addr"])

    def run(self):
        self._updater.start_polling()
        self._updater.idle()


def main():

    # Define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", nargs="?", default=DEFAULT_CONFIG_PATH,
        help="path to the config file of the bot")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    # Try to open and read config file
    try:
        with open(args.config, "r") as f:
            config = yaml.load(f)
    except IOError as exc:
        logging.critical("unable to open config file '{}': {}"
                         .format(args.config, exc.strerror))
        sys.exit(1)
    except yaml.YAMLError as exc:
        logging.critical("YAML error while parsing config file: {}".format(exc))
        sys.exit(2)

    # Check that config is okay
    if not isinstance(config, dict):
        logging.critical("config is not a dictionary")
        sys.exit(3)
    if set(config.keys()) != set(["token", "interface", "user_ids"]):
        logging.critical("config is expected to have the following keys: "
                         "'token', 'interface' and 'user_ids'")
        sys.exit(4)
    for key in ("token", "interface"):
        if not isinstance(config[key], str):
            logging.critical("config key '{}' is expected to have string value"
                             .format(key))
            sys.exit(5)
    if not isinstance(config["user_ids"], list) \
    or not all(isinstance(x, int) and x > 0 for x in config["user_ids"]):
        logging.critical("config key 'user_ids' is expected to be list of positive integers")
        sys.exit(6)

    # Create bot
    bot = VIPBot(**config)

    # Run
    logging.info("running telegram bot")
    try:
        bot.run()
    except KeyboardInterrupt:
        logging.info("interrupted by user")
        sys.exit(0)

if __name__ == '__main__':
    main()
