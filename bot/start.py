from telethon import events
from config import OWNER_ID, OWNER_NAME, OWNER_USERNAME
import html 
from firebase import add_new_user

img = "https://res.cloudinary.com/dyju9bym4/image/upload/v1754582915/IMG_20250807_213812_840_ldshna.jpg"

async def start_handle(client, event):
  if not event.is_private:
    return
  user_id = event.sender_id
  sender = await event.get_sender()
  first_name = sender.first_name

  mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
  owner = f'<a href="https://t.me/{OWNER_USERNAME}">{OWNER_NAME}</a>'
  
  msg = (
    f"<blockquote>Hey there! {mention}</blockquote>\n"
    "➠ I'm a Userbot Creator Bot\n"
    "➠ Use me to create your own userbot \n"
    "<blockquote>Steps to create a userbot:</blockquote>\n"
    "➠ /gen – Generate a string session\n"
    "➠ /clone &lt;your string session&gt; – Clone the userbot\n"
    "➠ /ping – Check bot is alive or not.\n"
    "➠ That’s it, you’re good to go ✨\n\n"
    f"➠ Owner : {owner}\n\n"
)
  try:
    await event.respond(msg, file=img, parse_mode="html")
  except:
    await event.respond(msg, parse_mode="html")
  user = await event.get_sender()
  data = {
    "first_name": user.first_name,
    "last_name": user.last_name,
    "username": user.username,
    "user_id": user.id,
  }
  add_new_user(data)