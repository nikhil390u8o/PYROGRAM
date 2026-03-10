import os
import threading
import asyncio
from flask import Flask
from telethon import TelegramClient
from pyrogram import Client
from pytgcalls import PyTgCalls

from config import API_ID, API_HASH, BOT_TOKEN, bot_info
from bot_handlers import register_bot
from user_handlers import register_user
from session import users, my_profile, set_ping
from firebase import fetch_sessions_from_database

active_user_sessions = {}
app = Flask(__name__)

@app.route('/')
def home():
    msg = f"""bot is running ✅
Name : {bot_info.get("name")}
Username : {bot_info.get("username")}
User ID : {bot_info.get("user_id")}
"""
    return msg

bot = None
userbot = None

# Custom asyncio exception handler to ignore "Peer id invalid" errors globally
def handle_exception(loop, context):
    exception = context.get("exception")
    if exception and isinstance(exception, ValueError) and "Peer id invalid" in str(exception):
        print("Ignored Peer id invalid error")
        return
    loop.default_exception_handler(context)

async def run_bot_async():
    global bot
    try:
        bot = TelegramClient("bot", API_ID, API_HASH)
        await bot.start(bot_token=BOT_TOKEN)

        me = await bot.get_me()
        user_id = me.id
        first_name = me.first_name
        username = me.username

        bot_info["name"] = first_name
        bot_info["username"] = username
        bot_info["user_id"] = user_id

        register_bot(bot)
        set_ping()
        fetch_sessions_from_database()

        print(f"{first_name} Bot is connected and running...")

        await bot.run_until_disconnected()

    except Exception as e:
        print(f"run_bot_async error: {e}")


async def monitor_new_clients():
    while True:
        for session_str in users.get("client", []):

            if session_str not in active_user_sessions:
                try:

                    user_client = Client(
                        name=session_str,
                        api_id=API_ID,
                        api_hash=API_HASH,
                        session_string=session_str
                    )

                    await user_client.start()

                    # 🔊 Start Voice Chat Engine
                    try:
                        user_client.call_py = PyTgCalls(user_client)
                        await user_client.call_py.start()
                        print("VC engine started for user")
                    except Exception as vc_error:
                        print(f"VC start error: {vc_error}")

                    try:
                        me = await user_client.get_me()
                        my_profile(me)

                        register_user(user_client)

                        active_user_sessions[session_str] = user_client

                        print(f"Userbot connected: {me.first_name}")

                    except Exception as e:
                        print(f"Failed to get user info or register user: {e}")
                        await user_client.disconnect()

                except Exception as e:
                    clients = users.get("client", [])
                    if session_str in clients:
                        clients.remove(session_str)

                    print(f"Removed 1 user not working session: {e}")

        await asyncio.sleep(5)


def run_users():
    loop = asyncio.new_event_loop()
    loop.set_exception_handler(handle_exception)
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(monitor_new_clients())

    except Exception as e:
        print(f"user bot error: {e}")


def run_bot():
    loop = asyncio.new_event_loop()
    loop.set_exception_handler(handle_exception)
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(run_bot_async())

    except Exception as e:
        print(f"Bot error: {e}")


if __name__ == "__main__":

    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    user_thread = threading.Thread(target=run_users, daemon=True)
    user_thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
