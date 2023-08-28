from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import TOKEN
BOT_USERNAME: Final = '@spotifyrandomsongbot_bot'

# Spotify credentials
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET


# Spotify playlist URI
from config import PLAYLIST_URI

# Initialize the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

# Retrieve songs from the Spotify playlist
playlist = sp.playlist_tracks(PLAYLIST_URI)
song_list = [track['track']['external_urls']['spotify'] for track in playlist['items']]


#COMMANDS
#why async?
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Hey, this is my first version as she is new to this. Thanks for chatting with me.");

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = [
        '/start - Start the bot',
        '/help - Get help',
        '/custom - Perform a custom command',
        '/recommendSong - Get a recommended song'
    ]
    commands_text = '\n'.join(commands)
    await update.message.reply_text(f"Hey, this is my first version as she is new to this. Thanks for chatting with me.\n\nAvailable commands:\n{commands_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help is on the way.");

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your wish is my command, I am your bot.");

async def recommendSong_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_song = random.choice(song_list)
    await update.message.reply_text(f"There you go: {random_song}")

#RESPONSES
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Oui'

    if 'how are you' in processed:
        return 'All good. How are you?'
        
    if 'song' in processed:
        return f"There you go: {random.choice(song_list)}"

    return 'Ok, I\'m done'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message. Group chat or private chat?
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else: # Reply normal if the message is in private
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)




# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('songRecommendation',recommendSong_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    #Polls the bot
    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
