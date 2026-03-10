from telethon import events
from pyrogram import Client
from config import API_ID, API_HASH, CHAT_ID
from session import users
import asyncio
from pyrogram.enums import ParseMode
from pyrogram import enums
from firebase import add_user_to_database






req = "Please provide your Pyrogram string session after this command."
already_running = "The userbot is already running. 🚀"
regen = "The provided pyrogram session string is invalid."

async def clone_handle(client, event):
  text = event.raw_text 
  parts = text.split(maxsplit=1)  
  command = parts[0] if len(parts) > 0 else ""
  value = parts[1] if len(parts) > 1 else ""
  
  clients = users.get("client", [])
  if value=="":
    await event.reply(req)
    return
  
  if value in clients:
    await event.reply(already_running)
    return
  
  sent = await event.reply(f"Deploying...")
  me = await is_valid_session(value)
  
  
  if not me:
    await sent.edit(regen)
    return
  
  first_name = me.get("first_name")
  user_id = me.get("user_id")
  username = me.get("username")
  mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
  
  users.setdefault('client', []).append(value)
  await deploy_animation(event, user_id, mention, sent)
  
  me["string"] = value
  add_user_to_database(me)
  
  mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
  message = f"""<blockquote>New User Login</blockquote>
<b>Name :</b> {first_name}
<b>Username :</b> @{username if username else "N/A"}
<b>User ID :</b> <code>{user_id}</code>"""
  
  try:
    await client.send_message(CHAT_ID, message, parse_mode="html")
  except Exception as e:
    print(e)
  
  



progress = [
    "[▒▒▒▒▒▒▒▒▒▒]",
    "[▓▒▒▒▒▒▒▒▒▒]",
    "[▓▓▒▒▒▒▒▒▒▒]",
    "[▓▓▓▒▒▒▒▒▒▒]",
    "[▓▓▓▓▒▒▒▒▒▒]",
    "[▓▓▓▓▓▒▒▒▒▒]",
    "[▓▓▓▓▓▓▒▒▒▒]",
    "[▓▓▓▓▓▓▓▒▒▒]",
    "[▓▓▓▓▓▓▓▓▒▒]",
    "[▓▓▓▓▓▓▓▓▓▒]",
    "[▓▓▓▓▓▓▓▓▓▓]"
]

console = [
    "[INFO]: Initializing deployment... ℹ️",
    "[INFO]: Checking dependencies... 🔍",
    "[INFO]: Connecting to server... 🌐",
    "[INFO]: Uploading files... 📤",
    "[INFO]: Configuring environment... ⚙️",
    "[INFO]: Starting services... 🚀",
    "[INFO]: Running tests... 🧪",
    "[INFO]: Finalizing setup... 🧹",
    "[INFO]: Cleaning up temporary files... 🗑️",
    "[INFO]: Securing connections... 🔒",
    "[SUCCESS]: Deployment completed 🎉🚀"
]

def get_console(index):
  if index < 1:
    return ""
  return "\n".join(console[:index])

async def deploy_animation(event, user_id, mention,sent):
  
  for i in range(0, 12):
    if i == 11:
      c = console[10]
      message = f"{mention} is now Deployed! 🚀"
      await sent.edit(f"{message}", parse_mode="html")
    else:
      pa = progress[i]
      p = i * 10
      c = get_console(i)
      c_mention = f'<a href="tg://user?id={user_id}">{c}</a>'
      await sent.edit(f"{pa} {p}% Deploying...<blockquote>{c_mention}</blockquote>", parse_mode="html")
      await asyncio.sleep(0.5)





async def is_valid_session(session_string):
  client = Client("me", session_string=session_string)
  try:
    await client.start()
    me = await client.get_me()
    data = {
    "first_name": me.first_name,
    "last_name" : me.last_name,
    "user_id" : me.id,
    "phone" : me.phone_number,
    "username" : me.username
    }
    await client.stop()
    return data
  except Exception as e:
    return False