import os
import simplematrixbotlib as smb
from dotenv import load_dotenv
import requests
import random
from timeit import default_timer as timer

load_dotenv()

homeserver = os.environ['KP_HOMESERVER']
username = os.environ['KP_USERNAME']
password = os.environ['KP_PASSWORD']

if homeserver is None or username is None or password is None:
    print("Please set the environment variables KPHOMESERVER, KP_USERNAME and KP_PASSWORD")
    exit(1)

creds = smb.Creds(homeserver, username, password)
bot = smb.Bot(creds)
config = smb.Config()
config.load_toml("config.toml")

@bot.listener.on_message_event
async def pus(room, message):
    match = smb.MessageMatch(room, message, bot)

    if match.is_not_from_this_bot() and match.prefix() and match.command('!pus'):
        start = timer()
        cat = requests.get("https://cataas.com/cat", stream=True)
        # get filetype of cat
        filetype = cat.headers['content-type'].split('/')[1]

        # save cat file with filetype
        with open(f'./pus/cat.{filetype}', 'wb') as f:
            f.write(cat.content)
        # send cat file
            await bot.api.send_image_message(room.room_id, f'./pus/cat.{filetype}')
        # delete cat file
        os.remove(f'./pus/cat.{filetype}')
        end = timer()
        print("!pus tok " + str(end - start) + " sekunder til å kjøre.")

@bot.listener.on_message_event
async def pus_si(room, message):
    match = smb.MessageMatch(room, message, bot)

    if match.is_not_from_this_bot() and match.prefix() and match.command('!pus_si'):
        start = timer()
        s = " ".join(match.args())
        cat = requests.get("https://cataas.com/cat/says/" + s,  stream=True)
        # get filetype of cat
        filetype = cat.headers['content-type'].split('/')[1]

        # save cat file with filetype
        with open(f'./pus/cat.{filetype}', 'wb') as f:
            f.write(cat.content)
        # send cat file
            await bot.api.send_image_message(room.room_id, f'./pus/cat.{filetype}')
        # delete cat file
        os.remove(f'./pus/cat.{filetype}')
        end = timer()
        print("!pus_si tok " + str(end - start) + " sekunder til å kjøre.")

@bot.listener.on_startup
async def startup(stfu):
    print('Bot started!')
    print('Checking for pus folder...')
    if not os.path.exists('./pus'):
        os.makedirs('./pus')
        print('Pus folder created!')
    else:
        print('Pus folder found!')

bot.run()