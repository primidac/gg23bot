# importing all dependencies for the project
import os
import json
from alith import Agent
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# load the environment variables
load_dotenv()

# get the token from the environment variables
TOKEN = os.getenv("TELEGRAM_API_KEY")
ALITH_API_KEY = os.getenv("ALITH_API_KEY")

# open json file
with open("eligibility_criteria.json", "r") as file:
    criteria = json.load(file)


# create agent
agent = Agent(
    name="GG23 Eligibility Criteria Bot",
    model="gpt-4",
    api_key=ALITH_API_KEY,
    preamble="I am a bot that can help you with the eligibility criteria for the GG23 program. Ask me anything about the eligibility criteria and I will do my best to help you."
)


# function to handle the /start command
def start(update: Updater, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi! I am a bot that can help you with the eligibility criteria for the GG23 program. Ask me anything about the eligibility criteria and I will do my best to help you.")
    

# analyze function
def analyze_project(update: Updater, context: CallbackContext) -> None:
    """Analyze the project and return the eligibility criteria."""
    # get the message from the user
    user_text = update.message.text
    # check eligibility criteria
    for category, rules in criteria.items():
        for key, requirement in rules.items():
            if key in user_text.lower():
                update.message.reply_text(f"Eligbility Check: {requirement}")
    
    # if if criteria is not found
    ai_response = agent.prompt(user_text)
    update.message.reply_text(ai_response)

def main() -> None:
    # create the updater
    updater = Updater(TOKEN, usecontext=True)
    # get the dispatcher
    dispatcher = updater.dispatcher

    # add the /start command handler
    dispatcher.add_handler(CommandHandler("start", start))
    # add the message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, analyze_project))

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()



