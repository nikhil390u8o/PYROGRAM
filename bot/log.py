from telethon import events
from config import CHAT_ID, bot_info



async def log_msg(client, event):
  bot = bot_info.get("user_id")
  chat_id = event.chat_id
  user_id = event.sender_id
  user = await event.get_sender()
  first_name = user.first_name
  mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
  username = f"@{user.username}" if user.username else mention
  
  if chat_id == CHAT_ID:
    return
  
  if not event.is_private:
    if event.is_reply:
      reply = await event.get_reply_message()
      sender = reply.sender_id
      if not sender == bot:
        return
    else:
      return
      
  msg = event.message
  if not msg:
    return
  if msg.gif or msg.sticker:
    return
  
  text = msg.text
  if not text:
    text = ""
    
  msg_to_send = f"""{text}
<blockquote>Name : {first_name}
Username : {username}
User ID : <code>{user_id}</code></blockquote>
  """

  
  if msg.media:
    try:
      await client.send_file(CHAT_ID, file=msg.media, caption=msg_to_send, parse_mode="html")
    except Exception as e:
      print(e)
  elif msg.text:
    try:
      await client.send_message(CHAT_ID, msg_to_send, parse_mode="html")
    except Exception as e:
      print(e)