from telethon import events
from firebase import fetch_user
from config import SUDO_USERS



async def send_handle(client, event):
  sender_id = event.sender_id
  
  if sender_id not in SUDO_USERS:
    return
  
  msg = None
  sent = await event.reply("Fetching All users...")
  users = fetch_user()
  if not users:
    await sent.edit("There is no user.")
    return
  
  if event.is_reply:
    msg = await event.get_reply_message()
  else:
    msg = event.message
  
  await sent.edit("Sending in proggress...")
  total_user = len(users)
  
  not_sent = 0
  sent_key = 0

  if msg.media:
    text = event.raw_text.strip()
    parts = text.split(maxsplit=1)
    command = parts[0]  
    value = parts[1] if len(parts) > 1 else ""
    if event.is_reply:
      value = msg.raw_text
    for user in users:
      user = int(user)
      try:
        await client.send_file(
        user,
        msg.media,
        caption=value
        )
        key = users.index(f"{user}") 
        sent_key += 1
        await sent.edit(
    f"📢 **Message Delivery Report**\n\n"
    f"✅ Sent messages to users: {sent_key}\n"
    f"❌ Failed to send messages: {not_sent}\n"
    f"👥 Total users: {total_user}"
)
      except Exception as e:
        not_sent +=1
  else:
    text = event.raw_text.strip()
    parts = text.split(maxsplit=1)
    command = parts[0]  # e.g. "/send"
    value = parts[1] if len(parts) > 1 else ""
    if event.is_reply:
      value = msg.raw_text
    if value == "":
      await sent.edit("Reply or provide text after command.")
      return
    for user in users:
      user = int(user)
      try:
        await client.send_message(
        user,
        value
        )
        key = users.index(f"{user}") 
        sent_key += 1
        await sent.edit(
    f"📢 **Message Delivery Report**\n\n"
    f"✅ Sent messages to users: {sent_key}\n"
    f"❌ Failed to send messages: {not_sent}\n"
    f"👥 Total users: {total_user}"
)
      except Exception as e:
        not_sent +=1