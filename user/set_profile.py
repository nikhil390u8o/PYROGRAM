from pyrogram.raw.functions.account import UpdateUsername
import os

# file_path = jo aapne download kiya hai







async def name_handle(client, msg):
  text = msg.text or ""
  parts = text.split(maxsplit=1)
  command = parts[0] if len(parts) > 0 else ""
  value = parts[1] if len(parts) > 1 else ""
  
  if value == "":
    await msg.edit("Provide a name after command.")
    return
  try:
    await client.update_profile(first_name=value, last_name=None)
  except Exception as e:
    return
  
  await msg.edit(f"Your profile name has been changed to {value}")
  
  

async def username_handle(client, msg):
  text = msg.text or ""
  parts = text.split(maxsplit=1)
  command = parts[0] if len(parts) > 0 else ""
  value = parts[1] if len(parts) > 1 else ""
  
  if value == "":
    await msg.edit("Provide a username after command.")
    return
  try:
    await client.invoke(UpdateUsername(username=value))
  except Exception as e:
    e = str(e)
    if "The username is invalid" in e:
      await msg.edit(f"The username is invalid.")
    elif "The username is already in use by someone else":
      await msg.edit(f"The username is already in use by someone else.")
    else:
      await msg.edit(f"{e}")
      
    return
  await msg.edit(f"Your profile username has been changed to {value}")
  
  


async def update_pfp(client, msg):
  if msg.reply_to_message and msg.reply_to_message.photo:
    await msg.edit("Updating pfp...")
    file_path = await msg.reply_to_message.download()
    try:
      await client.set_profile_photo(photo=file_path)
    except Exception as e:
      await msg.edit(f"{e}")
      return
    await msg.edit("Your profile photo has been changed.")
    if os.path.exists(file_path):
      os.remove(file_path)
  else:
    await msg.edit("Reply to a image containing msg.")
  

async def bio_handle(client, msg):
  text = msg.text or ""
  parts = text.split(maxsplit=1)
  command = parts[0] if len(parts) > 0 else ""
  value = parts[1] if len(parts) > 1 else ""
  
  if value == "":
    await msg.edit("Provide a bio after command.")
    return
  try:
    await client.update_profile(bio=value)
  except Exception as e:
    e = str(e)
    if "ABOUT_TOO_LONG" in e:
      await msg.edit("Provided about/bio text is too long.")
    else:
      await msg.edit(f"{e}")
    return
  
  await msg.edit(f"Your profile bio has been changed.")