from pyrogram.enums import ChatType
from session import clone_users, users_info
import os


async def clone_handle(client, msg):
  sender_id = msg.from_user.id
  text = msg.text.strip()  
  parts = text.split(maxsplit=1)  
  command = parts[0]  
  value = parts[1] if len(parts) > 1 else None
  
  user = None
  
  if value:
    user = value
  elif msg.reply_to_message:
    user = msg.reply_to_message.from_user.id
  elif msg.chat.type == ChatType.PRIVATE or msg.chat.type == ChatType.BOT:
    user = msg.chat.id
  else:
    await msg.edit("Reply or provide username after command.")
    return
  
  try:
    user = await client.get_users(user)
    profile = bool(user.photo)
    first_name = user.first_name
    user_id = user.id
    mention = f"[{first_name}](tg://user?id={user_id})"
    await msg.edit(f"{mention}'s account cloning...")
  except Exception as e:
    await msg.edit("Looks like I haven't seen this user before.")
    return
  
  data = {
      "first_name" : first_name,
      "profile" : profile,
      "user_id" : user_id
    }
  
  if sender_id not in clone_users:
    clone_users[sender_id] = []
  
  clone_users[sender_id].append(data)
  if profile:
    pfp = await update_pfp(client, user_id)
    if not pfp:
      await msg.edit("Error updating profile.")
      return
  
  try:
    await client.update_profile(first_name=first_name, last_name=None)
  except Exception as e:
    await msg.edit(f"{e}")
    return
  
  await msg.edit(f"{mention}'s account cloned ✅")






async def update_pfp(client, user_id: int):
    photos = []
    async for photo in client.get_chat_photos(user_id, limit=1):
        photos.append(photo)
    
    if not photos:
        return False

    photo = photos[0]
    file_path = await client.download_media(photo.file_id, file_name=f"{user_id}.jpg")
    
    try:
        await client.set_profile_photo(photo=file_path)
    except Exception as e:
        print(f"Error setting profile photo: {e}")
        return False
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    return True