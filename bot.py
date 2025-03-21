import os
import json
import logging
from alith import Agent
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get the token from the environment variables
TOKEN = os.getenv("TELEGRAM_API_KEY")
ALITH_API_KEY = os.getenv("ALITH_API_KEY")

# Open JSON file containing eligibility criteria
with open("eligibility_criteria.json", "r") as file:
    criteria = json.load(file)

# Create AI agent
agent = Agent(
    name="GG23 Eligibility Criteria Bot",
    model="gpt-4",
    api_key=ALITH_API_KEY,
    preamble="I am a bot that can help you with the eligibility criteria for the GG23 program. Ask me anything about the eligibility criteria, and I will do my best to help you."
)

# Function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text(
        "Hi! I am a bot that can help you with the eligibility criteria for the GG23 program. Ask me anything about the eligibility criteria, and I will do my best to help you."
    )

# Function to analyze the project description
async def analyze_project(update: Update, context: CallbackContext) -> None:
    """Analyze the project and return the eligibility criteria."""
    user_text = update.message.text
    logger.info(f"Received message: {user_text}")

    try:
        # Check eligibility criteria
        for category, rules in criteria.items():
            for key, requirement in rules.items():
                if key.lower() in user_text.lower():
                    await update.message.reply_text(f"Eligibility Check: {requirement}")
                    return  # Stop checking further if a match is found

        # If criteria are not found, use AI to analyze
        ai_response = await agent.prompt(user_text)  # Ensure it's awaited
        logger.info(f"AI response: {ai_response}")
        
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again.")

# Main function to run the bot
def main() -> None:
    """Start the bot."""
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_project))

    # Start polling
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()