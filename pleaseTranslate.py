# Name: pleaseTranslate (/u/pleaseTranslate)
# Author: Saroekin (/u/Saroekin)
# Version: Python 2.7.6

#Files or importations that are used elsewhere in program.
import os
import praw
import time
import traceback
import externals_pleaseTranslate
from mstranslator import Translator

#Setting up account.
translator = Translator(externals_pleaseTranslate.client_ID, externals_pleaseTranslate.client_secret)

#User's username and password.
Username = externals_pleaseTranslate.username
Password = externals_pleaseTranslate.password

#What reddit sees from the bot's requests.
user_agent = externals_pleaseTranslate.user_agent
r = praw.Reddit(user_agent = user_agent)
print("\n\nLogging in. . .\n\n")
r.login(Username, Password)

#Set of list variables for program.
fullLangNames = externals_pleaseTranslate.fullLangNames
abbrevLangNames = externals_pleaseTranslate.abbrevLangNames
supportedLangs = externals_pleaseTranslate.supportedLangs

#Message/link variables.
source_link = "https://github.com/Saroekin/pleaseTranslate"
pm_link = "https://www.reddit.com/message/compose/?to=Saroekin&subject=/u/pleaseTranslate"
info_post = "https://www.reddit.com/r/Saroekin_redditBots/comments/354g14/upleasetranslate_information/"

#Templates for messages and comments (and variables).
REPLY_MENTION_TEMPLATE = """
**Translated from *%s* to *%s*:**

%s

---
*I am a bot. If you have any questions or concerns, please feel free to contact my [creator]({pm_link}).*

^| ^[Source]({source_link}) ^| ^[Functionalities]({info_post}) ^|
""".format(pm_link = pm_link, info_post = info_post, source_link = source_link)

ERROR_MESSAGE_TEMPLATE = """
There was an error regarding your request.

Please review your syntax and make sure it fits the guidelines stated in this [post]({info_post}).

---
*I am a bot. If you have any questions or concerns, please feel free to contact my [creator]({pm_link}).*
""".format(info_post = info_post, pm_link = pm_link)

transMessage = REPLY_MENTION_TEMPLATE

errorMessage = ERROR_MESSAGE_TEMPLATE

#Definition for bot to reply towards username mentions.
def message_check():
    for message in r.get_unread():
        message_text = message.body.lower()
        if '[t-' not in message_text:
            message.mark_as_read()
            continue
        if 'n-/u/pleasetranslate' in message_text:
            message.mark_as_read()
            continue
        try:
            mauth = message.author.name
        except AttributeError:
            message.mark_as_read()
            continue

#Definition that translates the actual message and outputs the result.
def message_translate():
    for message in r.get_unread():
        if message.subject not in ['username mention', 'comment reply'] and not type(message) == praw.objects.Comment:
            message.mark_as_read()
            continue
        full_message_text = message.body
        messageList = full_message_text.split()
        defaultLang = translator.detect_lang(full_message_text)
        usedWord = ""
        count = 0
        #Fixing up default language styling.
        index = supportedLangs.index(defaultLang)
        finalized_defualtLang = fullLangNames[index]
        finalized_defualtLang = finalized_defualtLang.replace("[t-", "").replace("]", "")
        finalized_defualtLang = finalized_defualtLang.capitalize()
        #Looking for requested translation throughout message.
        for word in messageList:
            if word.lower() == "/u/pleasetranslate":
                full_message_text = full_message_text.replace(word, "")
            if word.lower() in fullLangNames:
                usedWord = word.lower()
                index = fullLangNames.index(usedWord)
                transLang = supportedLangs[index]
                requestTransLang = fullLangNames[index]
                full_message_text = full_message_text.replace(word, "")
                count += 1
            elif word.lower() in abbrevLangNames:
                usedWord = word.lower()
                index = abbrevLangNames.index(usedWord)
                transLang = supportedLangs[index]
                requestTransLang = fullLangNames[index]
                full_message_text = full_message_text.replace(word, "")
                count += 1
        if count < 1:
            message.reply(errorMessage)
            message.mark_as_read()
            continue
        #Used for setting up designated language in reply message.
        requestTransLang = requestTransLang.replace("[t-", "").replace("]", "")
        requestTransLang = requestTransLang.capitalize()
        #Arranging formattign for translation message.
        translation = (translator.translate(full_message_text, lang_from = defaultLang, lang_to = transLang))
        #Quoting entire message.
        translation = '>' + translation.replace('\n', '\n>')
        #Replying to user with finalized translation.
        message.reply(transMessage % (finalized_defualtLang, requestTransLang, translation))
        message.mark_as_read()

#Where bot begins (continues) to run.
print("/u/pleaseTranslate is currently translating. . .\n")
while True:
    try:
        message_check()
        message_translate()
    except Exception as e:
        traceback.print_exc()
        time.sleep(30)
    
    
